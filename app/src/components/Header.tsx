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
        <p className="subtitle">
          github/docs Pull Requests have awful titles. <br />
          To make it easier to follow changes, this gives you AI-powered summaries of their Pull Requests
        </p>
        <p className="subtitle">
          <br />
          <a 
            href="https://github.com/timmeinerzhagen/pr-summary" 
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
          <span className="stat-number">{latestDate}</span>
          <span className="stat-label">Latest Analysis</span>
        </div>
      </div>
    </>
  );
};

export default Header;
