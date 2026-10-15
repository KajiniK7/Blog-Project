import React, { useState } from 'react';

/**
 * Medium-Style Article Story Card
 * Now supports editing EXCLUSIVELY for draft posts!
 */
export default function PostCard({
  post,
  currentUser = null,
  onSubmitForReview,
  onPublish,
  onEditPost,
  onViewPost,
  isSubmitting = false,
  isPublishing = false,
}) {
  const { id, title, content, status, flagged_reasons, created_at } = post;

  // ── Inline edit state (allowed EXCLUSIVELY for draft posts) ────────────────
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(title);
  const [editContent, setEditContent] = useState(content);
  const [editError, setEditError] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  const charCount = editContent.trim().length;

  let lengthStatus = 'neutral';
  let lengthHint = '50–2000 chars required for review';
  if (charCount > 0 && charCount < 50) {
    lengthStatus = 'warning';
    lengthHint = `Too short (${charCount}/50 chars)`;
  } else if (charCount >= 50 && charCount <= 2000) {
    lengthStatus = 'success';
    lengthHint = `Optimal length (${charCount} chars)`;
  } else if (charCount > 2000) {
    lengthStatus = 'danger';
    lengthHint = `Too long (${charCount}/2000 chars)`;
  }

  const openEdit = () => {
    setEditTitle(title);
    setEditContent(content);
    setEditError('');
    setIsEditing(true);
  };

  const cancelEdit = () => {
    setIsEditing(false);
    setEditError('');
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setEditError('');

    const trimmedTitle = editTitle.trim();
    const trimmedContent = editContent.trim();

    if (!trimmedTitle) {
      setEditError('Title cannot be empty.');
      return;
    }
    if (trimmedTitle.length > 200) {
      setEditError('Title must not exceed 200 characters.');
      return;
    }
    if (!trimmedContent) {
      setEditError('Content cannot be empty.');
      return;
    }

    setIsSaving(true);
    try {
      if (onEditPost) {
        await onEditPost(id, { title: trimmedTitle, content: trimmedContent });
      }
      setIsEditing(false);
    } catch {
      setEditError('Failed to save changes. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  // Formatting & Byline info (Date + Created Time)
  const formattedDateTime = created_at
    ? `${new Date(created_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
      })} at ${new Date(created_at).toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      })}`
    : 'Recent';

  const wordCount = content.split(/\s+/).filter(Boolean).length;
  const readTime = Math.max(1, Math.ceil(wordCount / 180));

  const isPublished = status === 'published';
  const isApproved  = status === 'approved';
  const isFlagged   = status === 'flagged';
  const isDraft     = status === 'draft';

  const statusBadgeConfig = {
    draft:     { label: 'Draft',     className: 'tag-draft' },
    flagged:   { label: 'Flagged',   className: 'tag-flagged' },
    approved:  { label: 'Approved',  className: 'tag-approved' },
    published: { label: 'Published', className: 'tag-published' },
  }[status] || { label: status, className: 'tag-draft' };

  // Medium story preview text
  const previewText =
    content.length > 180 ? `${content.substring(0, 180)}…` : content;

  // Author display name: always show author who created it
  const authorName = post.author_username
    ? `@${post.author_username}`
    : post.username
    ? `@${post.username}`
    : (currentUser?.username ? `@${currentUser.username}` : 'Author');
  const authorInitial = authorName.replace(/^@/, '')[0]?.toUpperCase() || 'M';

  return (
    <article className={`medium-post-story status-${status}`} aria-label={`Story #${id}: ${title}`}>
      {/* ── EDIT MODE (Only when post is a draft) ─────────────────────────── */}
      {isEditing && isDraft ? (
        <form className="medium-story-edit-form" onSubmit={handleSave}>
          <div className="medium-edit-alert">
            <span className="edit-alert-icon">✏️</span>
            <div>
              <strong>Editing Saved Draft</strong>
              <p>Update your story's title or body. Once saved, submit it to AI review when ready.</p>
            </div>
          </div>

          {editError && <div className="form-alert-error">{editError}</div>}

          <div className="edit-field-group">
            <input
              type="text"
              className="medium-edit-title-input"
              value={editTitle}
              maxLength={200}
              onChange={(e) => setEditTitle(e.target.value)}
              disabled={isSaving}
              autoFocus
              required
            />
          </div>

          <div className="edit-field-group">
            <textarea
              rows={8}
              className="medium-edit-content-textarea"
              value={editContent}
              maxLength={10000}
              onChange={(e) => setEditContent(e.target.value)}
              disabled={isSaving}
              required
            />
            <div className="edit-char-bar">
              <span className={`counter-text length-${lengthStatus}`}>
                {charCount} chars · {lengthHint}
              </span>
            </div>
          </div>

          <div className="edit-actions-row">
            <button
              type="button"
              className="btn-medium-ghost"
              onClick={cancelEdit}
              disabled={isSaving}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-medium-save"
              disabled={isSaving || !editTitle.trim() || !editContent.trim()}
            >
              {isSaving ? 'Saving...' : 'Save Draft'}
            </button>
          </div>
        </form>
      ) : (
        /* ── NORMAL STORY CARD VIEW ─────────────────────────────────────── */
        <div className="medium-story-card-inner">
          <div className="medium-story-main">
            {/* Author Byline */}
            <div className="medium-byline">
              <div className="author-avatar">{authorInitial}</div>
              <div className="byline-details">
                <span className="author-name">{authorName}</span>
                <span className="byline-dot">·</span>
                <time className="post-date">{formattedDateTime}</time>
                <span className="byline-dot">·</span>
                <span className={`medium-status-tag ${statusBadgeConfig.className}`}>
                  {statusBadgeConfig.label}
                </span>
                <span className="story-id">#{id}</span>
              </div>
            </div>

            {/* Headline and Preview */}
            <div
              className="medium-story-content"
              onClick={() => onViewPost(post)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => e.key === 'Enter' && onViewPost(post)}
            >
              <h2 className="medium-story-title">{title}</h2>
              <p className="medium-story-snippet">{previewText}</p>
            </div>

            {/* Moderation Flags Notice (if flagged) */}
            {isFlagged && flagged_reasons && flagged_reasons.length > 0 && (
              <div className="medium-flags-callout" role="alert">
                <div className="flags-callout-header">
                  <span className="flags-icon">⚠️</span>
                  <span className="flags-title">Flagged by Moderation ({flagged_reasons.length})</span>
                </div>
                <ul className="flags-list">
                  {flagged_reasons.map((reason, idx) => (
                    <li key={idx}>{reason}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Bottom Meta & Action Bar */}
            <div className="medium-story-footer">
              <div className="footer-meta-left">
                <span className="reading-time">{readTime} min read</span>
                <span className="meta-dot">·</span>
                <span className="char-count">{content.length} characters</span>
              </div>

              <div className="footer-actions-right">
                {/* Read full post */}
                <button
                  type="button"
                  className="medium-btn-text"
                  onClick={() => onViewPost(post)}
                >
                  Read
                </button>

                {/* ✏️ EDIT BUTTON — Only displayed if post is a saved DRAFT! */}
                {isDraft && (
                  <button
                    type="button"
                    className="medium-btn-edit"
                    onClick={openEdit}
                    title="Edit draft content"
                  >
                    Edit Draft
                  </button>
                )}

                {/* Submit for Review (Draft only) */}
                {isDraft && (
                  <button
                    type="button"
                    className="medium-btn-submit"
                    onClick={() => onSubmitForReview(id)}
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Reviewing...' : 'Review'}
                  </button>
                )}

                {/* Publish Article (Approved only) */}
                {isApproved && (
                  <button
                    type="button"
                    className="medium-btn-publish"
                    onClick={() => onPublish(id)}
                    disabled={isPublishing}
                  >
                    {isPublishing ? 'Publishing...' : 'Publish'}
                  </button>
                )}

                {/* Flagged Status Label (read only, no edit) */}
                {isFlagged && (
                  <span className="medium-locked-indicator" style={{ color: '#b91c1c' }}>
                    ⚠️ Flagged
                  </span>
                )}

                {/* Published Immutable Badge */}
                {isPublished && (
                  <span className="medium-locked-indicator" title="Published posts cannot be edited.">
                    🔒 Published
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </article>
  );
}
