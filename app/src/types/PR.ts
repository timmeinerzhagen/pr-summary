export interface PR {
  number: number;
  title: string;
  author: string;
  state: string;
  created: string;
  url: string;
  repository: string;
  analysis_date: string;
  details: string[];
  summary: string;
  generated_title: string;
  commits: string[];
  original_description: string;
  raw_analysis: string;
}
