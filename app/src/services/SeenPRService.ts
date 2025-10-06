/**
 * Service for tracking which PR entries the user has already seen
 * Uses localStorage to persist information across browser sessions
 */
export class SeenPRService {
  private static readonly STORAGE_KEY = 'pr-summary-last-seen';

  /**
   * Get the timestamp of when the user last visited the dashboard
   * @returns ISO timestamp string or null if never visited
   */
  static getLastSeenTimestamp(): string | null {
    try {
      return localStorage.getItem(this.STORAGE_KEY);
    } catch (error) {
      console.warn('Failed to read from localStorage:', error);
      return null;
    }
  }

  /**
   * Update the last seen timestamp to current time
   */
  static updateLastSeenTimestamp(): void {
    try {
      const now = new Date().toISOString();
      localStorage.setItem(this.STORAGE_KEY, now);
    } catch (error) {
      console.warn('Failed to write to localStorage:', error);
    }
  }

  /**
   * Check if a PR was created after the last seen timestamp
   * @param prCreatedDate ISO timestamp of when the PR was created
   * @returns true if the PR is new (created after last seen), false otherwise
   */
  static isPRNew(prCreatedDate: string): boolean {
    const lastSeen = this.getLastSeenTimestamp();
    if (!lastSeen) {
      // If user has never visited before, all PRs are considered "seen" (no new indicator)
      return false;
    }
    
    try {
      const prDate = new Date(prCreatedDate);
      const lastSeenDate = new Date(lastSeen);
      return prDate > lastSeenDate;
    } catch (error) {
      console.warn('Failed to parse dates:', error);
      return false;
    }
  }
}