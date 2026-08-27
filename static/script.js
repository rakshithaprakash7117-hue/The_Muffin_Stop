/**
 * THE MUFFIN STOP — Vanilla JavaScript Interactivity
 */
document.addEventListener('DOMContentLoaded', () => {

  // 1. Mobile Menu Drawer Toggle
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const navLinks = document.getElementById('navLinks');
  if (mobileMenuBtn && navLinks) {
    mobileMenuBtn.addEventListener('click', () => {
      navLinks.classList.toggle('show');
    });
  }
  // 2. Product Category Filter Tabs (muffins.html)
  const filterBtns = document.querySelectorAll('.filter-btn');
  const productCards = document.querySelectorAll('.product-card');
  if (filterBtns.length > 0 && productCards.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        // Update active class
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filterValue = btn.getAttribute('data-filter');
        productCards.forEach(card => {
          const category = card.getAttribute('data-category');
          if (filterValue === 'all' || category === filterValue) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }
  // 3. Product Quantity Increment / Decrement (muffin.html)
  const qtyMinus = document.getElementById('qtyMinus');
  const qtyPlus = document.getElementById('qtyPlus');
  const qtyInput = document.getElementById('qtyInput');
  if (qtyMinus && qtyPlus && qtyInput) {
    qtyMinus.addEventListener('click', () => {
      let val = parseInt(qtyInput.value, 10) || 1;
      if (val > 1) {
        qtyInput.value = val - 1;
      }
    });
    qtyPlus.addEventListener('click', () => {
      let val = parseInt(qtyInput.value, 10) || 1;
      if (val < 99) {
        qtyInput.value = val + 1;
      }
    });
  }
  // 4. Product Gallery Image Switcher (muffin.html)
  const mainImage = document.getElementById('mainProductImage');
  const thumbs = document.querySelectorAll('.thumb-img');
  if (mainImage && thumbs.length > 0) {
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        thumbs.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
        mainImage.src = thumb.src;
      });
    });
  }
  // 5. Cosmetic Add-to-Cart Toast Notification (muffin.html UI feedback)
  const addToCartBtn = document.getElementById('addToCartBtn');
  const toastNotification = document.getElementById('toastNotification');
  if (addToCartBtn && toastNotification) {
    addToCartBtn.addEventListener('click', (e) => {
      e.preventDefault(); // UI preview only
      toastNotification.classList.add('show');

      setTimeout(() => {
        toastNotification.classList.remove('show');
      }, 3500);
    });
  }
});
