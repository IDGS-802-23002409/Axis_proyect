DELIMITER //

CREATE PROCEDURE sp_procesar_venta_hibrida(
    IN p_uuid_venta VARCHAR(36),
    IN p_numero_pedido VARCHAR(25),
    IN p_uuid_cliente VARCHAR(36),
    IN p_metodo_pago VARCHAR(50),
    IN p_json_items JSON,
    OUT p_resumen_json JSON
)
proc: BEGIN
    DECLARE v_i INT DEFAULT 0;
    DECLARE v_count INT;
    DECLARE v_uuid_item VARCHAR(36);
    DECLARE v_cantidad INT;
    DECLARE v_precio DECIMAL(12,2);
    DECLARE v_stock_actual INT;
    DECLARE v_cantidad_venta INT;
    DECLARE v_cantidad_pedido INT;
    DECLARE v_uuid_pedido VARCHAR(36);
    DECLARE v_uuid_detalle_pedido VARCHAR(36);
    DECLARE v_has_pedido BOOLEAN DEFAULT FALSE;
    
    -- Variables para Producción y Receta
    DECLARE v_uuid_op VARCHAR(36);
    DECLARE v_cantidad_op INT;
    DECLARE v_uuid_explosion VARCHAR(36);
    DECLARE v_uuid_insumo VARCHAR(36);
    DECLARE v_consumo_u DECIMAL(12,4);
    DECLARE v_necesario DECIMAL(12,4);
    DECLARE v_u_medida VARCHAR(20);
    DECLARE v_prendas_rest INT;
    
    -- Variables para Trazabilidad de Rollos
    DECLARE v_rollo_id VARCHAR(36);
    DECLARE v_rollo_metraje DECIMAL(12,4);
    DECLARE v_prendas_rollo INT;
    DECLARE v_prendas_usar INT;
    DECLARE v_metros_usar DECIMAL(12,4);
    DECLARE v_uuid_corte VARCHAR(36);  -- ID del ejecucion_corte (agrupadon por insumo)
    
    DECLARE done INT DEFAULT FALSE;
    
    -- Error handling ACID
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- 1. Crear Encabezado de Venta
    INSERT INTO ventas_encabezado (uuid_venta, numero_pedido, uuid_cliente, metodo_pago, estatus_envio, fecha_venta, fecha_actualizacion)
    VALUES (p_uuid_venta, p_numero_pedido, p_uuid_cliente, p_metodo_pago, 'Procesando', NOW(), NOW());

    SET v_uuid_pedido = UUID();
    SET v_count = JSON_LENGTH(p_json_items);
    
    -- ─────────────────────────────────────────
    -- 2. Bucle principal: procesar cada item del carrito
    -- ─────────────────────────────────────────
    WHILE v_i < v_count DO
        SET v_uuid_item = JSON_UNQUOTE(JSON_EXTRACT(p_json_items, CONCAT('$[', v_i, '].uuid_producto')));
        SET v_cantidad = JSON_EXTRACT(p_json_items, CONCAT('$[', v_i, '].quantity'));
        SET v_precio = JSON_EXTRACT(p_json_items, CONCAT('$[', v_i, '].price'));

        -- Bloqueo de stock (FOR UPDATE para evitar race conditions)
        SELECT stock_fisico_actual, uuid_explosion INTO v_stock_actual, v_uuid_explosion
        FROM productos_terminados 
        WHERE uuid_producto = v_uuid_item 
        FOR UPDATE;

        -- Partición: qué va a venta directa y qué va a producción
        IF v_stock_actual >= v_cantidad THEN
            SET v_cantidad_venta = v_cantidad;
            SET v_cantidad_pedido = 0;
        ELSE
            SET v_cantidad_venta = GREATEST(0, v_stock_actual);
            SET v_cantidad_pedido = v_cantidad - v_cantidad_venta;
        END IF;

        -- ── Detalle de Venta (items con stock disponible) ──
        IF v_cantidad_venta > 0 THEN
            INSERT INTO ventas_detalle (uuid_detalle, uuid_venta, uuid_producto, cantidad, precio_unitario_historico)
            VALUES (UUID(), p_uuid_venta, v_uuid_item, v_cantidad_venta, v_precio);
            
            UPDATE productos_terminados 
            SET stock_fisico_actual = stock_fisico_actual - v_cantidad_venta 
            WHERE uuid_producto = v_uuid_item;
        END IF;

        -- ── Pedido + Producción (items sin stock suficiente) ──
        IF v_cantidad_pedido > 0 THEN
            -- Crear encabezado del pedido si es la primera vez
            IF NOT v_has_pedido THEN
                INSERT INTO pedidos_cliente_encabezado (uuid_pedido, numero_pedido, uuid_cliente, uuid_venta_origen, estatus, fecha_pedido, fecha_actualizacion)
                VALUES (v_uuid_pedido, CONCAT('PED-', p_numero_pedido), p_uuid_cliente, p_uuid_venta, 'Pendiente', NOW(), NOW());
                SET v_has_pedido = TRUE;
            END IF;

            -- Detalle del pedido pendiente
            SET v_uuid_detalle_pedido = UUID();
            INSERT INTO pedidos_cliente_detalle (uuid_detalle_pedido, uuid_pedido, uuid_producto, cantidad, precio_unitario_historico, estatus_item)
            VALUES (v_uuid_detalle_pedido, v_uuid_pedido, v_uuid_item, v_cantidad_pedido, v_precio, 'Pendiente');

            -- Orden de Producción
            SET v_cantidad_op = v_cantidad_pedido;
            SET v_uuid_op = UUID();
            INSERT INTO ordenes_produccion (uuid_op, uuid_producto, uuid_pedido_detalle, cantidad_a_producir, estado, fecha_solicitud)
            VALUES (v_uuid_op, v_uuid_item, v_uuid_detalle_pedido, v_cantidad_op, 'Pendiente', NOW());

            -- ── Reserva de Materiales (según receta) ──
            BEGIN
                DECLARE cur_insumos CURSOR FOR 
                    SELECT uuid_insumo, consumo_teorico_unitario 
                    FROM explosion_materiales_detalle 
                    WHERE uuid_explosion = v_uuid_explosion;
                DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
                
                SET done = FALSE;
                OPEN cur_insumos;
                insumo_loop: LOOP
                    FETCH cur_insumos INTO v_uuid_insumo, v_consumo_u;
                    IF done THEN LEAVE insumo_loop; END IF;
                    
                    SET v_necesario = v_consumo_u * v_cantidad_op;
                    
                    -- Descontar del stock total del insumo (bloqueo)
                    SELECT unidad_medida INTO v_u_medida 
                    FROM insumos WHERE uuid_insumo = v_uuid_insumo FOR UPDATE;
                    
                    UPDATE insumos 
                    SET stock_total_acumulado = stock_total_acumulado - v_necesario 
                    WHERE uuid_insumo = v_uuid_insumo;
                    
                    -- ── Trazabilidad de telas (ROLLO): usar ejecucion_corte_rollo ──
                    IF v_u_medida = 'ROLLO' THEN
                        SET v_prendas_rest = v_cantidad_op;

                        -- Crear registro de corte agregado para este insumo
                        SET v_uuid_corte = UUID();
                        INSERT INTO ejecucion_corte (uuid_corte, uuid_op, metros_teoricos_requeridos, metros_sacados_bodega, prendas_reales_logradas, fecha_proceso)
                        VALUES (v_uuid_corte, v_uuid_op, v_necesario, v_necesario, v_cantidad_op, NOW());

                        -- Sub-bucle: registrar consumo por rollo específico
                        BEGIN
                            DECLARE cur_rollos CURSOR FOR 
                                SELECT uuid_rollo, metraje_continuo_actual 
                                FROM rollos_inventario 
                                WHERE uuid_insumo = v_uuid_insumo AND metraje_continuo_actual > 0 
                                ORDER BY fecha_creacion ASC;
                            DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
                            
                            OPEN cur_rollos;
                            rollos_loop: LOOP
                                FETCH cur_rollos INTO v_rollo_id, v_rollo_metraje;
                                IF done THEN SET done = FALSE; LEAVE rollos_loop; END IF;
                                
                                SET v_prendas_rollo = FLOOR(v_rollo_metraje / v_consumo_u);
                                IF v_prendas_rollo > 0 THEN
                                    SET v_prendas_usar = LEAST(v_prendas_rest, v_prendas_rollo);
                                    SET v_metros_usar = v_prendas_usar * v_consumo_u;
                                    
                                    -- Descontar metraje físico del rollo
                                    UPDATE rollos_inventario 
                                    SET metraje_continuo_actual = metraje_continuo_actual - v_metros_usar 
                                    WHERE uuid_rollo = v_rollo_id;
                                    
                                    -- Trazabilidad granular: qué rollo aportó cuántos metros
                                    INSERT INTO ejecucion_corte_rollo (uuid, uuid_corte, uuid_rollo, uuid_insumo, metros_usados)
                                    VALUES (UUID(), v_uuid_corte, v_rollo_id, v_uuid_insumo, v_metros_usar);
                                    
                                    SET v_prendas_rest = v_prendas_rest - v_prendas_usar;
                                END IF;
                                
                                IF v_prendas_rest <= 0 THEN LEAVE rollos_loop; END IF;
                            END LOOP rollos_loop;
                            CLOSE cur_rollos;
                            SET done = FALSE; -- Reset para continuar el loop de insumos
                        END;
                    END IF;
                END LOOP insumo_loop;
                CLOSE cur_insumos;
            END;
        END IF;

        SET v_i = v_i + 1;
    END WHILE;

    -- 3. Actualizar estatus final de la venta
    IF v_has_pedido THEN
        UPDATE ventas_encabezado SET estatus_envio = 'Pendiente' WHERE uuid_venta = p_uuid_venta;
    ELSE
        UPDATE ventas_encabezado SET estatus_envio = 'Completado' WHERE uuid_venta = p_uuid_venta;
    END IF;

    COMMIT;
    
    -- 4. Devolver resumen al caller Python
    SET p_resumen_json = JSON_OBJECT(
        'has_pedido', v_has_pedido,
        'uuid_pedido', IF(v_has_pedido, v_uuid_pedido, NULL)
    );

END //

DELIMITER ;
