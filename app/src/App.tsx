import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import SearchBox from './components/SearchBox';
import PRGrid from './components/PRGrid';
import { PR } from './types/PR';
import { PRDataService } from './services/PRDataService';

function App() {
  const [allPRs, setAllPRs] = useState<PR[]>([]);
  const [filteredPRs, setFilteredPRs] = useState<PR[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
    const performSearch = async () => {
      if (searchQuery.trim() === '') {
        setFilteredPRs(allPRs);
      } else {
        const results = await PRDataService.searchPRs(searchQuery, allPRs);
        setFilteredPRs(results);
      }
    };

    performSearch();
  }, [searchQuery, allPRs]);

  const getLatestDate = (): string => {
    if (allPRs.length === 0) return '-';
    const latestDate = new Date(Math.max(...allPRs.map(pr => new Date(pr.created).getTime())));
    return latestDate.toISOString().split('T')[0]; // Format as YYYY-MM-DD
  };

  return (
    <div className="App">
      <div className="container">
        <Header totalPRs={allPRs.length} latestDate={getLatestDate()} />
        <SearchBox value={searchQuery} onChange={setSearchQuery} />
        <PRGrid prs={filteredPRs} loading={loading} error={error} />
      </div>
    </div>
  );
}

export default App;
