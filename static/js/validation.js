/* validation.js — client-side form validation for all auth pages */

const rules = {
  name: {
    test: v => v.trim().length >= 2,
    msg:  'Name must be at least 2 characters.'
  },
  email: {
    test: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()),
    msg:  'Enter a valid email address.'
  },
  password: {
    test: v => v.length >= 8,
    msg:  'Password must be at least 8 characters.'
  },
  confirm_password: {
    test: (v, form) => v === form.querySelector('[name="password"]')?.value,
    msg:  'Passwords do not match.'
  }
};

// ── Password strength ──────────────────────────────────────────────────────
function getStrength(pwd) {
  let score = 0;
  if (pwd.length >= 8)                    score++;
  if (/[A-Z]/.test(pwd))                 score++;
  if (/[0-9]/.test(pwd))                 score++;
  if (/[^A-Za-z0-9]/.test(pwd))          score++;
  return score; // 0–4
}

const strengthColors = ['#f87171', '#fbbf24', '#fbbf24', '#4ade80', '#4ade80'];

function updateStrengthBar(pwd, bar) {
  const score = getStrength(pwd);
  const segments = bar.querySelectorAll('.strength-segment');
  segments.forEach((seg, i) => {
    seg.style.background = i < score ? strengthColors[score] : 'var(--border)';
  });
}

// ── Field validation ───────────────────────────────────────────────────────
function validateField(input, form) {
  const name = input.name;
  const rule = rules[name];
  if (!rule) return true;

  const isValid = rule.test(input.value, form);
  const errEl   = input.closest('.form-group')?.querySelector('.field-error');

  input.classList.toggle('valid',   isValid);
  input.classList.toggle('invalid', !isValid);

  if (errEl) {
    errEl.textContent = isValid ? '' : rule.msg;
    errEl.classList.toggle('show', !isValid);
  }
  return isValid;
}

// ── Init on DOMContentLoaded ───────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

  // Password visibility toggle
  document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.closest('.input-wrap').querySelector('input');
      const isText = input.type === 'text';
      input.type = isText ? 'password' : 'text';
      btn.textContent = isText ? '👁️' : '🙈';
    });
  });

  // Strength bar
  const pwdInput  = document.querySelector('[name="password"]');
  const strengthBar = document.querySelector('.strength-bar');

  if (pwdInput && strengthBar) {
    pwdInput.addEventListener('input', () => {
      updateStrengthBar(pwdInput.value, strengthBar);
    });
  }

  // Real-time field validation
  document.querySelectorAll('input[name]').forEach(input => {
    const form = input.closest('form');
    input.addEventListener('blur',  () => validateField(input, form));
    input.addEventListener('input', () => {
      if (input.classList.contains('invalid')) validateField(input, form);
    });
  });

  // Form submit validation
  document.querySelectorAll('form[data-validate]').forEach(form => {
    form.addEventListener('submit', e => {
      let valid = true;
      form.querySelectorAll('input[name]').forEach(input => {
        if (!validateField(input, form)) valid = false;
      });
      if (!valid) {
        e.preventDefault();
        // Shake the submit button
        const btn = form.querySelector('.btn-primary');
        if (btn) {
          btn.style.animation = 'shake 0.4s ease';
          btn.addEventListener('animationend', () => btn.style.animation = '', { once: true });
        }
      }
    });
  });
});

// CSS shake keyframe injected via JS (avoids extra CSS file dependency)
const style = document.createElement('style');
style.textContent = `
  @keyframes shake {
    0%,100% { transform: translateX(0); }
    20%      { transform: translateX(-6px); }
    40%      { transform: translateX(6px); }
    60%      { transform: translateX(-4px); }
    80%      { transform: translateX(4px); }
  }
`;
document.head.appendChild(style);