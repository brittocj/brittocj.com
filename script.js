(function () {
  'use strict';

  const nav = document.getElementById('nav');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  const contactForm = document.getElementById('contactForm');

  const BLOG_PREVIEW = [
    { slug: 'entropy-eternal-energy', title: 'Entropy and Eternal Energy: A Thermodynamic Necessity for One Transcendent God' },
    { slug: 'devops-ready-reckoner', title: 'DevOps Ready Reckoner: Essential Cheat Sheets' },
    { slug: 'owning-google-us', title: 'The Day I Legally Owned google.us for a Short Time' },
    { slug: 'agentic-ai-in-india', title: 'My Vision for the Future of Agentic AI in India' },
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

  function isOnBlogPage() {
    return window.location.pathname.split('/').filter(Boolean).includes('blog');
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

    const boardLabel = blogLink.textContent.trim();
    blogLink.textContent = '';

    const swing = document.createElement('div');
    swing.className = 'nav__blog-sign-swing';

    const peg = document.createElement('span');
    peg.className = 'nav__blog-sign-peg';
    peg.setAttribute('aria-hidden', 'true');

    const board = document.createElement('span');
    board.className = 'nav__blog-sign-board';
    board.textContent = boardLabel;

    blogLink.appendChild(board);
    swing.appendChild(peg);
    swing.appendChild(blogLink);
    listItem.insertBefore(swing, listItem.firstChild);

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
      articleLink.innerHTML = article.title.replace(
        /google\.us/g,
        '<span class="google-us-gradient">google.us</span>'
      );
      item.appendChild(articleLink);
      tooltipList.appendChild(item);
    });

    tooltip.appendChild(tooltipTitle);
    tooltip.appendChild(tooltipList);
    listItem.appendChild(tooltip);

    blogLink.setAttribute('aria-describedby', 'nav-blog-tooltip');
    tooltip.id = 'nav-blog-tooltip';

    if (!isOnBlogPage()) {
      initBlogTooltipIntro(listItem);
    }
  }

  function initBlogTooltipIntro(listItem) {
    const TOOLTIP_DISPLAY_MS = 4500;
    const isDesktop = () => window.matchMedia('(min-width: 769px)').matches;
    const prefersReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!isDesktop() || prefersReducedMotion() || isOnBlogPage()) return;

    let hideTimeout;
    let leaveTimeout;

    const setTooltipOpen = (open) => {
      listItem.classList.toggle('nav__blog-item--tooltip-open', open);
    };

    const isEngaged = () => listItem.matches(':hover') || listItem.contains(document.activeElement);

    const showTooltipOnce = () => {
      if (!isDesktop() || document.hidden || isEngaged()) return;

      setTooltipOpen(true);
      hideTimeout = window.setTimeout(() => {
        if (!isEngaged()) setTooltipOpen(false);
      }, TOOLTIP_DISPLAY_MS);
    };

    window.setTimeout(showTooltipOnce, 800);

    listItem.addEventListener('mouseenter', () => {
      clearTimeout(hideTimeout);
      clearTimeout(leaveTimeout);
    });

    listItem.addEventListener('mouseleave', () => {
      clearTimeout(leaveTimeout);
      leaveTimeout = window.setTimeout(() => {
        if (!listItem.contains(document.activeElement)) {
          setTooltipOpen(false);
        }
      }, 200);
    });

    listItem.addEventListener('focusout', () => {
      if (!listItem.matches(':hover')) {
        setTooltipOpen(false);
      }
    });

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        clearTimeout(hideTimeout);
        setTooltipOpen(false);
      }
    });
  }

  initBlogNav();

  function initBlogSearch() {
    const searchInput = document.getElementById('blogSearch');
    const searchClear = document.getElementById('blogSearchClear');
    const searchStatus = document.getElementById('blogSearchStatus');
    const blogGrid = document.getElementById('blogGrid');
    const blogEmpty = document.getElementById('blogEmpty');

    if (!searchInput || !blogGrid) return;

    const cards = Array.from(blogGrid.querySelectorAll('.blog-card'));

    const filterCards = (query) => {
      const normalized = query.trim().toLowerCase();
      let visibleCount = 0;

      cards.forEach((card) => {
        const matches = !normalized || card.textContent.toLowerCase().includes(normalized);
        card.classList.toggle('blog-card--hidden', !matches);
        if (matches) visibleCount += 1;
      });

      const hasQuery = normalized.length > 0;
      if (searchClear) searchClear.hidden = !hasQuery;

      if (blogEmpty) {
        blogEmpty.hidden = !hasQuery || visibleCount > 0;
      }

      if (!hasQuery) {
        searchStatus.textContent = '';
      } else if (visibleCount === 0) {
        searchStatus.textContent = 'No matching articles';
      } else if (visibleCount === 1) {
        searchStatus.textContent = '1 article found';
      } else {
        searchStatus.textContent = `${visibleCount} articles found`;
      }
    };

    const setQuery = (query, { updateUrl = true } = {}) => {
      searchInput.value = query;
      filterCards(query);

      if (!updateUrl) return;

      const url = new URL(window.location.href);
      const trimmed = query.trim();
      if (trimmed) {
        url.searchParams.set('q', trimmed);
      } else {
        url.searchParams.delete('q');
      }
      window.history.replaceState({}, '', url);
    };

    searchInput.addEventListener('input', () => setQuery(searchInput.value));

    if (searchClear) {
      searchClear.addEventListener('click', () => {
        setQuery('');
        searchInput.focus();
      });
    }

    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        setQuery('');
        searchInput.blur();
      }
    });

    const initialQuery = new URLSearchParams(window.location.search).get('q');
    if (initialQuery) {
      setQuery(initialQuery, { updateUrl: false });
    }
  }

  initBlogSearch();

  function initBlogJumpTop() {
    const blogPost = document.querySelector('.blog-post');
    if (!blogPost) return;

    const jumpTop = document.createElement('a');
    jumpTop.href = '#';
    jumpTop.className = 'blog-jump-top';
    jumpTop.id = 'blogJumpTop';
    jumpTop.hidden = true;
    jumpTop.setAttribute('aria-label', 'Jump to top');
    jumpTop.innerHTML = `
      <span class="blog-jump-top__icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 19V5"></path>
          <path d="M5 12l7-7 7 7"></path>
        </svg>
      </span>
      <span>Top</span>
    `;
    document.body.appendChild(jumpTop);

    const scrollThreshold = 400;

    const updateJumpTop = () => {
      jumpTop.hidden = window.scrollY < scrollThreshold;
    };

    jumpTop.addEventListener('click', (event) => {
      event.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    window.addEventListener('scroll', updateJumpTop, { passive: true });
    updateJumpTop();
  }

  initBlogJumpTop();

  const BLOG_VIEWS_API = '/api/views';

  function formatViewCount(count) {
    if (count >= 1000000) {
      return `${(count / 1000000).toFixed(1).replace(/\.0$/, '')}M`;
    }
    if (count >= 1000) {
      return `${(count / 1000).toFixed(1).replace(/\.0$/, '')}k`;
    }
    return String(count);
  }

  function getBlogPostSlug() {
    const segments = window.location.pathname.split('/').filter(Boolean);
    const blogIndex = segments.indexOf('blog');

    if (blogIndex === -1 || segments.length <= blogIndex + 1) {
      return null;
    }

    const slug = segments[blogIndex + 1].replace(/\.html$/, '');

    if (!slug || slug === 'index') {
      return null;
    }

    return /^[a-z0-9-]+$/.test(slug) ? slug : null;
  }

  function isBlogIndexPage() {
    return Boolean(document.getElementById('blogGrid'));
  }

  async function fetchViewCount(slug) {
    const response = await fetch(`${BLOG_VIEWS_API}?slug=${encodeURIComponent(slug)}`, {
      headers: { Accept: 'application/json' },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch view count.');
    }

    const data = await response.json();
    return data.count;
  }

  async function fetchViewCounts(slugs) {
    if (!slugs.length) {
      return {};
    }

    const response = await fetch(`${BLOG_VIEWS_API}?slugs=${encodeURIComponent(slugs.join(','))}`, {
      headers: { Accept: 'application/json' },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch view counts.');
    }

    const data = await response.json();
    return data.counts || {};
  }

  async function recordView(slug) {
    const response = await fetch(BLOG_VIEWS_API, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ slug }),
    });

    if (!response.ok) {
      throw new Error('Failed to record view.');
    }

    const data = await response.json();
    return data.count;
  }

  function setViewCountText(element, count) {
    const target = element.querySelector('[data-view-count]') || element;
    target.textContent = formatViewCount(count);
  }

  async function initBlogPostViews(slug) {
    const meta = document.querySelector('.blog-meta');
    if (!meta) return;

    const viewsItem = document.createElement('div');
    viewsItem.className = 'blog-meta-item blog-meta-views';
    viewsItem.innerHTML = '👁 <span class="blog-view-count" data-view-count>-</span> views';
    meta.appendChild(viewsItem);

    const sessionKey = `blog-viewed-${slug}`;

    try {
      const count = sessionStorage.getItem(sessionKey)
        ? await fetchViewCount(slug)
        : await recordView(slug);

      setViewCountText(viewsItem, count);
      sessionStorage.setItem(sessionKey, '1');
    } catch {
      viewsItem.remove();
    }
  }

  async function initBlogIndexViews() {
    const cards = document.querySelectorAll('#blogGrid .blog-card');
    const slugMap = new Map();

    cards.forEach((card) => {
      const href = card.getAttribute('href') || '';
      const match = href.match(/^([a-z0-9-]+)\/index\.html$/);

      if (!match) return;

      const slug = match[1];
      slugMap.set(slug, card);
    });

    if (!slugMap.size) return;

    try {
      const counts = await fetchViewCounts([...slugMap.keys()]);

      slugMap.forEach((card, slug) => {
        const meta = card.querySelector('.blog-card-meta');
        const readtime = card.querySelector('.blog-card-readtime');

        if (!meta || !readtime || counts[slug] === undefined) return;

        const endGroup = document.createElement('div');
        endGroup.className = 'blog-card-meta-end';

        const views = document.createElement('span');
        views.className = 'blog-card-views';
        views.innerHTML = `👁 <span data-view-count>${formatViewCount(counts[slug])}</span>`;

        readtime.remove();
        endGroup.appendChild(views);
        endGroup.appendChild(readtime);
        meta.appendChild(endGroup);
      });
    } catch {
      // Views API unavailable - leave cards unchanged.
    }
  }

  async function initBlogViews() {
    const slug = getBlogPostSlug();

    if (slug) {
      await initBlogPostViews(slug);
      return;
    }

    if (isBlogIndexPage()) {
      await initBlogIndexViews();
    }
  }

  initBlogViews();

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

  // Contact form - sends message to brits@brittocj.com via FormSubmit
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
