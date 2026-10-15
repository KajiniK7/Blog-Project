import React from 'react';

/**
 * Notification banner component for feedback and error alerts.
 * @param {{
 *   notification: { type: 'success' | 'error' | 'warning' | 'info', title?: string, message: string, reasons?: string[] } | null,
 *   onClose: () => void
 * }} props
 */
export default function Notification({ notification, onClose }) {
  if (!notification) return null;

  const { type = 'info', title, message, reasons = [] } = notification;

  // Icon characters for each type
  const iconMap = {
    success: '✓',
    error:   '✕',
    warning: '⚠',
    info:    'i',
  };

  const icon = iconMap[type] || 'i';

  return (
    <div
      className={`notification-banner notification-${type}`}
      role="alert"
      aria-live="assertive"
    >
      <div className="notification-icon" aria-hidden="true">
        {icon}
      </div>
      <div className="notification-body">
        {title && <div className="notification-title">{title}</div>}
        <div className="notification-message">{message}</div>
        {reasons && reasons.length > 0 && (
          <div className="notification-reasons">
            <span className="reasons-heading">Violations Detected</span>
            <ul>
              {reasons.map((reason, idx) => (
                <li key={idx}>{reason}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
      <button
        type="button"
        className="notification-close"
        onClick={onClose}
        aria-label="Dismiss notification"
      >
        ×
      </button>
    </div>
  );
}
