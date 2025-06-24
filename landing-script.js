// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// CTA button tracking
document.querySelector('.cta-button').addEventListener('click', function(e) {
    e.preventDefault();
    alert('Thank you for your interest! Sign up form would open here.');
});

// Price button handling
document.querySelectorAll('.price-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        alert(`You selected the ${this.closest('.price-card').querySelector('h3').textContent} plan!`);
    });
});

console.log('Landing page loaded! Built with ULTIMA AI.');