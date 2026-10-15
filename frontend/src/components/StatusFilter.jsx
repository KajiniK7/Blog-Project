import React, { useState } from 'react';

const FILTER_TABS = [
  { key: 'all',       label: 'For you',   statusKey: 'all' },
  { key: 'published', label: 'Published', statusKey: 'published' },
  { key: 'approved',  label: 'Approved',  statusKey: 'approved' },
  { key: 'flagged',   label: 'Flagged',   statusKey: 'flagged' },
  { key: 'draft',     label: 'Drafts',    statusKey: 'draft' },
  { key: 'my_posts',  label: 'My Posts',  statusKey: 'my_posts' },
];

/**
 * Medium-style category navigation and feed tabs
 */
export default function StatusFilter({
  currentFilter,
  onSelectFilter,
  counts = { all: 0, draft: 0, flagged: 0, approved: 0, published: 0 },
}) {
  return (
    <div className="medium-feed-nav-wrapper">
      <nav className="medium-feed-nav" aria-label="Stories Feed Filter">
        {FILTER_TABS.map((tab) => {
          const isActive = currentFilter === tab.key;
          const count = counts[tab.statusKey] || 0;

          return (
            <button
              key={tab.key}
              type="button"
              className={`medium-tab-item ${isActive ? 'is-active' : ''}`}
              onClick={() => onSelectFilter(tab.key)}
              aria-current={isActive ? 'page' : undefined}
            >
              <span className="tab-label">{tab.label}</span>
              <span className="tab-count-pill">{count}</span>
            </button>
          );
        })}
      </nav>
      <div className="medium-feed-divider" />
    </div>
  );
}
