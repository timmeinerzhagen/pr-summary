import { PR } from '../types/PR';
import { generatePRData } from './DataGenerator';

export class PRDataService {
  static async loadPRData(): Promise<PR[]> {
    try {
      // Load the generated sample data
      const data = await generatePRData();
      console.log(`Loaded ${data.length} PR analyses`);
      return data;
    } catch (error) {
      console.error('Error loading PR data:', error);
      return [];
    }
  }

  static async searchPRs(query: string, data: PR[]): Promise<PR[]> {
    const lowercaseQuery = query.toLowerCase();
    return data.filter(pr =>
      pr.title.toLowerCase().includes(lowercaseQuery) ||
      pr.number.toString().includes(lowercaseQuery) ||
      pr.author.toLowerCase().includes(lowercaseQuery) ||
      pr.summary.toLowerCase().includes(lowercaseQuery) ||
      pr.details.some(detail => detail.toLowerCase().includes(lowercaseQuery))
    );
  }
}
