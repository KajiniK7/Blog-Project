import React from 'react';
import PostCard from './PostCard';

/**
 * Medium-Style Stories Feed Container
 */
export default function PostList({
  posts = [],
  currentUser = null,
  isLoading = false,
  currentFilter = 'all',
  searchQuery = '',
  onClearSearch,
  onSubmitForReview,
  onPublish,
  onEditPost,
  onViewPost,
  submittingId = null,
  publishingId = null,
  onResetFilter,
}) {
  if (isLoading && posts.length === 0) {
    return (
      <div className="medium-feed-loading">
        <div className="medium-skeleton-card">
          <div className="skeleton-avatar" />
          <div className="skeleton-line skeleton-title" />
          <div className="skeleton-line skeleton-body" />
          <div className="skeleton-line skeleton-body short" />
        </div>
        <div className="medium-skeleton-card">
          <div className="skeleton-avatar" />
          <div className="skeleton-line skeleton-title" />
          <div className="skeleton-line skeleton-body" />
          <div className="skeleton-line skeleton-body short" />
        </div>
      </div>
    );
  }

  if (posts.length === 0) {
    if (searchQuery.trim()) {
      return (
        <div className="medium-empty-state">
          <div className="empty-symbol">🔍</div>
          <h3 className="empty-headline">
            No stories matching "{searchQuery}"
          </h3>
          <p className="empty-description">
            We couldn't find any articles with titles matching your search query. Try another keyword or clear search.
          </p>
          {onClearSearch && (
            <button
              type="button"
              className="btn-medium-outline"
              onClick={onClearSearch}
            >
              Clear search
            </button>
          )}
        </div>
      );
    }

    const getEmptyHeadline = () => {
      if (currentFilter === 'all') return 'No stories from other writers yet';
      if (currentFilter === 'my_posts') return "You haven't created any posts yet";
      return `No ${currentFilter} stories yet`;
    };

    const getEmptyDescription = () => {
      if (currentFilter === 'all') {
        return 'Check back soon to see stories and perspectives shared by other authors across the community.';
      }
      if (currentFilter === 'my_posts') {
        return 'Start writing to build your personal catalog of drafts and published articles.';
      }
      return `There are currently no articles in the "${currentFilter}" category.`;
    };

    return (
      <div className="medium-empty-state">
        <div className="empty-symbol">✍️</div>
        <h3 className="empty-headline">
          {getEmptyHeadline()}
        </h3>
        <p className="empty-description">
          {getEmptyDescription()}
        </p>
        {currentFilter !== 'all' && (
          <button
            type="button"
            className="btn-medium-outline"
            onClick={onResetFilter}
          >
            Explore all stories
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="medium-stories-feed">
      {posts.map((post) => (
        <PostCard
          key={post.id}
          post={post}
          currentUser={currentUser}
          onSubmitForReview={onSubmitForReview}
          onPublish={onPublish}
          onEditPost={onEditPost}
          onViewPost={onViewPost}
          isSubmitting={submittingId === post.id}
          isPublishing={publishingId === post.id}
        />
      ))}
    </div>
  );
}
