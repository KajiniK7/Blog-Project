import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  listPosts,
  createPost,
  submitPost,
  publishPost,
  updatePost,
} from './api/client';
import PostForm from './components/PostForm';
import PostList from './components/PostList';
import StatusFilter from './components/StatusFilter';
import Notification from './components/Notification';
import PublishedView from './components/PublishedView';
import AuthModal from './components/AuthModal';
import UserPostAnalytics from './components/UserPostAnalytics';

export default function App() {
  const [posts, setPosts] = useState([]);
  const [currentFilter, setCurrentFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(false);
  const [isAutoRefreshing, setIsAutoRefreshing] = useState(true);
  const [lastRefreshedAt, setLastRefreshedAt] = useState(null);

  // Notifications and actions
  const [notification, setNotification] = useState(null);
  const [submittingId, setSubmittingId] = useState(null);
  const [publishingId, setPublishingId] = useState(null);
  const [selectedPostForView, setSelectedPostForView] = useState(null);
  const [isCreatingDraft, setIsCreatingDraft] = useState(false);
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Authentication State (stores logged-in user in localStorage)
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const saved = localStorage.getItem('medium_blog_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authModalMode, setAuthModalMode] = useState('login');

  // Theme State: 'dark' (luxury obsidian & gold) or 'light'
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('medium_blog_theme') || 'dark';
  });

  // Apply theme to <html> element
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('medium_blog_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const handleAuthSuccess = (user) => {
    setCurrentUser(user);
    localStorage.setItem('medium_blog_user', JSON.stringify(user));
    setNotification({
      type: 'success',
      title: 'Welcome!',
      message: `Signed in as @${user.username}`,
    });
  };

  const handleSignOut = () => {
    setCurrentUser(null);
    localStorage.removeItem('medium_blog_user');
    setNotification({
      type: 'info',
      title: 'Signed Out',
      message: 'You have been signed out successfully.',
    });
  };

  // Full posts cache for counting statistics
  const [allPostsForStats, setAllPostsForStats] = useState([]);

  /**
   * Loads posts from API scoped by the current user.
   */
  const loadPosts = useCallback(
    async (showSpinner = false) => {
      if (showSpinner) setIsLoading(true);
      try {
        const username = currentUser?.username || null;
        const isClientFilter = currentFilter === 'all' || currentFilter === 'my_posts';
        const [allData, filteredData] = await Promise.all([
          listPosts('all', username),
          isClientFilter ? Promise.resolve(null) : listPosts(currentFilter, username),
        ]);

        setAllPostsForStats(allData || []);
        setPosts(isClientFilter ? allData : filteredData || []);
        setLastRefreshedAt(new Date());
      } catch (err) {
        const errorMsg =
          err?.response?.data?.detail ||
          err?.message ||
          'Failed to connect to backend API.';
        setNotification({
          type: 'error',
          title: 'Network / API Error',
          message: errorMsg,
        });
      } finally {
        if (showSpinner) setIsLoading(false);
      }
    },
    [currentFilter, currentUser]
  );

  // Initial load and filter change load
  useEffect(() => {
    loadPosts(true);
  }, [loadPosts]);

  // Auto-refresh polling every 5 seconds
  useEffect(() => {
    if (!isAutoRefreshing) return;
    const intervalId = setInterval(() => {
      loadPosts(false);
    }, 5000);
    return () => clearInterval(intervalId);
  }, [isAutoRefreshing, loadPosts]);

  // Compute status counts for summary bar
  const counts = useMemo(() => {
    const currentUsername = (currentUser?.username || '').trim().toLowerCase();
    const statCounts = {
      all: 0,
      draft: 0,
      flagged: 0,
      approved: 0,
      published: 0,
      my_posts: 0,
    };
    allPostsForStats.forEach((p) => {
      const author = (p.author_username || p.username || '').trim().toLowerCase();
      const isMine = currentUsername && author === currentUsername;

      if (isMine) {
        statCounts.my_posts += 1;
      }

      // 'For you' shows other authors' posts
      if (currentUsername) {
        if (author && author !== currentUsername) {
          statCounts.all += 1;
        }
      } else {
        statCounts.all += 1;
      }

      if (statCounts[p.status] !== undefined) {
        statCounts[p.status] += 1;
      }
    });
    return statCounts;
  }, [allPostsForStats, currentUser]);

  // Filter posts based on current tab ('all' = others' posts, 'my_posts' = user's posts) and searchQuery
  const displayedPosts = useMemo(() => {
    const currentUsername = (currentUser?.username || '').trim().toLowerCase();

    let filtered = posts;

    if (currentFilter === 'all' && currentUsername) {
      // "For you" feed shows other authors' posts
      filtered = posts.filter((post) => {
        const author = (post.author_username || post.username || '').trim().toLowerCase();
        return author && author !== currentUsername;
      });
    } else if (currentFilter === 'my_posts') {
      // "My Posts" tab shows all posts by the logged-in user
      filtered = allPostsForStats.filter((post) => {
        const author = (post.author_username || post.username || '').trim().toLowerCase();
        return currentUsername && author === currentUsername;
      });
    }

    if (!searchQuery.trim()) return filtered;
    const query = searchQuery.trim().toLowerCase();
    return filtered.filter((post) =>
      post.title && post.title.toLowerCase().includes(query)
    );
  }, [posts, allPostsForStats, currentFilter, currentUser, searchQuery]);

  // Handler: Create new draft
  const handleCreatePost = async (postData) => {
    setIsCreatingDraft(true);
    try {
      const payload = {
        ...postData,
        author_username: currentUser?.username || null,
      };
      const created = await createPost(payload);
      setNotification({
        type: 'success',
        title: 'Story Draft Saved',
        message: `"${created.title}" was saved as a draft. You can now submit it for review.`,
      });
      await loadPosts(false);
    } catch (err) {
      const errorDetail =
        err?.response?.data?.detail || err?.message || 'Failed to create draft.';
      setNotification({
        type: 'error',
        title: 'Failed to Save Story',
        message: Array.isArray(errorDetail)
          ? errorDetail.map((e) => e.msg || JSON.stringify(e)).join(', ')
          : String(errorDetail),
      });
      throw err;
    } finally {
      setIsCreatingDraft(false);
    }
  };

  // Handler: Submit for AI moderation review
  const handleSubmitForReview = async (postId) => {
    setSubmittingId(postId);
    try {
      const result = await submitPost(postId);
      if (result.status === 'approved') {
        setNotification({
          type: 'success',
          title: 'Story Approved',
          message: `Story #${postId} passed moderation and is ready to be published!`,
          reasons: [],
        });
      } else {
        setNotification({
          type: 'error',
          title: 'Story Flagged for Revision',
          message: `Story #${postId} requires revisions before publication.`,
          reasons: result.reasons || [],
        });
      }
      await loadPosts(false);
    } catch (err) {
      const errorMsg =
        err?.response?.data?.detail ||
        err?.message ||
        'Error submitting post for review.';
      setNotification({
        type: 'error',
        title: 'Review Submission Error',
        message: errorMsg,
      });
    } finally {
      setSubmittingId(null);
    }
  };

  // Handler: Edit a flagged post (resets it to draft)
  const handleEditPost = async (postId, postData) => {
    try {
      await updatePost(postId, postData);
      setNotification({
        type: 'success',
        title: 'Story Updated',
        message: `Story #${postId} has been saved as draft. You can now re-submit it for review.`,
      });
      await loadPosts(false);
    } catch (err) {
      const errorMsg =
        err?.response?.data?.detail ||
        err?.message ||
        'Failed to update post.';
      setNotification({
        type: 'error',
        title: 'Update Failed',
        message: errorMsg,
      });
      throw err;
    }
  };

  // Handler: Publish an approved post
  const handlePublish = async (postId) => {
    setPublishingId(postId);
    try {
      const published = await publishPost(postId);
      setNotification({
        type: 'success',
        title: 'Story Published',
        message: `"${published.title}" is now officially published!`,
      });
      await loadPosts(false);
    } catch (err) {
      const errorMsg =
        err?.response?.data?.detail ||
        err?.message ||
        'Failed to publish article.';
      setNotification({
        type: 'error',
        title: 'Publish Error',
        message: errorMsg,
      });
    } finally {
      setPublishingId(null);
    }
  };

  return (
    <div className="medium-app-layout">
      {/* ── Medium Top Header ─────────────────────────────────────────────── */}
      <header className="medium-navbar">
        <div className="medium-navbar-container">
          <div className="navbar-left">
            <a href="#" className="medium-brand-logo" onClick={(e) => { e.preventDefault(); setCurrentFilter('all'); }}>
              <span className="brand-name">Blog Hub</span>
            </a>
            <div className="navbar-search-box">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              <input
                type="text"
                placeholder="Search stories by title..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                aria-label="Search stories by title"
              />
              {searchQuery && (
                <button
                  type="button"
                  className="search-clear-btn"
                  onClick={() => setSearchQuery('')}
                  title="Clear search"
                  aria-label="Clear search"
                >
                  ✕
                </button>
              )}
            </div>
          </div>

          <div className="navbar-right">
            {/* Theme Toggle Button (Light/Dark mode) */}
            <button
              type="button"
              className="theme-toggle-btn"
              onClick={toggleTheme}
              title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? '☀️' : '🌙'}
            </button>

            <button
              type="button"
              className="navbar-write-link"
              onClick={() => setIsEditorOpen((prev) => !prev)}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 20h9"></path>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
              </svg>
              <span>Write</span>
            </button>

            {/* User Account / Sign In Trigger */}
            {currentUser ? (
              <div className="navbar-user-btn" title={`Signed in as @${currentUser.username}`}>
                <div className="navbar-user-avatar">
                  {currentUser.username[0].toUpperCase()}
                </div>
                <span className="user-username">@{currentUser.username}</span>
                <button
                  type="button"
                  className="navbar-signout-btn"
                  onClick={handleSignOut}
                  title="Sign out"
                >
                  Exit
                </button>
              </div>
            ) : (
              <button
                type="button"
                className="navbar-signin-trigger"
                onClick={() => setIsAuthModalOpen(true)}
              >
                Sign In
              </button>
            )}
          </div>
        </div>
      </header>

      {/* ── Main Layout (Gated by Authentication) ────────────────────────── */}
      <div className="medium-main-layout">
        {!currentUser ? (
          /* ── Auth Gate: Displayed for guests / unauthenticated visitors ── */
          <div className="auth-gate-hero" style={{ width: '100%' }}>
            <span className="auth-gate-badge">🔒 Exclusive Editorial Access</span>
            <h1 className="auth-gate-title">Stories that inspire, inform, and ignite curiosity.</h1>
            <p className="auth-gate-subtitle">
              Sign in or create an account to read articles, browse stories across editorial feeds, and draft new publications.
            </p>
            <div className="auth-gate-actions">
              <button
                type="button"
                className="btn-gate-primary"
                onClick={() => {
                  setAuthModalMode('login');
                  setIsAuthModalOpen(true);
                }}
              >
                Sign In to Read
              </button>
              <button
                type="button"
                className="btn-gate-secondary"
                onClick={() => {
                  setAuthModalMode('register');
                  setIsAuthModalOpen(true);
                }}
              >
                Create Account
              </button>
            </div>
          </div>
        ) : (
          /* ── Authenticated User View: Full Blog Platform Access ── */
          <>
            {/* Left Column: Feed & Editor */}
            <main className="medium-feed-column">
              {/* Toast Notification */}
              <Notification
                notification={notification}
                onClose={() => setNotification(null)}
              />

              {/* Story Editor Section */}
              <section className="medium-editor-section">
                <PostForm
                  onSubmit={handleCreatePost}
                  isSubmitting={isCreatingDraft}
                  isOpen={isEditorOpen}
                  onToggleOpen={() => setIsEditorOpen((prev) => !prev)}
                  currentUser={currentUser}
                />
              </section>

              {/* Feed Tabs: For you / Published / Approved / Flagged / Drafts */}
              <section className="medium-tabs-section">
                <StatusFilter
                  currentFilter={currentFilter}
                  onSelectFilter={setCurrentFilter}
                  counts={counts}
                />
              </section>

              {/* Story Articles Feed */}
              <section className="medium-feed-section">
                <PostList
                  posts={displayedPosts}
                  currentUser={currentUser}
                  isLoading={isLoading}
                  currentFilter={currentFilter}
                  searchQuery={searchQuery}
                  onClearSearch={() => setSearchQuery('')}
                  onSubmitForReview={handleSubmitForReview}
                  onPublish={handlePublish}
                  onEditPost={handleEditPost}
                  onViewPost={setSelectedPostForView}
                  submittingId={submittingId}
                  publishingId={publishingId}
                  onResetFilter={() => setCurrentFilter('all')}
                />
              </section>
            </main>

            {/* Right Column: Medium Sidebar */}
            <aside className="medium-sidebar-column">
              <div className="sidebar-sticky-wrapper">
                {/* Staff Picks / Platform Highlights */}
                <div className="sidebar-widget">
                  <h3 className="widget-title">Publishing Guidelines</h3>
                  <ul className="guidelines-list">
                    <li>
                      <span className="guideline-number">01</span>
                      <div>
                        <strong>Length Rule</strong>
                        <p>Articles between 50 and 2,000 characters qualify for automated AI review.</p>
                      </div>
                    </li>
                    <li>
                      <span className="guideline-number">02</span>
                      <div>
                        <strong>Civil Discourse</strong>
                        <p>AI reviews for profanity, harassment, and excessive shouting.</p>
                      </div>
                    </li>
                    <li>
                      <span className="guideline-number">03</span>
                      <div>
                        <strong>Immutable Publication</strong>
                        <p>Once published, articles become read-only and permanently locked.</p>
                      </div>
                    </li>
                    <li>
                      <span className="guideline-number">04</span>
                      <div>
                        <strong>Reject ALL-CAPS</strong>
                        <p>All words with capital letters will not be approved.</p>
                      </div>
                    </li>
                    <li>
                      <span className="guideline-number">05</span>
                      <div>
                        <strong>Overly Aggressive Content</strong>
                        <p>Over Aggressive Content will not be approved by AI.</p>
                      </div>
                    </li>
                  </ul>
                </div>

                {/* ── User Post Analytics & Real-Time Chart ──────────────── */}
                <UserPostAnalytics
                  currentUser={currentUser}
                  allPosts={allPostsForStats}
                  lastRefreshedAt={lastRefreshedAt}
                  isAutoRefreshing={isAutoRefreshing}
                  onRefresh={() => loadPosts(false)}
                  onFilterSelect={(tabKey) => setCurrentFilter(tabKey)}
                />
              </div>
            </aside>
          </>
        )}
      </div>

      {/* Full Screen Article Reader Modal */}
      <PublishedView
        post={selectedPostForView}
        currentUser={currentUser}
        onClose={() => setSelectedPostForView(null)}
      />

      {/* Authentication Modal (Login & Registration) */}
      <AuthModal
        isOpen={isAuthModalOpen}
        initialMode={authModalMode}
        onClose={() => setIsAuthModalOpen(false)}
        onAuthSuccess={handleAuthSuccess}
      />
    </div>
  );
}
