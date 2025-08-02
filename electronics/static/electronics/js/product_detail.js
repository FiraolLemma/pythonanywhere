document.addEventListener('DOMContentLoaded', function() {
  // ===== Image Zoom Effect =====
  const productImage = document.querySelector('.product-image');
  if (productImage) {
    productImage.addEventListener('click', function() {
      this.classList.toggle('zoomed');
    });
  }

  // ===== Button Ripple Effect =====
  const buttons = document.querySelectorAll('.btn');
  buttons.forEach(button => {
    button.addEventListener('click', function(e) {
      // Create ripple element
      const ripple = document.createElement('span');
      ripple.className = 'ripple-effect';
      
      // Position ripple
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      // Style ripple
      ripple.style.width = ripple.style.height = `${size}px`;
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      
      // Add ripple to button
      this.appendChild(ripple);
      
      // Remove ripple after animation
      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });

  // ===== Review Star Rating Animation =====
  const reviewStars = document.querySelectorAll('.review-stars i');
  reviewStars.forEach(star => {
    star.addEventListener('mouseenter', function() {
      this.style.transform = 'scale(1.2)';
      this.style.transition = 'transform 0.2s ease';
    });
    
    star.addEventListener('mouseleave', function() {
      this.style.transform = 'scale(1)';
    });
  });

  // ===== Smooth Scrolling for Anchor Links =====
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });

  // ===== Add to Cart Animation =====
  const buyButton = document.querySelector('.btn.primary');
  if (buyButton) {
    buyButton.addEventListener('click', function(e) {
      if (!this.classList.contains('adding')) {
        this.classList.add('adding');
        this.innerHTML = '<i class="bi bi-check-circle"></i> Added to Cart';
        
        setTimeout(() => {
          this.classList.remove('adding');
          this.innerHTML = '<i class="bi bi-cart-plus"></i> Buy Now';
        }, 2000);
      }
    });
  }
});
