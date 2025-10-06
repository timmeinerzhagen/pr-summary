import React from 'react';
import { PR } from '../types/PR';
import PRCard from './PRCard';
import { SeenPRService } from '../services/SeenPRService';

interface PRGridProps {
  prs: PR[];
  loading: boolean;
  error: string | null;
}

const PRGrid: React.FC<PRGridProps> = ({ prs, loading, error }) => {
  if (loading) {
    return (
      <div className="loading">
        Loading PR analyses...
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        {error}
      </div>
    );
  }

  if (prs.length === 0) {
    return (
      <div className="no-results">
        <h3>No results found</h3>
        <p>Try adjusting your search terms</p>
      </div>
    );
  }

  return (
    <div className="pr-grid">
      {prs.map((pr, index) => {
        const isNewPR = SeenPRService.isPRNew(pr.created);
        const prevPR = index > 0 ? prs[index - 1] : null;
        const isPrevPRNew = prevPR ? SeenPRService.isPRNew(prevPR.created) : true;
        
        // Show "new" indicator when transitioning from new to old PRs
        const showNewIndicator = !isNewPR && isPrevPRNew;
        
        return (
          <React.Fragment key={pr.number}>
            {showNewIndicator && (
              <div className="new-indicator">
                <div className="new-indicator-line"></div>
                <div className="new-indicator-text">new</div>
                <div className="new-indicator-line"></div>
              </div>
            )}
            <PRCard pr={pr} />
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default PRGrid;
