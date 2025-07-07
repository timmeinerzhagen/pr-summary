import React from 'react';

interface HeaderProps {
  totalPRs: number;
  latestDate: string;
}

const Header: React.FC<HeaderProps> = ({ totalPRs, latestDate }) => {
  return (
    <>
      <header>
        <h1>🔍 GitHub PR Analysis Dashboard</h1>
        <p className="subtitle">AI-powered summaries of GitHub Pull Requests</p>
        <p className="subtitle">
          <a 
            href="https://github.com/timmeinerzhagen/llm-pr-summary" 
            target="_blank" 
            rel="noopener noreferrer"
          >
            📁 View Repository on GitHub
          </a>
        </p>
      </header>

      <div className="stats">
        <div className="stat-card">
          <span className="stat-number">{totalPRs}</span>
          <span className="stat-label">Total PRs</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">1</span>
          <span className="stat-label">Repository</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">{latestDate}</span>
          <span className="stat-label">Latest Analysis</span>
        </div>
      </div>
    </>
  );
};

export default Header;
