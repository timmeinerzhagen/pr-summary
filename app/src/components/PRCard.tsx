import React, { useState } from 'react';
import { PR } from '../types/PR';
import { renderMarkdown } from '../utils/markdown';

interface PRCardProps {
  pr: PR;
}

const PRCard: React.FC<PRCardProps> = ({ pr }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  // Clean up the summary text
  let summary = pr.summary || 'No summary available';
  if (summary.includes('Based on the git diff')) {
    summary = pr.details && pr.details.length > 0 ? pr.details[0] : 'No summary available';
  }

  return (
    <div className={`pr-card ${isExpanded ? 'expanded' : ''}`} onClick={toggleExpanded}>
      <div className="pr-basic-info">
        <div className="pr-basic-content">
          <div className="pr-meta">
            <a 
              href={pr.url} 
              target="_blank" 
              rel="noopener noreferrer" 
              onClick={(e) => e.stopPropagation()}
              style={{ textDecoration: 'none' }}
            >
              <span className="pr-number">#{pr.number}</span>              
            </a>
            <span>📅 {formatDate(pr.created)}</span>
            <span>👤 {pr.author}</span>
          </div>
          <div className="pr-title">{pr.generated_title}</div>
          
        </div>
        <div className="expand-indicator">▼</div>
      </div>
      
      {isExpanded && (
        <div className="pr-content" onClick={(e) => e.stopPropagation()}>
          <div className="pr-summary">
            <h3>Summary</h3>
            <div 
              className="markdown-content" 
              dangerouslySetInnerHTML={{ __html: renderMarkdown(summary) }}
            />
            
            {pr.commits && pr.commits.length > 0 && (
              <div className="commits-section">
                <h4>Commits</h4>
                <div className="commits-list">
                  {pr.commits.slice(0, 3).map((commit, index) => (
                    <div 
                      key={index} 
                      className="commit-item markdown-content"
                      dangerouslySetInnerHTML={{ __html: renderMarkdown(commit) }}
                    />
                  ))}
                  {pr.commits.length > 3 && (
                    <div className="commit-item" style={{ color: '#666' }}>
                      ... and {pr.commits.length - 3} more
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
          
          <div className="pr-actions">
            <a 
              href={pr.url} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="btn btn-primary"
              onClick={(e) => e.stopPropagation()}
            >
              View on GitHub
            </a>
            <a 
              href={pr.url + "/files"} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="btn btn-primary"
              onClick={(e) => e.stopPropagation()}
            >
              Changed Files
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default PRCard;
