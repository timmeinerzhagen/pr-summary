import React from 'react';
import { PR } from '../types/PR';
import PRCard from './PRCard';

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
      {prs.map((pr) => (
        <PRCard key={pr.number} pr={pr} />
      ))}
    </div>
  );
};

export default PRGrid;
