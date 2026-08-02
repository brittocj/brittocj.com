(function () {
  'use strict';

  const nav = document.getElementById('nav');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  const contactForm = document.getElementById('contactForm');

  // Sticky nav background on scroll
  window.addEventListener('scroll', () => {
    nav.classList.toggle('nav--scrolled', window.scrollY > 40);
  });

  // Mobile nav toggle
  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    navToggle.classList.toggle('active');
  });

  // Close mobile nav on link click
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      navToggle.classList.remove('active');
    });
  });

  // Active nav link highlighting
  const sections = document.querySelectorAll('section[id], header[id]');
  const navItems = navLinks.querySelectorAll('a[href^="#"]');

  const observerOptions = {
    root: null,
    rootMargin: '-40% 0px -55% 0px',
    threshold: 0
  };

  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navItems.forEach(item => {
          item.classList.toggle('active', item.getAttribute('href') === `#${id}`);
        });
      }
    });
  }, observerOptions);

  sections.forEach(section => sectionObserver.observe(section));

  // Fade-in animation on scroll
  const fadeElements = document.querySelectorAll(
    '.expertise__card, .timeline__item, .project__card, .about__highlights, .certs__section, .skills__category'
  );

  fadeElements.forEach(el => el.classList.add('fade-in'));

  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  fadeElements.forEach(el => fadeObserver.observe(el));

  // Contact form — sends message to brits@brittocj.com via FormSubmit
  if (contactForm) {
    const formStatus = document.getElementById('formStatus');
    const formSubmit = document.getElementById('formSubmit');
    const defaultButtonText = formSubmit.textContent;
    const CONTACT_EMAIL = 'brits@brittocj.com';

    const setFormStatus = (message, type) => {
      formStatus.textContent = message;
      formStatus.className = `form__status form__status--${type}`;
      formStatus.hidden = false;
    };

    const clearFormStatus = () => {
      formStatus.textContent = '';
      formStatus.className = 'form__status';
      formStatus.hidden = true;
    };

    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      clearFormStatus();

      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const message = document.getElementById('message').value.trim();

      formSubmit.disabled = true;
      formSubmit.textContent = 'Sending…';

      const formData = new FormData(contactForm);
      formData.set('name', name);
      formData.set('email', email);
      formData.set('message', message);
      formData.set('_subject', `Portfolio Contact from ${name}`);
      formData.set('_captcha', 'false');
      formData.set('_template', 'table');

      try {
        const response = await fetch(`https://formsubmit.co/ajax/${CONTACT_EMAIL}`, {
          method: 'POST',
          body: formData,
          headers: { Accept: 'application/json' },
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
          throw new Error(data.message || 'Failed to send message.');
        }

        contactForm.reset();
        setFormStatus('Message sent! I\'ll get back to you soon.', 'success');
      } catch (err) {
        setFormStatus(
          err.message || 'Something went wrong. Please try again or email brits@brittocj.com directly.',
          'error'
        );
      } finally {
        formSubmit.disabled = false;
        formSubmit.textContent = defaultButtonText;
      }
    });
  }
})();
