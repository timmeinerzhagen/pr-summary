import React from 'react';

interface SearchBoxProps {
  value: string;
  onChange: (value: string) => void;
  onSearchStart?: () => void;
  placeholder?: string;
}

const SearchBox: React.FC<SearchBoxProps> = ({ 
  value, 
  onChange, 
  onSearchStart,
  placeholder = "🔍 Search PRs by title, number, or content..." 
}) => {
  const handleChange = (newValue: string) => {
    if (onSearchStart) {
      onSearchStart();
    }
    onChange(newValue);
  };

  return (
    <div className="search-container">
      <input
        type="text"
        className="search-box"
        value={value}
        onChange={(e) => handleChange(e.target.value)}
        placeholder={placeholder}
      />
    </div>
  );
};

export default SearchBox;
