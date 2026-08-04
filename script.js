(function () {
  'use strict';

  const nav = document.getElementById('nav');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  const contactForm = document.getElementById('contactForm');

  const BLOG_PREVIEW = [
    { slug: 'owning-google-us', title: 'The Day I Legally Owned google.us for a Short Time' },
    { slug: 'agentic-ai-in-india', title: 'My Vision for the Future of Agentic AI in India' },
    { slug: 'microservices-on-azure-aks', title: 'Microservices Architecture on Azure Kubernetes Service' },
    { slug: 'linux-fundamentals', title: 'Linux Fundamentals: The Foundation Every Cloud Engineer Needs' },
  ];

  function getBlogArticleHref(slug) {
    const segments = window.location.pathname.split('/').filter(Boolean);
    const blogIndex = segments.indexOf('blog');

    if (blogIndex === -1) {
      return `blog/${slug}/index.html`;
    }

    if (segments.length > blogIndex + 1) {
      return `../${slug}/index.html`;
    }

    return `${slug}/index.html`;
  }

  function initBlogNav() {
    if (!navLinks) return;

    const blogLink = Array.from(navLinks.querySelectorAll('a')).find((link) => {
      const text = link.textContent.trim();
      const href = link.getAttribute('href') || '';
      return text === 'Blog' && (href.includes('blog') || href.endsWith('index.html'));
    });

    if (!blogLink || blogLink.closest('.nav__blog-item')) return;

    const listItem = blogLink.parentElement;
    listItem.classList.add('nav__blog-item');
    blogLink.classList.add('nav__blog-link');

    const tooltip = document.createElement('div');
    tooltip.className = 'nav__blog-tooltip';
    tooltip.setAttribute('role', 'tooltip');

    const tooltipTitle = document.createElement('p');
    tooltipTitle.className = 'nav__blog-tooltip-title';
    tooltipTitle.textContent = 'Latest articles';

    const tooltipList = document.createElement('ul');
    tooltipList.className = 'nav__blog-tooltip-list';

    BLOG_PREVIEW.forEach((article) => {
      const item = document.createElement('li');
      const articleLink = document.createElement('a');
      articleLink.href = getBlogArticleHref(article.slug);
      articleLink.textContent = article.title;
      item.appendChild(articleLink);
      tooltipList.appendChild(item);
    });

    tooltip.appendChild(tooltipTitle);
    tooltip.appendChild(tooltipList);
    listItem.appendChild(tooltip);

    blogLink.setAttribute('aria-describedby', 'nav-blog-tooltip');
    tooltip.id = 'nav-blog-tooltip';

    initBlogTooltipAutoShow(listItem);
  }

  function initBlogTooltipAutoShow(listItem) {
    const TOOLTIP_CYCLE_MS = 6000;
    const TOOLTIP_DISPLAY_MS = 4500;
    const isDesktop = () => window.matchMedia('(min-width: 769px)').matches;
    const prefersReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!isDesktop() || prefersReducedMotion()) return;

    let hideTimeout;
    let userEngaged = false;

    const setTooltipOpen = (open) => {
      listItem.classList.toggle('nav__blog-item--tooltip-open', open);
    };

    const isEngaged = () => userEngaged || listItem.matches(':hover') || listItem.contains(document.activeElement);

    const showTooltip = () => {
      if (!isDesktop() || document.hidden || isEngaged()) return;

      setTooltipOpen(true);
      clearTimeout(hideTimeout);
      hideTimeout = setTimeout(() => {
        if (!isEngaged()) setTooltipOpen(false);
      }, TOOLTIP_DISPLAY_MS);
    };

    const intervalId = window.setInterval(showTooltip, TOOLTIP_CYCLE_MS);
    const initialTimeout = window.setTimeout(showTooltip, TOOLTIP_CYCLE_MS);

    listItem.addEventListener('mouseenter', () => {
      userEngaged = true;
      clearTimeout(hideTimeout);
    });

    listItem.addEventListener('mouseleave', () => {
      userEngaged = false;
      if (!listItem.contains(document.activeElement)) {
        setTooltipOpen(false);
      }
    });

    listItem.addEventListener('focusin', () => {
      userEngaged = true;
      clearTimeout(hideTimeout);
    });

    listItem.addEventListener('focusout', () => {
      userEngaged = false;
      if (!listItem.matches(':hover')) {
        setTooltipOpen(false);
      }
    });

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) setTooltipOpen(false);
    });

    window.addEventListener('beforeunload', () => {
      clearInterval(intervalId);
      clearTimeout(initialTimeout);
      clearTimeout(hideTimeout);
    });
  }

  initBlogNav();

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
    const FORMSUBMIT_KEY = 'e91a6b67557e276576cf2b7d588d8fec';

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
        const response = await fetch(`https://formsubmit.co/ajax/${FORMSUBMIT_KEY}`, {
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
