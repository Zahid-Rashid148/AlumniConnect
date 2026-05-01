// ═══════════════════════════════════════════════════════════
// AlumniConnect® — Main JS
// ═══════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {

  // ── Page Loader ──────────────────────────────────────────
  const loader = document.getElementById('page-loader');
  if (loader) {
    window.addEventListener('load', () => {
      setTimeout(() => loader.classList.add('hidden'), 500);
    });
    // Fallback
    setTimeout(() => loader.classList.add('hidden'), 2500);
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

    // Auto-resize textarea
    const textarea = document.querySelector('.message-input');
    if (textarea) {
      textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
      });

      // Send on Ctrl+Enter
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

  // ── Notification Read ─────────────────────────────────────
  document.querySelectorAll('[data-mark-read]').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.getAttribute('data-mark-read');
      fetch(`/notifications/${id}/read/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
      });
    });
  });

  // ── Confirm Delete ────────────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      if (!confirm(el.getAttribute('data-confirm'))) e.preventDefault();
    });
  });

  // ── Skills Input Tag UI ───────────────────────────────────
  const skillsInput = document.querySelector('input[name="skills"]');
  if (skillsInput) {
    skillsInput.addEventListener('input', () => {
      const preview = document.getElementById('skills-preview');
      if (!preview) return;
      preview.innerHTML = skillsInput.value
        .split(',')
        .filter(s => s.trim())
        .map(s => `<span class="skill-tag">${s.trim()}</span>`)
        .join('');
    });
  }

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

  // ── Mobile nav toggle class ───────────────────────────────
  const toggler = document.querySelector('.navbar-toggler');
  if (toggler) {
    toggler.addEventListener('click', () => {
      document.querySelector('.navbar-collapse')?.classList.toggle('show');
    });
  }

  // ── Password Visibility Toggle ────────────────────────────
  window.togglePassword = function(inputId, iconElement) {
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
