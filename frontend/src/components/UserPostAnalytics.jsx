import React from 'react';

/**
 * UserPostAnalytics — Live real-time visual chart & analytics widget
 * Displays a sleek, interactive single chart showing the user's personal posts
 * broken down across Draft, Flagged, Approved, and Published statuses.
 */
export default function UserPostAnalytics({
  currentUser,
  allPosts = [],
  lastRefreshedAt = null,
  isAutoRefreshing = true,
  onRefresh = null,
  onFilterSelect = null,
}) {
  if (!currentUser?.username) return null;

  const username = currentUser.username.toLowerCase();

  // Filter posts belonging specifically to this authenticated user
  const userPosts = allPosts.filter((p) => {
    const author = (p.author_username || p.username || '').toLowerCase();
    return author === username;
  });

  const counts = {
    draft: 0,
    flagged: 0,
    approved: 0,
    published: 0,
  };

  userPosts.forEach((p) => {
    if (counts[p.status] !== undefined) {
      counts[p.status] += 1;
    }
  });

  const total = userPosts.length;

  const categories = [
    {
      key: 'published',
      label: 'Published',
      count: counts.published,
      color: '#10b981', // Emerald green
      accentBg: 'rgba(16, 185, 129, 0.12)',
      icon: '🌐',
    },
    {
      key: 'approved',
      label: 'Approved',
      count: counts.approved,
      color: '#3b82f6', // Sapphire blue
      accentBg: 'rgba(59, 130, 246, 0.12)',
      icon: '✅',
    },
    {
      key: 'draft',
      label: 'Draft',
      count: counts.draft,
      color: '#c5a880', // Obsidian warm gold
      accentBg: 'rgba(197, 168, 128, 0.12)',
      icon: '📝',
    },
    {
      key: 'flagged',
      label: 'Flagged',
      count: counts.flagged,
      color: '#ef4444', // Warning red
      accentBg: 'rgba(239, 68, 68, 0.12)',
      icon: '⚠️',
    },
  ];

  // Calculate percentages for the stacked segmented bar chart
  let cumulative = 0;
  const segments = categories.map((cat) => {
    const pct = total > 0 ? (cat.count / total) * 100 : 0;
    const start = cumulative;
    cumulative += pct;
    return {
      ...cat,
      pct,
      start,
    };
  });

  const timeString = lastRefreshedAt
    ? new Date(lastRefreshedAt).toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
      })
    : 'Just now';

  return (
    <div className="sidebar-widget user-analytics-widget">
      {/* Widget Header with live pulse */}
      <div className="analytics-header">
        <div className="analytics-title-group">
          <span className="analytics-icon">📊</span>
          <h3 className="widget-title" style={{ margin: 0 }}>
            My Stories Overview
          </h3>
        </div>
        <div className="live-status-badge" title="Live real-time polling active every 5s">
          <span className={`live-pulse-dot ${isAutoRefreshing ? 'active' : ''}`} />
          <span className="live-text">LIVE</span>
        </div>
      </div>

      <div className="analytics-byline">
        Stories authored by <strong className="analytics-username">@{currentUser.username}</strong>
      </div>

      {/* Primary Visual: Multi-Segmented Proportional Bar Chart */}
      <div className="analytics-chart-container">
        <div className="analytics-chart-bar" role="img" aria-label="Stories breakdown by status">
          {total === 0 ? (
            <div className="chart-segment empty" style={{ width: '100%' }}>
              <span className="empty-chart-label">No stories yet</span>
            </div>
          ) : (
            segments.map((seg) =>
              seg.pct > 0 ? (
                <div
                  key={seg.key}
                  className={`chart-segment segment-${seg.key}`}
                  style={{
                    width: `${seg.pct}%`,
                    backgroundColor: seg.color,
                  }}
                  title={`${seg.label}: ${seg.count} (${seg.pct.toFixed(1)}%)`}
                />
              ) : null
            )
          )}
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="analytics-grid">
        {categories.map((cat) => (
          <button
            key={cat.key}
            type="button"
            className="analytics-stat-card"
            onClick={() => onFilterSelect && onFilterSelect(cat.key)}
            title={`View ${cat.label} stories`}
          >
            <div className="stat-card-top">
              <span className="stat-icon">{cat.icon}</span>
              <span className="stat-count" style={{ color: cat.color }}>
                {cat.count}
              </span>
            </div>
            <div className="stat-card-bottom">
              <span className="stat-label">{cat.label}</span>
              <span className="stat-pct">
                {total > 0 ? `${Math.round((cat.count / total) * 100)}%` : '0%'}
              </span>
            </div>
          </button>
        ))}
      </div>

      {/* Real-Time Live Footer Info */}
      <div className="analytics-footer">
        <div className="live-timestamp">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <span>Synced: {timeString}</span>
        </div>
        {onRefresh && (
          <button
            type="button"
            className="analytics-refresh-btn"
            onClick={onRefresh}
            title="Refresh analytics data now"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M23 4v6h-6"></path>
              <path d="M1 20v-6h6"></path>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            <span>Sync</span>
          </button>
        )}
      </div>
    </div>
  );
}
