import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import SearchBox from './components/SearchBox';
import PRGrid from './components/PRGrid';
import { PR } from './types/PR';
import { PRDataService } from './services/PRDataService';
import { ThemeProvider } from './contexts/ThemeContext';

function App() {
  const [allPRs, setAllPRs] = useState<PR[]>([]);
  const [filteredPRs, setFilteredPRs] = useState<PR[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hashFilterActive, setHashFilterActive] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const data = await PRDataService.loadPRData();
        setAllPRs(data);
        setFilteredPRs(data);
        setError(null);
      } catch (err) {
        setError('Failed to load PR data. Please try again later.');
        console.error('Error loading PR data:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash;
      console.log('Hash changed to:', hash);
      
      if (hash.startsWith('#pr-')) {
        const prNumber = parseInt(hash.substring(4));
        if (!isNaN(prNumber)) {
          const targetPR = allPRs.find(pr => pr.number === prNumber);
          if (targetPR) {
            setFilteredPRs([targetPR]);
            setHashFilterActive(true);
            // Scroll to the PR card after a short delay to ensure it's rendered
            setTimeout(() => {
              const element = document.getElementById(`pr-${prNumber}`);
              if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
              }
            }, 100);
          }
        }
      } else {
        // No hash or invalid hash, show all PRs
        setHashFilterActive(false);
        setFilteredPRs(allPRs);
      }
    };

    // Listen for hash changes
    window.addEventListener('hashchange', handleHashChange);
    
    // Handle initial hash on mount if we have data
    if (allPRs.length > 0) {
      handleHashChange();
    }

    return () => {
      window.removeEventListener('hashchange', handleHashChange);
    };
  }, [allPRs]);

  useEffect(() => {
    const performSearch = async () => {
      // Skip search if hash filter is active
      if (hashFilterActive) {
        return;
      }
      
      if (searchQuery.trim() === '') {
        setFilteredPRs(allPRs);
      } else {
        const results = await PRDataService.searchPRs(searchQuery, allPRs);
        setFilteredPRs(results);
      }
    };

    performSearch();
  }, [searchQuery, allPRs, hashFilterActive]);

  const getLatestDate = (): string => {
    if (allPRs.length === 0) return '-';
    const latestDate = new Date(Math.max(...allPRs.map(pr => new Date(pr.created).getTime())));
    return latestDate.toISOString().split('T')[0]; // Format as YYYY-MM-DD
  };

  const handleSearchStart = () => {
    setHashFilterActive(false);
    // Clear the hash from URL when user starts searching
    if (window.location.hash) {
      window.history.replaceState(null, '', window.location.pathname);
    }
  };

  return (
    <ThemeProvider>
      <div className="App">
        <div className="container">
          <Header totalPRs={allPRs.length} latestDate={getLatestDate()} />
          <SearchBox 
            value={searchQuery} 
            onChange={setSearchQuery} 
            onSearchStart={handleSearchStart}
          />
          <PRGrid prs={filteredPRs} loading={loading} error={error} />
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
