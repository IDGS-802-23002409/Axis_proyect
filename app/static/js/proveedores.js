document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal-proveedor');
    const form = document.getElementById('form-proveedor');
    const modalTitle = document.getElementById('modal-title');
    const btnNuevo = document.getElementById('btn-nuevo-proveedor');
    const btnClose = document.getElementById('btn-close-modal');

    // Función para abrir modal
    const showModal = () => modal.classList.remove('hidden');
    
    // Función para cerrar modal
    const hideModal = () => {
        modal.classList.add('hidden');
        form.reset();
    };

    // Abrir para Nuevo Proveedor
    if (btnNuevo) {
        btnNuevo.addEventListener('click', () => {
            modalTitle.innerText = "Registrar Proveedor";
            form.action = "/proveedores/guardar";
            form.reset();
            showModal();
        });
    }

    // Cerrar modal
    if (btnClose) btnClose.addEventListener('click', hideModal);

    // Cerrar al hacer clic fuera del contenido
    window.addEventListener('click', (e) => {
        if (e.target === modal) hideModal();
    });

    // Lógica para los botones de EDITAR
    document.querySelectorAll('.btn-edit').forEach(button => {
        button.addEventListener('click', async () => {
            const uid = button.getAttribute('data-uid');
            modalTitle.innerText = "Editar Proveedor";
            form.action = `/proveedores/editar/${uid}`;

            try {
                const response = await fetch(`/proveedores/api/get/${uid}`);
                if (!response.ok) throw new Error('Error al obtener datos');
                
                const data = await response.json();
                
                document.getElementById('razon_social').value = data.razon_social;
                document.getElementById('rfc').value = data.rfc;
                document.getElementById('contacto_nombre').value = data.contacto_nombre;
                
                showModal();
            } catch (error) {
                console.error(error);
                alert("Error al cargar los datos del proveedor.");
            }
        });
    });

    // Confirmación de eliminación
    document.querySelectorAll('.delete-form').forEach(deleteForm => {
        deleteForm.addEventListener('submit', (e) => {
            if (!confirm('¿Estás seguro de que deseas eliminar este proveedor?')) {
                e.preventDefault();
            }
        });
    });
});