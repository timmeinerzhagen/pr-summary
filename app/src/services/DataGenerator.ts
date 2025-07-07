import { PR } from '../types/PR';

// Function to generate PR data for the React app
export const generatePRData = async (): Promise<PR[]> => {
  try {
    // Fetch data from pr-data.json file
    const response = await fetch('/pr-data.json');
    if (!response.ok) {
      throw new Error(`Failed to fetch PR data: ${response.status} ${response.statusText}`);
    }
    
    const prData: PR[] = await response.json();
    return prData;
  } catch (error) {
    console.error('Error fetching PR data from /pr-data.json:', error);
    // Return empty array on error instead of hardcoded fallback
    return [];
  }
};

// Function to load real data from files
export const loadRealPRData = async (): Promise<PR[]> => {
  // This now uses the same implementation as generatePRData
  return generatePRData();
};
