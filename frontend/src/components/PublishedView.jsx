import React, { useEffect } from 'react';

/**
 * Medium-Style Full Story Reader Overlay
 */
export default function PublishedView({ post, onClose, currentUser = null }) {
  if (!post) return null;

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  const isPublished = post.status === 'published';
  const formattedDate = post.created_at
    ? `${new Date(post.created_at).toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric',
      })} at ${new Date(post.created_at).toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      })}`
    : 'Recently';

  const wordCount = post.content.split(/\s+/).filter(Boolean).length;
  const readTime = Math.max(1, Math.ceil(wordCount / 180));
  const authorName = post.author_username
    ? `@${post.author_username}`
    : post.username
    ? `@${post.username}`
    : (currentUser?.username ? `@${currentUser.username}` : 'Author');
  const authorInitial = authorName.replace(/^@/, '')[0]?.toUpperCase() || 'M';

  const statusLabel = {
    draft:     'Draft',
    flagged:   'Flagged',
    approved:  'Approved for Publishing',
    published: 'Published',
  }[post.status] || post.status;

  return (
    <div className="medium-reader-backdrop" onClick={onClose} role="dialog" aria-modal="true">
      <div className="medium-reader-container" onClick={(e) => e.stopPropagation()}>
        {/* Top Navbar */}
        <div className="medium-reader-header">
          <div className="reader-header-left">
            <span className="brand-dot">●</span>
            <span className="story-category-tag">{statusLabel}</span>
            {isPublished && <span className="reader-immutable-tag">🔒 Immutable</span>}
          </div>
          <button
            type="button"
            className="reader-close-btn"
            onClick={onClose}
            aria-label="Close story"
          >
            ✕
          </button>
        </div>

        {/* Article Body */}
        <article className="medium-article-body">
          <h1 className="medium-article-title">{post.title}</h1>

          {/* Author details */}
          <div className="medium-article-author-card">
            <div className="author-avatar large">{authorInitial}</div>
            <div className="author-meta-info">
              <span className="author-title-name">{authorName}</span>
              <div className="meta-subline">
                <span>{readTime} min read</span>
                <span className="meta-dot">·</span>
                <span>{formattedDate}</span>
                <span className="meta-dot">·</span>
                <span>Post #{post.id}</span>
              </div>
            </div>
          </div>

          <hr className="medium-article-rule" />

          {/* Flagged reasons callout if needed */}
          {post.status === 'flagged' &&
            post.flagged_reasons &&
            post.flagged_reasons.length > 0 && (
              <div className="medium-flags-callout in-reader">
                <div className="flags-callout-header">
                  <span className="flags-icon">⚠️</span>
                  <span className="flags-title">Moderation Flags</span>
                </div>
                <ul className="flags-list">
                  {post.flagged_reasons.map((reason, idx) => (
                    <li key={idx}>{reason}</li>
                  ))}
                </ul>
              </div>
            )}

          {/* Story Paragraphs */}
          <div className="medium-prose">
            {post.content.split('\n').map((paragraph, idx) =>
              paragraph.trim() ? (
                <p key={idx}>{paragraph}</p>
              ) : (
                <div key={idx} className="prose-spacing" />
              )
            )}
          </div>
        </article>
      </div>
    </div>
  );
}
