/**
 * Main JavaScript logic for AXIS Streetwear
 * Built to replace React Context and State with Vanilla JS + GSAP
 */

// Basic State Management
const store = {
  cart: [],
  favorites: [],
  activeSection: "home",
  selectedProduct: null,
  isCartOpen: false,
  isProductModalOpen: false,
};

// Elements
const modalEls = {
  cart: document.getElementById('cart-drawer'),
  product: document.getElementById('product-modal'),
  cartOverlay: document.getElementById('cart-overlay'),
  productOverlay: document.getElementById('product-overlay')
};

// Utility Functions
function updateCartCount() {
  const count = store.cart.reduce((sum, item) => sum + item.quantity, 0);
  document.querySelectorAll('[data-cart-count]').forEach(el => {
    el.textContent = count;
    // Show/hide badge
    if(count > 0) el.classList.remove('hidden');
    else el.classList.add('hidden');
  });
}

function renderCart() {
  // To be implemented during template integration
  console.log('Rendering cart...', store.cart);
  updateCartCount();
}

// Actions
function toggleCart() {
  store.isCartOpen = !store.isCartOpen;
  if(store.isCartOpen) {
    modalEls.cart.classList.remove('translate-x-full');
    modalEls.cartOverlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  } else {
    modalEls.cart.classList.add('translate-x-full');
    modalEls.cartOverlay.classList.add('hidden');
    document.body.style.overflow = '';
  }
}

function addToCart(product, size, color) {
  const existing = store.cart.find(item => item.id === product.id && item.selectedSize === size);
  if (existing) {
    existing.quantity += 1;
  } else {
    store.cart.push({ ...product, quantity: 1, selectedSize: size, selectedColor: color });
  }
  renderCart();
  if(!store.isCartOpen) toggleCart();
}

