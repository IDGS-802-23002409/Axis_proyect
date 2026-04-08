document.addEventListener('DOMContentLoaded', () => {
    // Configuración global GSAP
    gsap.registerPlugin(ScrollTrigger);

    /* =========================================
       CART DRAWER LOGIC - SIMPLE (SIN APIs)
       ========================================= */
    const cartBtn = document.getElementById('cart-btn');
    const cartCloseBtn = document.getElementById('cart-close-btn');
    const cartOverlay = document.getElementById('cart-overlay');
    const cartDrawer = document.getElementById('cart-drawer');
    const cartContinueBtn = document.getElementById('cart-continue-btn');

    let isCartOpen = false;

    function toggleCart(state) {
        if (state === undefined) isCartOpen = !isCartOpen;
        else isCartOpen = state;

        if (isCartOpen) {
            cartOverlay.classList.remove('opacity-0', 'pointer-events-none');
            cartOverlay.classList.add('opacity-100');
            cartDrawer.classList.remove('translate-x-full');
            cartDrawer.classList.add('translate-x-0');
            // Recargar la página para obtener el carrito actualizado desde el archivo JSON
            if (!document.getElementById('cart-items-list').hasAttribute('data-loaded')) {
                window.location.reload();
            }
        } else {
            cartOverlay.classList.add('opacity-0', 'pointer-events-none');
            cartOverlay.classList.remove('opacity-100');
            cartDrawer.classList.add('translate-x-full');
            cartDrawer.classList.remove('translate-x-0');
        }
    }

    if (cartBtn) cartBtn.addEventListener('click', () => toggleCart(true));
    if (cartCloseBtn) cartCloseBtn.addEventListener('click', () => toggleCart(false));
    if (cartOverlay) cartOverlay.addEventListener('click', () => toggleCart(false));
    if (cartContinueBtn) cartContinueBtn.addEventListener('click', () => toggleCart(false));

    /* =========================================
       TOAST / ALERTS LOGIC
       ========================================= */
    function showToast(message, type = 'info') {
        const container = document.getElementById('flash-container') || createFlashContainer();
        const toast = document.createElement('div');
        toast.className = `flash-msg flex items-start gap-3 px-4 py-3 border shadow-xl text-sm backdrop-blur-md transition-all duration-300 translate-x-full opacity-0`;

        let bgColor, borderColor, icon, iconColor;
        if (type === 'error') {
            bgColor = 'bg-destructive/10'; borderColor = 'border-destructive/50'; icon = 'alert-circle'; iconColor = 'text-destructive';
        } else if (type === 'success') {
            bgColor = 'bg-emerald-500/10'; borderColor = 'border-emerald-500/50'; icon = 'check-circle'; iconColor = 'text-emerald-400';
        } else if (type === 'warning') {
            bgColor = 'bg-amber-500/10'; borderColor = 'border-amber-500/50'; icon = 'alert-triangle'; iconColor = 'text-amber-400';
        } else {
            bgColor = 'bg-secondary'; borderColor = 'border-border'; icon = 'info'; iconColor = 'text-primary';
        }

        toast.classList.add(bgColor, borderColor);
        toast.innerHTML = `
            <i data-lucide="${icon}" class="w-4 h-4 mt-0.5 shrink-0 ${iconColor}"></i>
            <span>${message}</span>
        `;

        container.appendChild(toast);
        lucide.createIcons();

        // Animate in
        requestAnimationFrame(() => {
            toast.classList.remove('translate-x-full', 'opacity-0');
        });

        // Auto remove
        setTimeout(() => {
            toast.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    function createFlashContainer() {
        const c = document.createElement('div');
        c.id = 'flash-container';
        c.className = 'fixed top-20 right-4 z-[200] space-y-2 max-w-sm w-full';
        document.body.appendChild(c);
        return c;
    }

    // Auto-abrir carrito si el backend lo solicita
    if (document.body.dataset.openCart === 'true') {
        setTimeout(() => toggleCart(true), 500);
    }

    // Marcar como cargado
    const cartItemsList = document.getElementById('cart-items-list');
    if (cartItemsList) cartItemsList.setAttribute('data-loaded', 'true');

    /* =========================================
       HEADER LOGIC
       ========================================= */
    const header = document.getElementById('main-header');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIconOpen = document.getElementById('menu-icon-open');
    const menuIconClose = document.getElementById('menu-icon-close');
    const mobileLinks = document.querySelectorAll('.mobile-link');
    let isMobileMenuOpen = false;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('bg-background/95', 'backdrop-blur-md', 'border-b', 'border-border');
            header.classList.remove('bg-transparent');
        } else {
            header.classList.remove('bg-background/95', 'backdrop-blur-md', 'border-b', 'border-border');
            header.classList.add('bg-transparent');
        }
    });

    function toggleMobileMenu() {
        isMobileMenuOpen = !isMobileMenuOpen;
        if (isMobileMenuOpen) {
            menuIconOpen.classList.add('hidden'); menuIconOpen.classList.remove('block');
            menuIconClose.classList.add('block'); menuIconClose.classList.remove('hidden');
            mobileMenu.classList.add('opacity-100', 'visible');
            mobileMenu.classList.remove('opacity-0', 'invisible');
            mobileLinks.forEach(link => { link.style.animation = 'fadeInUp 0.5s ease forwards'; });
        } else {
            menuIconOpen.classList.add('block'); menuIconOpen.classList.remove('hidden');
            menuIconClose.classList.add('hidden'); menuIconClose.classList.remove('block');
            mobileMenu.classList.add('opacity-0', 'invisible');
            mobileMenu.classList.remove('opacity-100', 'visible');
            mobileLinks.forEach(link => { link.style.animation = 'none'; });
        }
    }

    if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', toggleMobileMenu);
    mobileLinks.forEach(link => link.addEventListener('click', () => { if (isMobileMenuOpen) toggleMobileMenu(); }));

    /* =========================================
       HERO LOGIC
       ========================================= */
    const heroSection = document.getElementById('hero-section');
    if (heroSection) {
        const heroTextAxis = document.getElementById('hero-text-axis');
        const heroOverlay = document.getElementById('hero-flashlight-overlay');
        const heroControls = document.getElementById('hero-controls-container');
        const subtitle = document.getElementById('hero-subtitle');
        const btnPrimary = document.getElementById('hero-btn-primary');
        const btnSecondary = document.getElementById('hero-btn-secondary');
        const scrollHint = document.getElementById('hero-scroll-hint');

        let searchPhase = 'scan';
        let maskMouse = { x: 50, y: 50 };
        let revealProgress = 0;
        let freezeScroll = true;

        // document.body.style.overflow = 'hidden';
        // document.body.style.touchAction = 'none';

        let frameId; let finishTimeout; let rafId;
        let x = 12, y = 22, dx = 2.3, dy = 1.6;

        function animateFlashlight() {
            if (searchPhase !== 'scan') return;
            x += dx; y += dy;
            if (x <= 6 || x >= 94) dx = -dx;
            if (y <= 12 || y >= 88) dy = -dy;
            maskMouse.x = Math.max(5, Math.min(95, x));
            maskMouse.y = Math.max(10, Math.min(90, y));
            if (heroOverlay) {
                heroOverlay.style.background = `radial-gradient(circle 18vw at ${maskMouse.x}% ${maskMouse.y}%, rgba(0,0,0,0) 0%, rgba(0,0,0,0.7) 68%, rgba(0,0,0,0.94) 100%)`;
            }
            frameId = setTimeout(animateFlashlight, 18);
        }
        animateFlashlight();

        finishTimeout = setTimeout(() => {
            searchPhase = 'found';
            if (frameId) clearTimeout(frameId);
            const duration = 900;
            const start = performance.now();

            function step(now) {
                const t = Math.min(1, (now - start) / duration);
                revealProgress = t;
                if (heroTextAxis && heroOverlay) {
                    heroTextAxis.style.filter = `brightness(${0.65 + 0.35 * t}) grayscale(${1 - t})`;
                    heroOverlay.style.opacity = 1 - t;
                    heroOverlay.style.background = `radial-gradient(circle ${18 + 22 * t}vw at ${maskMouse.x}% ${maskMouse.y}%, rgba(0,0,0,0) 0%, rgba(0,0,0,${0.7 * (1 - t)}) 68%, rgba(0,0,0,${0.94 * (1 - t)}) 100%)`;
                }
                if (t < 1) rafId = requestAnimationFrame(step);
                else { heroOverlay.style.display = 'none'; showControls(); }
            }
            rafId = requestAnimationFrame(step);
        }, 800);

        function showControls() {
            heroControls.classList.remove('opacity-0', 'pointer-events-none');
            heroControls.classList.add('opacity-100');
            heroControls.style.pointerEvents = 'auto';
            setTimeout(() => { subtitle.classList.remove('opacity-0', 'translate-y-4'); subtitle.classList.add('opacity-100', 'translate-y-0'); }, 50);
            setTimeout(() => { btnPrimary.classList.remove('opacity-0', 'translate-y-6'); btnPrimary.classList.add('opacity-100', 'translate-y-0'); }, 250);
            setTimeout(() => { btnSecondary.classList.remove('opacity-0', 'translate-y-6'); btnSecondary.classList.add('opacity-100', 'translate-y-0'); }, 450);
            setTimeout(() => {
                scrollHint.classList.remove('opacity-0', 'translate-y-2'); scrollHint.classList.add('opacity-100', 'translate-y-0');
                freezeScroll = false;
                document.body.style.overflow = '';
                document.body.style.touchAction = '';
            }, 650);
        }
    }

    /* =========================================
       HORIZONTAL SCROLL LOGIC
       ========================================= */
    const horizScrollContainer = document.getElementById('horizontal-scroll-container');
    const horizWrapper = document.getElementById('horizontal-scroll-wrapper');
    const horizProgress = document.getElementById('horizontal-scroll-progress');

    if (horizScrollContainer && horizWrapper && horizProgress) {
        const cards = horizWrapper.querySelectorAll('.category-card');
        const cardContents = horizWrapper.querySelectorAll('.card-content');
        const cardImages = horizWrapper.querySelectorAll('.card-image');

        const totalWidth = horizWrapper.scrollWidth - window.innerWidth;

        gsap.set(cardContents, { y: 50, opacity: 0 });
        gsap.set(cardImages, { scale: 1.2 });

        const scrollTween = gsap.to(horizWrapper, {
            x: -totalWidth,
            ease: "none",
            id: "horizontalScroll",
            scrollTrigger: {
                trigger: horizScrollContainer,
                start: "top top",
                end: () => `+=${totalWidth}`,
                pin: true,
                scrub: 0.8,
                anticipatePin: 1,
                invalidateOnRefresh: true,
                onUpdate: (self) => {
                    horizProgress.style.transform = `scaleX(${self.progress})`;
                }
            }
        });

        cards.forEach((card, index) => {
            const content = cardContents[index];
            const image = cardImages[index];

            gsap.to(content, {
                y: 0,
                opacity: 1,
                duration: 0.8,
                ease: "power2.out",
                scrollTrigger: {
                    trigger: card,
                    start: "left 80%",
                    end: "left 40%",
                    scrub: 0.5,
                    containerAnimation: scrollTween,
                }
            });

            gsap.to(image, {
                scale: 1,
                duration: 0.8,
                ease: "power2.out",
                scrollTrigger: {
                    trigger: card,
                    start: "left 90%",
                    end: "left 50%",
                    scrub: 0.5,
                    containerAnimation: scrollTween,
                }
            });
        });

        gsap.to(horizScrollContainer.querySelector('.section-title'), {
            xPercent: -30,
            ease: "none",
            scrollTrigger: {
                trigger: horizScrollContainer,
                start: "top top",
                end: () => `+=${totalWidth}`,
                scrub: 1,
            }
        });
    }

    /* =========================================
       IMAGE REVEAL LOGIC
       ========================================= */
    const imgRevealContainer = document.getElementById('image-reveal-container');
    if (imgRevealContainer) {
        const textContainer = document.getElementById('image-reveal-text');
        const imageContainer = document.getElementById('image-reveal-wrapper');

        const words = textContainer?.querySelectorAll('.word');
        if (words && words.length > 0) {
            gsap.set(words, { opacity: 0.15, y: 15 });
            gsap.to(words, {
                opacity: 1, y: 0, duration: 0.6, stagger: 0.08, ease: "power2.out",
                scrollTrigger: {
                    trigger: textContainer,
                    start: "top 70%",
                    end: "center center",
                    toggleActions: "play none none reverse",
                }
            });
        }

        const pieces = imageContainer?.querySelectorAll('.reveal-piece');
        if (pieces && pieces.length > 0) {
            gsap.set(pieces, { scaleY: 1 });
            gsap.to(pieces, {
                scaleY: 0, duration: 0.8, stagger: 0.1, ease: "power2.inOut",
                scrollTrigger: {
                    trigger: imageContainer,
                    start: "top 60%",
                    toggleActions: "play none none reverse",
                }
            });
        }

        const statElements = imgRevealContainer.querySelectorAll('.stat-number');
        statElements.forEach((stat) => {
            const targetValue = parseInt(stat.getAttribute('data-target') || '0');
            ScrollTrigger.create({
                trigger: stat, start: "top 85%", once: true,
                onEnter: () => {
                    const counter = { value: 0 };
                    gsap.to(counter, {
                        value: targetValue, duration: 2, ease: "power2.out",
                        onUpdate: () => { stat.textContent = Math.floor(counter.value).toString(); }
                    });
                }
            });
        });

        const decorElements = imgRevealContainer.querySelectorAll('.decor-element');
        if (decorElements && decorElements.length > 0) {
            gsap.fromTo(decorElements,
                { opacity: 0, scale: 0.8 },
                {
                    opacity: 1, scale: 1, duration: 1, stagger: 0.2, ease: "power2.out",
                    scrollTrigger: {
                        trigger: imgRevealContainer, start: "top 60%", toggleActions: "play none none reverse",
                    }
                }
            );
        }
    }

    /* =========================================
       FEATURED PRODUCTS LOGIC
       ========================================= */
    const featuredContainer = document.getElementById('featured-products-container');
    if (featuredContainer) {
        const cards = featuredContainer.querySelectorAll('.product-card');

        ScrollTrigger.create({
            trigger: featuredContainer,
            start: "top top",
            end: `+=${window.innerHeight * 2}`,
            pin: true,
            pinSpacing: true,
            scrub: 0.5,
            onUpdate: (self) => {
                const progress = self.progress;
                const numCards = cards.length;

                cards.forEach((card, i) => {
                    const cardStart = i / numCards;
                    const cardEnd = (i + 1) / numCards;

                    if (progress >= cardStart) {
                        const cardProgress = Math.min((progress - cardStart) / (cardEnd - cardStart), 1);
                        gsap.to(card, {
                            opacity: cardProgress,
                            y: 100 - (cardProgress * 100),
                            rotateX: 15 - (cardProgress * 15),
                            duration: 0.1,
                            overwrite: true
                        });
                    }
                });
            }
        });

        gsap.to('.featured-title', {
            y: 0, opacity: 1, clipPath: 'inset(0% 0 0 0)',
            duration: 1, stagger: 0.1, ease: "power4.out",
            scrollTrigger: {
                trigger: featuredContainer, start: "top 80%", end: "top 50%", scrub: 1,
            }
        });
    }

    /* =========================================
       VIDEO SHOWCASE LOGIC
       ========================================= */
    const videoContainer = document.getElementById('video-showcase-container');
    if (videoContainer) {
        const wrapper = document.getElementById('video-wrapper');
        const textContainer = document.getElementById('video-text-container');
        const videoElt = document.getElementById('showcase-video');
        const playBtn = document.getElementById('video-play-btn');
        const muteBtn = document.getElementById('video-mute-btn');
        const iconPause = document.getElementById('video-icon-pause');
        const iconPlay = document.getElementById('video-icon-play');
        const iconMuted = document.getElementById('video-icon-muted');
        const iconUnmuted = document.getElementById('video-icon-unmuted');

        gsap.to(wrapper, {
            scale: 1, borderRadius: '0px', opacity: 1, ease: "power2.out",
            scrollTrigger: { trigger: videoContainer, start: "top 80%", end: "top 10%", scrub: 0.5 }
        });

        const textLines = textContainer?.querySelectorAll('.video-text');
        if (textLines) {
            ScrollTrigger.create({
                trigger: textContainer, start: "top 70%",
                onEnter: () => {
                    gsap.to(textLines, {
                        y: 0, opacity: 1, rotateX: 0, duration: 1, stagger: 0.15, ease: "power4.out"
                    });
                }
            });
        }

        gsap.to('.video-main-title', {
            yPercent: -30,
            scrollTrigger: { trigger: videoContainer, start: "top top", end: "bottom top", scrub: 1 }
        });

        let isPlaying = true;
        let isMuted = true;

        if (playBtn) playBtn.addEventListener('click', () => {
            if (isPlaying) {
                videoElt.pause();
                iconPause.classList.add('hidden');
                iconPlay.classList.remove('hidden');
            } else {
                videoElt.play();
                iconPause.classList.remove('hidden');
                iconPlay.classList.add('hidden');
            }
            isPlaying = !isPlaying;
        });

        if (muteBtn) muteBtn.addEventListener('click', () => {
            videoElt.muted = !isMuted;
            isMuted = !isMuted;
            if (isMuted) {
                iconMuted.classList.remove('hidden');
                iconUnmuted.classList.add('hidden');
            } else {
                iconMuted.classList.add('hidden');
                iconUnmuted.classList.remove('hidden');
            }
        });
    }

    /* =========================================
       TEXT MARQUEE LOGIC
       ========================================= */
    const marqueeContainer = document.getElementById('text-marquee-container');
    if (marqueeContainer) {
        const r1 = document.getElementById('marquee-row-1');
        const r2 = document.getElementById('marquee-row-2');
        const r3 = document.getElementById('marquee-row-3');

        const scrollDistance = window.innerHeight * 2;

        gsap.to(r1, { xPercent: -40, ease: "none", scrollTrigger: { trigger: marqueeContainer, start: "top bottom", end: `+=${scrollDistance}`, scrub: 0.5 } });
        gsap.to(r2, { xPercent: 40, ease: "none", scrollTrigger: { trigger: marqueeContainer, start: "top bottom", end: `+=${scrollDistance}`, scrub: 0.5 } });
        gsap.to(r3, { xPercent: -30, ease: "none", scrollTrigger: { trigger: marqueeContainer, start: "top bottom", end: `+=${scrollDistance}`, scrub: 0.5 } });

        gsap.to(marqueeContainer, {
            opacity: 1,
            scrollTrigger: { trigger: marqueeContainer, start: "top 90%", end: "top 50%", scrub: 0.5 }
        });
    }

    /* =========================================
       SPLIT SCREEN LOGIC
       ========================================= */
    const splitContainer = document.getElementById('split-screen-container');
    if (splitContainer) {
        const leftPanel = document.getElementById('split-left-panel');
        const rightPanel = document.getElementById('split-right-panel');

        gsap.to(leftPanel, {
            y: "0%", opacity: 1, duration: 1,
            scrollTrigger: { trigger: splitContainer, start: "top 70%", end: "top 20%", scrub: 1 }
        });

        gsap.to(rightPanel, {
            y: "0%", opacity: 1, duration: 1,
            scrollTrigger: { trigger: splitContainer, start: "top 70%", end: "top 20%", scrub: 1 }
        });

        const parallaxImgs = splitContainer.querySelectorAll('.split-parallax-img');
        parallaxImgs.forEach(img => {
            gsap.to(img, {
                yPercent: -20,
                scrollTrigger: { trigger: img, start: "top bottom", end: "bottom top", scrub: 1 }
            });
        });
    }

    /* =========================================
       NEWSLETTER LOGIC
       ========================================= */
    const newsletterContainer = document.getElementById('newsletter-container');
    if (newsletterContainer) {
        const elements = document.querySelectorAll('#newsletter-content > *');

        if (elements.length > 0) {
            gsap.to(elements, {
                y: 0, translate: 0, opacity: 1, duration: 0.8, stagger: 0.15,
                scrollTrigger: { trigger: newsletterContainer, start: "top 70%" }
            });
        }

        gsap.to('#newsletter-bg-text', {
            xPercent: -10,
            scrollTrigger: { trigger: newsletterContainer, start: "top bottom", end: "bottom top", scrub: 1 }
        });

        const form = document.getElementById('newsletter-form');
        const successMsg = document.getElementById('newsletter-success');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const mail = document.getElementById('newsletter-email').value;
                if (mail) {
                    form.classList.add('hidden');
                    successMsg.classList.remove('hidden');
                    successMsg.classList.add('block');
                }
            });
        }
    }

    /* =========================================
       ABOUT PAGE LOGIC
       ========================================= */
    const aboutContainer = document.getElementById('about-container');
    if (aboutContainer) {
        const heroTl = gsap.timeline({ defaults: { ease: "power4.out" } });
        heroTl.to('.hero-text', { y: 0, opacity: 1, skewY: 0, duration: 1.2, stagger: 0.15 });

        gsap.to('.parallax-hero', {
            yPercent: 30,
            scrollTrigger: { trigger: '.hero-image-section', start: "top bottom", end: "bottom top", scrub: 1 }
        });

        gsap.to('.story-content > *', {
            y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: "power3.out",
            scrollTrigger: { trigger: '.story-section', start: "top 70%" }
        });

        gsap.to('.story-image', {
            scale: 1, opacity: 1, duration: 1.2, ease: "power3.out",
            scrollTrigger: { trigger: '.story-section', start: "top 70%" }
        });

        const statsSection = document.querySelector('.stats-section');
        if (statsSection) {
            ScrollTrigger.create({
                trigger: '.stats-section',
                start: "top 75%",
                onEnter: () => {
                    const duration = 2000;
                    const start = Date.now();
                    const targets = { clients: 50, designs: 500, countries: 25, years: 8 };

                    const animate = () => {
                        const elapsed = Date.now() - start;
                        const progress = Math.min(elapsed / duration, 1);
                        const eased = 1 - Math.pow(1 - progress, 3);

                        document.getElementById('stat-clients').textContent = Math.round(targets.clients * eased);
                        document.getElementById('stat-designs').textContent = Math.round(targets.designs * eased);
                        document.getElementById('stat-countries').textContent = Math.round(targets.countries * eased);
                        document.getElementById('stat-years').textContent = Math.round(targets.years * eased);

                        if (progress < 1) requestAnimationFrame(animate);
                    };
                    animate();
                }
            });

            gsap.to('.stat-item', {
                y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: "power3.out",
                scrollTrigger: { trigger: '.stats-section', start: "top 80%" }
            });
        }

        gsap.to('.value-card', {
            y: 0, opacity: 1, rotateY: 0, duration: 0.8, stagger: 0.15, ease: "power3.out",
            scrollTrigger: { trigger: '.values-section', start: "top 70%" }
        });

        gsap.to('.team-member', {
            y: 0, opacity: 1, duration: 0.8, stagger: 0.2, ease: "power3.out",
            scrollTrigger: { trigger: '.team-section', start: "top 70%" }
        });

        gsap.to('.cta-content > *', {
            y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: "power3.out",
            scrollTrigger: { trigger: '.cta-section', start: "top 80%" }
        });
    }

    /* =========================================
       NUEVO PAGE LOGIC
       ========================================= */
    const nuevoContainer = document.getElementById('nuevo-container');
    if (nuevoContainer) {
        gsap.to('.nuevo-hero-text', {
            y: 0, opacity: 1, skewY: 0, duration: 1, stagger: 0.1, ease: "power3.out"
        });

        gsap.to('.nuevo-product', {
            y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: "power3.out",
            scrollTrigger: { trigger: '#nuevo-products-grid', start: "top 85%" }
        });

        gsap.to('#nuevo-hero-image', {
            yPercent: 20, ease: "none",
            scrollTrigger: { trigger: '#nuevo-hero', start: "top top", end: "bottom top", scrub: true }
        });
    }

    /* =========================================
       CATALOGO PAGE LOGIC
       ========================================= */
    const catalogoContainer = document.getElementById('catalogo-container');
    if (catalogoContainer) {
        gsap.to('.catalog-hero-bg', {
            yPercent: 30,
            scrollTrigger: { trigger: '#catalogo-hero', start: "top top", end: "bottom top", scrub: 1 }
        });

        const heroTl = gsap.timeline({ defaults: { ease: "power4.out" } });
        heroTl.to('.catalog-hero-line', {
            y: 0, opacity: 1, skewY: 0, duration: 1, stagger: 0.1
        });

        gsap.fromTo('.category-btn',
            { y: 30, opacity: 0 },
            {
                y: 0, opacity: 1, duration: 0.6, stagger: 0.05, ease: "power3.out",
                scrollTrigger: { trigger: '.categories-section', start: "top 85%" }
            }
        );

        const categoryBtns = document.querySelectorAll('.category-btn');
        const items = document.querySelectorAll('.catalog-item');
        const catalogVisibleCount = document.getElementById('catalog-visible-count');
        const catalogProductCount = document.getElementById('catalog-product-count');
        const emptyState = document.getElementById('catalog-empty-state');
        const endMessage = document.getElementById('catalog-end-message');
        const sortSelect = document.getElementById('sort-select');
        const productsContainer = document.getElementById('catalog-products-container');

        let currentCategory = 'all';

        function updateCatalog() {
            let visibleCount = 0;
            const sortVal = sortSelect.value;
            let itemsArr = Array.from(items);

            itemsArr.sort((a, b) => {
                if (sortVal === 'price-asc') return parseFloat(a.dataset.price) - parseFloat(b.dataset.price);
                if (sortVal === 'price-desc') return parseFloat(b.dataset.price) - parseFloat(a.dataset.price);
                if (sortVal === 'newest') return parseInt(b.dataset.new) - parseInt(a.dataset.new);
                return parseInt(b.dataset.featured) - parseInt(a.dataset.featured);
            });

            itemsArr.forEach(item => productsContainer.appendChild(item));

            itemsArr.forEach(item => {
                if (currentCategory === 'all' || item.dataset.category === currentCategory) {
                    item.style.display = 'block';
                    visibleCount++;
                } else {
                    item.style.display = 'none';
                }
            });

            const visibleItems = Array.from(items).filter(item => item.style.display !== 'none');
            gsap.fromTo(visibleItems,
                { y: 40, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.5, stagger: 0.04, ease: "power2.out" }
            );

            catalogVisibleCount.textContent = visibleCount;
            catalogProductCount.textContent = visibleCount;

            if (visibleCount === 0) {
                emptyState.classList.remove('hidden');
                endMessage.classList.add('hidden');
            } else {
                emptyState.classList.add('hidden');
                endMessage.classList.remove('hidden');
            }
        }

        categoryBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                categoryBtns.forEach(b => {
                    b.classList.remove('text-primary-foreground');
                    b.classList.add('text-muted-foreground');
                    b.querySelector('.category-bg').classList.remove('scale-x-100');
                    b.querySelector('.category-bg').classList.add('scale-x-0');
                    b.querySelector('.category-indicator').classList.add('hidden');
                });
                btn.classList.add('text-primary-foreground');
                btn.classList.remove('text-muted-foreground');
                btn.querySelector('.category-bg').classList.add('scale-x-100');
                btn.querySelector('.category-bg').classList.remove('scale-x-0');
                btn.querySelector('.category-indicator').classList.remove('hidden');

                currentCategory = btn.dataset.category;
                updateCatalog();
            });
        });

        sortSelect.addEventListener('change', updateCatalog);

        const gridNormalBtn = document.getElementById('grid-normal-btn');
        const gridLargeBtn = document.getElementById('grid-large-btn');

        gridNormalBtn.addEventListener('click', () => {
            productsContainer.className = "products-container grid gap-6 md:gap-8 grid-cols-2 md:grid-cols-3 lg:grid-cols-4";
            gridNormalBtn.className = "p-2 rounded transition-colors bg-background text-primary";
            gridLargeBtn.className = "p-2 rounded transition-colors text-muted-foreground hover:text-foreground";
        });

        gridLargeBtn.addEventListener('click', () => {
            productsContainer.className = "products-container grid gap-6 md:gap-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3";
            gridLargeBtn.className = "p-2 rounded transition-colors bg-background text-primary";
            gridNormalBtn.className = "p-2 rounded transition-colors text-muted-foreground hover:text-foreground";
        });
    }

    /* =========================================
       PRODUCTO LOGIC
       ========================================= */
    const productoContainer = document.getElementById('producto-container');
    if (productoContainer) {
        gsap.to('.producto-image',
            { scale: 1, opacity: 1, duration: 1, ease: "power3.out" }
        );

        gsap.to('.producto-info > div', {
            y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: "power2.out", delay: 0.3
        });

        const mainImage = document.getElementById('main-product-image');
        const thumbBtns = document.querySelectorAll('.thumb-btn');
        thumbBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                mainImage.src = btn.dataset.src;
                thumbBtns.forEach(b => {
                    b.classList.remove('ring-2', 'ring-primary');
                    b.classList.add('opacity-60');
                });
                btn.classList.add('ring-2', 'ring-primary');
                btn.classList.remove('opacity-60');
            });
        });

        let selectedColorVal = document.getElementById('selected-color-label').textContent;
        const colorBtns = document.querySelectorAll('.color-btn');
        colorBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                colorBtns.forEach(b => {
                    b.className = "color-btn px-4 py-2 text-sm border transition-all border-border hover:border-foreground";
                });
                btn.className = "color-btn px-4 py-2 text-sm border transition-all border-primary bg-primary/10 text-primary";
                selectedColorVal = btn.dataset.color;
                document.getElementById('selected-color-label').textContent = selectedColorVal;
            });
        });

        let selectedSizeVal = null;
        const sizeBtns = document.querySelectorAll('.size-btn');
        const addToCartProductBtn = document.getElementById('btn-add-to-cart-product');
        const formTalla = document.getElementById('form-talla');
        sizeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                sizeBtns.forEach(b => {
                    b.className = "size-btn w-12 h-12 text-sm border transition-all border-border hover:border-foreground";
                });
                btn.className = "size-btn w-12 h-12 text-sm border transition-all border-primary bg-primary text-primary-foreground";
                selectedSizeVal = btn.dataset.size;
                document.getElementById('selected-size-label').textContent = selectedSizeVal;
                if (formTalla) formTalla.value = selectedSizeVal;

                // Enable the submit button now that a size is selected
                addToCartProductBtn.disabled = false;
                addToCartProductBtn.className = "w-full py-4 font-[var(--font-display)] text-xl tracking-[0.2em] flex items-center justify-center gap-3 transition-all bg-primary text-primary-foreground hover:bg-primary/90";
            });
        });

        let quantityVal = 1;
        const qtyMinus = document.getElementById('qty-minus');
        const qtyPlus = document.getElementById('qty-plus');
        const qtyValue = document.getElementById('qty-value');
        const formCantidad = document.getElementById('form-cantidad');

        qtyMinus.addEventListener('click', () => {
            quantityVal = Math.max(1, quantityVal - 1);
            qtyValue.textContent = quantityVal;
            if (formCantidad) formCantidad.value = quantityVal;
        });

        qtyPlus.addEventListener('click', () => {
            const currentTotal = parseInt(document.getElementById('cart-total-items-header')?.textContent || '0');
            if (currentTotal + quantityVal + 1 > 100) {
                showToast('Límite de 100 productos alcanzado.', 'warning');
                return;
            }
            quantityVal++;
            qtyValue.textContent = quantityVal;
            if (formCantidad) formCantidad.value = quantityVal;
        });

        const addToCartForm = document.getElementById('add-to-cart-form');
        if (addToCartForm) {
            addToCartForm.addEventListener('submit', (e) => {
                const currentTotal = parseInt(document.getElementById('cart-total-items-header')?.textContent || '0');
                if (currentTotal + quantityVal > 100) {
                    e.preventDefault();
                    showToast('No puedes agregar más de 100 productos al carrito.', 'error');
                }
            });
        }
    }

    /* =========================================
       CARRITO PAGE LOGIC
       ========================================= */
    const carritoContainer = document.getElementById('carrito-container');
    if (carritoContainer) {
        gsap.to('#cart-header-content, #cart-page-empty, #cart-page-content', {
            y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: "power2.out"
        });
    }
});