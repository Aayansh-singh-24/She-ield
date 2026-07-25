/**
 * toast.js
 * ─────────────────────────────────────────────────────────────
 * Lightweight toast notification system.
 * Types: 'success' | 'error' | 'warn' | 'info'
 */

'use strict';

window.SafeHer = window.SafeHer || {};

window.SafeHer.Toast = (() => {

  const ICONS = {
    success: '✅',
    error:   '❌',
    warn:    '⚠️',
    info:    'ℹ️',
  };

  /**
   * Show a toast notification.
   *
   * @param {string} message
   * @param {'success'|'error'|'warn'|'info'} [type='info']
   * @param {number} [duration]  ms — 0 = sticky
   */
  function show(message, type = 'info', duration) {
    const cfg      = window.SafeHer.CONFIG;
    const ms       = duration ?? cfg.TOAST_DURATION;
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast--${type}`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
      <span class="toast-icon" aria-hidden="true">${ICONS[type] ?? ICONS.info}</span>
      <span class="toast-msg">${_escape(message)}</span>
    `;

    container.appendChild(toast);

    if (ms > 0) {
      setTimeout(() => _dismiss(toast), ms);
    }

    return toast;
  }

  function _dismiss(toast) {
    toast.classList.add('toast-out');
    toast.addEventListener('animationend', () => toast.remove(), { once: true });
    // Fallback in case animationend never fires
    setTimeout(() => toast.remove(), 600);
  }

  /** Basic HTML escape to prevent XSS in toast messages */
  function _escape(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  return { show };

})();
