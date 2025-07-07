import { marked } from 'marked';
import DOMPurify from 'dompurify';

// Configure marked for safe rendering
marked.setOptions({
  breaks: true,
  gfm: true,
});

export const renderMarkdown = (text: string): string => {
  if (!text) return '';
  
  try {
    const rawHtml = marked.parse(text);
    return DOMPurify.sanitize(rawHtml as string);
  } catch (error) {
    console.error('Error rendering markdown:', error);
    return text;
  }
};
