import React, { useState } from 'react';

/**
 * Modern Medium-style Story Editor
 * @param {{
 *   onSubmit: (postData: { title: string, content: string }) => Promise<void>,
 *   isSubmitting: boolean,
 *   isOpen?: boolean,
 *   onToggleOpen?: () => void
 * }} props
 */
export default function PostForm({
  onSubmit,
  isSubmitting = false,
  isOpen = false,
  onToggleOpen,
  currentUser = null,
}) {
  const [internalOpen, setInternalOpen] = useState(false);
  const isExpanded = onToggleOpen ? isOpen : internalOpen;
  const toggle = onToggleOpen || (() => setInternalOpen((prev) => !prev));

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [formError, setFormError] = useState('');

  const charCount = content.trim().length;

  let lengthStatus = 'neutral';
  let lengthHint = 'Minimum 50 characters required for AI publication approval.';

  if (charCount > 0 && charCount < 50) {
    lengthStatus = 'warning';
    lengthHint = `Add ${50 - charCount} more characters for moderation readiness.`;
  } else if (charCount >= 50 && charCount <= 2000) {
    lengthStatus = 'success';
    lengthHint = `Ready for AI review (${charCount} characters).`;
  } else if (charCount > 2000) {
    lengthStatus = 'danger';
    lengthHint = `Exceeds 2,000 char threshold (${charCount}/2000).`;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');

    const trimmedTitle = title.trim();
    const trimmedContent = content.trim();

    if (!trimmedTitle) {
      setFormError('Please enter a story title.');
      return;
    }

    if (trimmedTitle.length > 200) {
      setFormError('Title must not exceed 200 characters.');
      return;
    }

    if (!trimmedContent) {
      setFormError('Please write your story content.');
      return;
    }

    try {
      await onSubmit({ title: trimmedTitle, content: trimmedContent });
      setTitle('');
      setContent('');
      if (onToggleOpen) {
        onToggleOpen();
      } else {
        setInternalOpen(false);
      }
    } catch (err) {
      const errorMsg =
        err?.response?.data?.detail || err?.message || 'Failed to publish draft.';
      setFormError(errorMsg);
    }
  };

  return (
    <div className={`medium-editor-container ${isExpanded ? 'is-open' : ''}`}>
      {!isExpanded ? (
        <div className="medium-editor-collapsed" onClick={toggle} role="button" tabIndex={0}>
          <span className="editor-collapsed-placeholder">
            What's on your mind? Write a new story...
          </span>
          <button type="button" className="medium-write-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 20h9"></path>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
            </svg>
            Write Story
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="medium-editor-card">
          <div className="medium-editor-topbar">
            <div className="editor-author-meta">
              <div className="editor-author-avatar">
                {currentUser?.username ? currentUser.username[0].toUpperCase() : 'M'}
              </div>
              <div>
                <span className="editor-author-name">
                  {currentUser?.username ? `@${currentUser.username}` : 'Draft Story'}
                </span>
                <span className="editor-guideline-badge status-badge">{lengthHint}</span>
              </div>
            </div>
            <button
              type="button"
              className="medium-close-btn"
              onClick={toggle}
              title="Close editor"
              aria-label="Close"
            >
              ✕
            </button>
          </div>

          {formError && <div className="form-alert-error">{formError}</div>}

          <div className="medium-input-group">
            <input
              id="post-title"
              type="text"
              className="medium-title-input"
              placeholder="Title"
              value={title}
              maxLength={200}
              onChange={(e) => setTitle(e.target.value)}
              disabled={isSubmitting}
              autoFocus
              required
            />
            <span className="medium-char-indicator">{title.trim().length}/200</span>
          </div>

          <div className="medium-textarea-group">
            <textarea
              id="post-content"
              rows={8}
              className="medium-body-textarea"
              placeholder="Tell your story... Write your ideas, tech insights, or editorial opinion."
              value={content}
              maxLength={10000}
              onChange={(e) => setContent(e.target.value)}
              disabled={isSubmitting}
              required
            />
          </div>

          <div className="medium-editor-bottombar">
            <div className="medium-stats-preview">
              <span className={`stats-pill-counter length-${lengthStatus}`}>
                {charCount} characters · ~{Math.max(1, Math.ceil(charCount / 800))} min read
              </span>
            </div>

            <div className="medium-editor-actions">
              <button
                type="button"
                className="btn-medium-ghost"
                onClick={() => {
                  setTitle('');
                  setContent('');
                  toggle();
                }}
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn-medium-publish"
                disabled={isSubmitting || !title.trim() || !content.trim()}
              >
                {isSubmitting ? 'Saving Story...' : 'Save Draft'}
              </button>
            </div>
          </div>
        </form>
      )}
    </div>
  );
}
