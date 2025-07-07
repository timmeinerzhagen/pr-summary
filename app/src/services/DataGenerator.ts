import { PR } from '../types/PR';

// Function to generate PR data for the React app
export const generatePRData = async (): Promise<PR[]> => {
  try {
    // In a real scenario, you would fetch this from an API or load files
    // For now, we'll create a few more sample PRs to showcase the functionality
    const samplePRs: PR[] = [
      {
        number: 38984,
        title: "Repo sync",
        author: "docs-bot",
        state: "closed",
        created: "2025-06-20T12:38:38Z",
        url: "https://github.com/github/docs/pull/38984",
        repository: "github/docs",
        analysis_date: "2025-07-06 15:43:02",
        details: [
          "Updated GitHub Actions secrets documentation to clarify case-insensitivity behavior",
          "Specified that secret names are case-insensitive when referenced",
          "Added note that GitHub stores secret names in uppercase regardless of input casing"
        ],
        summary: "- Updated GitHub Actions secrets documentation to clarify case-insensitivity behavior\n- Specified that secret names are case-insensitive when referenced\n- Added note that GitHub stores secret names in uppercase regardless of input casing",
        generated_title: "Clarify secret name casing behavior in GitHub Actions documentation",
        commits: [
          "**0560de3**: Clarify secret name casing behavior in GitHub Actions documentation (#56014) (by Copilot)"
        ],
        original_description: "\nThis is an automated pull request to sync changes between the public and private repos.\nOur bot will merge this pull request automatically.\nTo preserve continuity across repos, _do not squash_ this pull request.\n",
        raw_analysis: "### Summary\n- Updated GitHub Actions secrets documentation to clarify case-insensitivity behavior\n- Specified that secret names are case-insensitive when referenced\n- Added note that GitHub stores secret names in uppercase regardless of input casing\n\n### Title\nClarify secret name casing behavior in GitHub Actions documentation"
      },
      {
        number: 39111,
        title: "Fix authentication issue",
        author: "john-doe",
        state: "merged",
        created: "2025-06-25T09:15:22Z",
        url: "https://github.com/github/docs/pull/39111",
        repository: "github/docs",
        analysis_date: "2025-07-06 16:22:15",
        details: [
          "Fixed OAuth authentication flow for third-party applications",
          "Updated error handling for expired tokens",
          "Added retry mechanism for failed authentication attempts"
        ],
        summary: "This PR addresses critical authentication issues in the OAuth flow, improving user experience and system reliability.",
        generated_title: "Fix OAuth authentication flow and improve error handling",
        commits: [
          "**abc123f**: Fix OAuth token validation logic",
          "**def456g**: Add retry mechanism for auth failures",
          "**ghi789h**: Update error messages for better UX"
        ],
        original_description: "Fixes the authentication issues reported in #38950. This includes better error handling and a more robust retry mechanism.",
        raw_analysis: "### Summary\nThis PR addresses critical authentication issues in the OAuth flow, improving user experience and system reliability.\n\n### Details\n- Fixed OAuth authentication flow for third-party applications\n- Updated error handling for expired tokens\n- Added retry mechanism for failed authentication attempts"
      },
      {
        number: 39114,
        title: "Add new API endpoints",
        author: "jane-smith",
        state: "open",
        created: "2025-06-28T14:30:45Z",
        url: "https://github.com/github/docs/pull/39114",
        repository: "github/docs",
        analysis_date: "2025-07-06 17:05:33",
        details: [
          "Added new REST API endpoints for repository management",
          "Implemented rate limiting for new endpoints",
          "Added comprehensive documentation for all new APIs",
          "Included unit tests for all new functionality"
        ],
        summary: "**New API Endpoints Added**\n\nThis PR introduces several new REST API endpoints to enhance repository management capabilities:\n\n- `/api/v1/repos/{owner}/{repo}/settings` - Get/update repository settings\n- `/api/v1/repos/{owner}/{repo}/collaborators` - Manage collaborators\n- `/api/v1/repos/{owner}/{repo}/hooks` - Webhook management\n\nAll endpoints include proper authentication, rate limiting, and comprehensive error handling.",
        generated_title: "Add repository management API endpoints with rate limiting",
        commits: [
          "**xyz789a**: Add repository settings API endpoint",
          "**uvw456b**: Implement collaborators management API",
          "**rst123c**: Add webhook management endpoints",
          "**opq987d**: Add rate limiting and documentation"
        ],
        original_description: "This PR adds new API endpoints for repository management as requested in issue #38500. All endpoints follow our established patterns and include comprehensive testing.",
        raw_analysis: "### Summary\nThis PR introduces several new REST API endpoints to enhance repository management capabilities with proper rate limiting and documentation.\n\n### Key Changes\n- Added new REST API endpoints for repository management\n- Implemented rate limiting for new endpoints\n- Added comprehensive documentation for all new APIs\n- Included unit tests for all new functionality"
      }
    ];

    return samplePRs;
  } catch (error) {
    console.error('Error generating PR data:', error);
    return [];
  }
};

// Function to load real data from files (to be implemented)
export const loadRealPRData = async (): Promise<PR[]> => {
  // This would be implemented to load actual JSON files from the data directory
  // For now, we'll use the generated sample data
  return generatePRData();
};
