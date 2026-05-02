// ═══════════════════════════════════════════════════════════
// AlumniConnect® — Main JS
// ═══════════════════════════════════════════════════════════

/* ═══════════════════════════════════════════════════════════
   THEME MANAGEMENT SYSTEM
   ═══════════════════════════════════════════════════════════ */
const themeManager = {
  init() {
    const savedTheme = localStorage.getItem('theme') ||
      (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
    this.applyTheme(savedTheme, false);

    // Listen for system changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (!localStorage.getItem('theme')) {
        this.applyTheme(e.matches ? 'dark' : 'light', true);
      }
    });
  },

  applyTheme(theme, animate) {
    if (animate) {
      document.body.classList.add('theme-transition-active');
      setTimeout(() => {
        document.documentElement.setAttribute('data-theme', theme);
        document.body.classList.remove('theme-transition-active');
      }, 300);
    } else {
      document.documentElement.setAttribute('data-theme', theme);
    }
    localStorage.setItem('theme', theme);
  },

  toggle() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    this.applyTheme(newTheme, true);
  }
};

/* ═══════════════════════════════════════════════════════════
   FIRE & SPARK ENGINE (CANVAS)
   ═══════════════════════════════════════════════════════════ */
const fireEngine = {
  canvas: null,
  ctx: null,
  particles: [],
  maxParticles: 120,

  init() {
    this.canvas = document.getElementById('fire-canvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.resize();
    window.addEventListener('resize', () => this.resize());
    this.animate();
  },

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  },

  createParticle() {
    return {
      x: Math.random() * this.canvas.width,
      y: this.canvas.height + 10,
      size: Math.random() * 2 + 1,
      speedY: Math.random() * -1.5 - 0.5,
      speedX: Math.random() * 2 - 1,
      opacity: Math.random() * 0.5 + 0.5,
      color: Math.random() > 0.5 ? '#f0b429' : '#ffffff'
    };
  },

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    if (this.particles.length < this.maxParticles) {
      this.particles.push(this.createParticle());
    }

    for (let i = 0; i < this.particles.length; i++) {
      let p = this.particles[i];
      p.y += p.speedY;
      p.x += p.speedX;
      p.opacity -= 0.003;

      if (p.opacity <= 0 || p.y < -10) {
        this.particles[i] = this.createParticle();
      }

      this.ctx.globalAlpha = p.opacity;
      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      this.ctx.fill();
    }

    requestAnimationFrame(() => this.animate());
  }
};

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Theme & Fire
  themeManager.init();
  fireEngine.init();

  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => themeManager.toggle());
  }

  // ── Page Loader ──────────────────────────────────────────
  const loader = document.getElementById('page-loader');
  if (loader) {
    if (sessionStorage.getItem('loaderShown')) {
      loader.remove();
    } else {
      window.addEventListener('load', () => {
        setTimeout(() => {
          loader.classList.add('hidden');
          sessionStorage.setItem('loaderShown', 'true');
        }, 2500);
      });
      setTimeout(() => {
        loader.classList.add('hidden');
        sessionStorage.setItem('loaderShown', 'true');
      }, 4500);
    }
  }

  // ── Navbar Scroll Effect ─────────────────────────────────
  const navbar = document.querySelector('.navbar-glass');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  // ── Auto-dismiss Alerts ──────────────────────────────────
  document.querySelectorAll('.alert-glass').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-8px)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

  // ── Smooth Scroll for Anchor Links ───────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Intersection Observer for Rise Animations ─────────────
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animationPlayState = 'running';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.glass-card, .stat-card, .user-card, .post-card').forEach(el => {
    el.style.animationPlayState = 'paused';
    observer.observe(el);
  });

  // ── Chat Auto-scroll ─────────────────────────────────────
  const chatMessages = document.getElementById('chat-messages');
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
    const textarea = document.querySelector('.message-input');
    if (textarea) {
      textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
      });
      textarea.addEventListener('keydown', e => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
          const form = textarea.closest('form');
          if (form) form.submit();
        }
      });
    }
  }

  // ── Hero Counter Animation ────────────────────────────────
  const counters = document.querySelectorAll('.hero-stat-number[data-target]');
  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-target'));
        const suffix = el.getAttribute('data-suffix') || '';
        let current = 0;
        const step = Math.ceil(target / 40);
        const timer = setInterval(() => {
          current = Math.min(current + step, target);
          el.textContent = current.toLocaleString() + suffix;
          if (current >= target) clearInterval(timer);
        }, 30);
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(c => counterObserver.observe(c));

  // ── CSRF Cookie Helper ────────────────────────────────────
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      for (const cookie of document.cookie.split(';')) {
        const c = cookie.trim();
        if (c.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(c.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // ── Password Visibility Toggle ────────────────────────────
  window.togglePassword = function (inputId, iconElement) {
    const input = document.getElementById(inputId);
    if (input) {
      if (input.type === 'password') {
        input.type = 'text';
        iconElement.classList.replace('bi-eye', 'bi-eye-slash');
      } else {
        input.type = 'password';
        iconElement.classList.replace('bi-eye-slash', 'bi-eye');
      }
    }
  };
});