function switchSection(section) {
  // Basic implementation to swap sections on main page (if it's a SPA-like experience)
  // Since we use Jinja, usually this would be handled by href links in the NavBar. 
  // But if the user wants single-page section switching:
  document.querySelectorAll('main > section[data-section]').forEach(el => {
    if(el.getAttribute('data-section') === section) {
      el.classList.remove('hidden');
    } else {
      el.classList.add('hidden');
    }
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Event Listeners initialization
document.addEventListener('DOMContentLoaded', () => {
  // GSAP Registration
  if(window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    initGSAPAnimations();
  }

  // Cart toggles
  document.querySelectorAll('[data-toggle-cart]').forEach(btn => {
    btn.addEventListener('click', toggleCart);
  });
  
  if(modalEls.cartOverlay) {
    modalEls.cartOverlay.addEventListener('click', toggleCart);
  }

  // Initial render
  updateCartCount();
});

// GSAP Animations (Replicated exactly from React implementation)
function initGSAPAnimations() {
  // -- HERO SECTION --
  const pinWrap = document.getElementById('hero-pin-wrap');
  if (pinWrap) {
    const videoWrap = document.getElementById('hero-video-wrap');
    const overlay = document.getElementById('hero-overlay');
    const title = document.getElementById('hero-title');
    const subtitleLine = document.getElementById('hero-subtitle-line');
    const tagline1 = document.getElementById('hero-tagline-1');
    const tagline2 = document.getElementById('hero-tagline-2');
    const tagline3 = document.getElementById('hero-tagline-3');
    const ctaBlock = document.getElementById('hero-cta-block');
    const scrollHint = document.getElementById('hero-scroll-hint');
    const lineTop = document.getElementById('hero-line-top');
    const lineBot = document.getElementById('hero-line-bot');
    const sideLeft = document.getElementById('hero-side-left');
    const sideRight = document.getElementById('hero-side-right');
    const cornerTL = document.getElementById('corner-tl');
    const cornerTR = document.getElementById('corner-tr');
    const cornerBL = document.getElementById('corner-bl');
    const cornerBR = document.getElementById('corner-br');
    const axisLetters = document.querySelectorAll('[data-axis-letter]');

    // Hide everything initially
    gsap.set(
      [title, subtitleLine, tagline1, tagline2, tagline3, ctaBlock, scrollHint, lineTop, lineBot, sideLeft, sideRight, cornerTL, cornerTR, cornerBL, cornerBR],
      { opacity: 0 }
    );

    // Quick intro (no scroll)
    const intro = gsap.timeline({ delay: 0.3 });
    intro
      .to(cornerTL, { opacity: 1, duration: 0.3 })
      .to(cornerTR, { opacity: 1, duration: 0.3 }, "<0.1")
      .to(cornerBL, { opacity: 1, duration: 0.3 }, "<0.1")
      .to(cornerBR, { opacity: 1, duration: 0.3 }, "<0.1")
      .to(scrollHint, { opacity: 1, duration: 0.5 }, "<0.2")
      .to(sideLeft, { opacity: 0.06, duration: 0.8 }, "<")
      .to(sideRight, { opacity: 0.06, duration: 0.8 }, "<0.1");

    // Scroll-driven pinned timeline
    const master = gsap.timeline({
      scrollTrigger: {
        trigger: pinWrap,
        start: "top top",
        end: "+=350%",
        pin: true,
        scrub: 0.8,
        anticipatePin: 1,
      },
    });

    // Phase 1
    master
      .fromTo(videoWrap, { clipPath: "circle(8% at 50% 50%)" }, { clipPath: "circle(75% at 50% 50%)", duration: 1, ease: "power2.inOut" }, 0)
      .fromTo(overlay, { opacity: 0.9 }, { opacity: 0.5, duration: 1 }, 0)
      .to(title, { opacity: 1, duration: 0.1 }, 0.15)
      .fromTo(axisLetters, { y: 120, opacity: 0, rotateX: -90, scale: 0.5 }, { y: 0, opacity: 1, rotateX: 0, scale: 1, duration: 0.5, stagger: 0.08, ease: "back.out(1.4)" }, 0.2)
      .fromTo(subtitleLine, { scaleX: 0, opacity: 0, transformOrigin: "center" }, { scaleX: 1, opacity: 1, duration: 0.4, ease: "power3.inOut" }, 0.6);

    // Phase 2
    master
      .fromTo(tagline1, { y: 80, opacity: 0, filter: "blur(10px)" }, { y: 0, opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "power3.out" }, 1.1)
      .fromTo(tagline2, { y: 80, opacity: 0, filter: "blur(10px)" }, { y: 0, opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "power3.out" }, 1.5)
      .fromTo(tagline3, { y: 80, opacity: 0, filter: "blur(10px)" }, { y: 0, opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "power3.out" }, 1.9)
      .fromTo(lineTop, { scaleX: 0, opacity: 0 }, { scaleX: 1, opacity: 1, duration: 0.5, ease: "power3.inOut" }, 1.3)
      .fromTo(lineBot, { scaleX: 0, opacity: 0 }, { scaleX: 1, opacity: 1, duration: 0.5, ease: "power3.inOut" }, 1.7);

    // Phase 3
    master.fromTo(ctaBlock, { y: 50, opacity: 0, scale: 0.9 }, { y: 0, opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 2.4);

    // Phase 4
    master
      .to(title, { scale: 3, opacity: 0, duration: 1, ease: "power2.in" }, 3)
      .to([subtitleLine, tagline1, tagline2, tagline3], { opacity: 0, y: -40, duration: 0.6, stagger: 0.05, ease: "power2.in" }, 3)
      .to([lineTop, lineBot], { scaleX: 3, opacity: 0, duration: 0.8 }, 3)
      .to(ctaBlock, { opacity: 0, y: -30, duration: 0.5 }, 3.1)
      .to([cornerTL, cornerTR, cornerBL, cornerBR], { opacity: 0, duration: 0.5 }, 3)
      .to(overlay, { opacity: 0.95, duration: 1 }, 3)
      .to(scrollHint, { opacity: 0, duration: 0.3 }, 3)
      .to(videoWrap, { scale: 1.15, duration: 1 }, 3);

    // Video Audio Mute functionality
    const videoBg = document.getElementById('hero-video');
    const muteBtn = document.getElementById('hero-mute-btn');
    const muteIconOn = document.getElementById('hero-mute-on');
    const muteIconOff = document.getElementById('hero-mute-off');
    
    if (muteBtn && videoBg) {
      muteBtn.addEventListener('click', () => {
        videoBg.muted = !videoBg.muted;
        if(videoBg.muted) {
          muteIconOff.classList.remove('hidden');
          muteIconOn.classList.add('hidden');
        } else {
          muteIconOff.classList.add('hidden');
          muteIconOn.classList.remove('hidden');
        }
      });
    }
  }

  // -- FEATURED SECTION --
  const featuredSection = document.getElementById('featured-section');
  if (featuredSection) {
    gsap.from("[data-feat-card]", {
      y: 80,
      opacity: 0,
      duration: 0.8,
      stagger: 0.15,
      ease: "power3.out",
      scrollTrigger: {
        trigger: featuredSection,
        start: "top 75%",
      },
    });
  }

  // -- URBAN BANNER --
  const bannerSection = document.getElementById('urban-banner');
  if (bannerSection) {
    gsap.from("[data-banner-text]", {
      y: 60,
      opacity: 0,
      duration: 1,
      stagger: 0.2,
      ease: "power3.out",
      scrollTrigger: {
        trigger: bannerSection,
        start: "top 70%",
      },
    });
  }

  // -- NEW ARRIVALS --
  const newSection = document.getElementById('new-arrivals');
  if (newSection) {
    gsap.from("[data-new-card]", {
      y: 80,
      opacity: 0,
      duration: 0.8,
      stagger: 0.15,
      ease: "power3.out",
      scrollTrigger: {
        trigger: newSection,
        start: "top 75%",
      },
    });
  }
}

// Export for global use in other scripts
window.axisStore = store;
window.updateCartCount = updateCartCount;
window.addToCart = addToCart;
window.toggleCart = toggleCart;
window.switchSection = switchSection;
