/**
 * Citation Extractor Service
 * Parses and enriches citations from LLM responses.
 */

import { logger } from '../utils/logger.js';

/**
 * Citation pattern for extracting references from text.
 * Matches: [Title], [Title > Section], According to [Title]...
 */
const CITATION_PATTERN = /\[([^\]]+)\]/g;

/**
 * Extract citations from LLM response text.
 *
 * @param {string} text - LLM response text
 * @returns {Array<Object>} Extracted citations with text and position
 */
export function extractCitations(text) {
  const citations = [];
  let match;

  while ((match = CITATION_PATTERN.exec(text)) !== null) {
    const fullMatch = match[0];
    const content = match[1];

    // Parse title and section
    const parts = content.split('>').map(p => p.trim());
    const title = parts[0];
    const section = parts[1] || null;

    citations.push({
      raw: fullMatch,
      title,
      section,
      position: match.index,
    });
  }

  // Reset regex state
  CITATION_PATTERN.lastIndex = 0;

  return citations;
}

/**
 * Match a citation to source chunks by title.
 *
 * @param {Object} citation - Parsed citation object
 * @param {Array} chunks - Retrieved chunks with metadata
 * @returns {Object|null} Best matching chunk or null
 */
export function matchCitationToChunk(citation, chunks) {
  if (!chunks || chunks.length === 0) return null;

  // Try exact title match first
  let match = chunks.find(chunk =>
    chunk.metadata?.title?.toLowerCase() === citation.title.toLowerCase()
  );

  if (match) return match;

  // Try partial/fuzzy match
  match = chunks.find(chunk => {
    const chunkTitle = chunk.metadata?.title?.toLowerCase() || '';
    const citationTitle = citation.title.toLowerCase();

    return chunkTitle.includes(citationTitle) ||
           citationTitle.includes(chunkTitle) ||
           similarity(chunkTitle, citationTitle) > 0.7;
  });

  return match || null;
}

/**
 * Simple string similarity (Dice coefficient).
 *
 * @param {string} a - First string
 * @param {string} b - Second string
 * @returns {number} Similarity score 0-1
 */
export function similarity(a, b) {
  if (!a || !b) return 0;
  if (a === b) return 1;

  const aBigrams = getBigrams(a.toLowerCase());
  const bBigrams = getBigrams(b.toLowerCase());

  let matches = 0;
  for (const bigram of aBigrams) {
    if (bBigrams.has(bigram)) matches++;
  }

  return (2 * matches) / (aBigrams.size + bBigrams.size);
}

/**
 * Get bigrams (character pairs) from string.
 *
 * @param {string} str - Input string
 * @returns {Set<string>} Set of bigrams
 */
function getBigrams(str) {
  const bigrams = new Set();
  for (let i = 0; i < str.length - 1; i++) {
    bigrams.add(str.slice(i, i + 2));
  }
  return bigrams;
}

/**
 * Enrich citations with source metadata from chunks.
 *
 * @param {Array} citations - Parsed citations
 * @param {Array} chunks - Retrieved chunks with metadata
 * @returns {Array<Object>} Enriched citations
 */
export function enrichCitations(citations, chunks) {
  return citations.map(citation => {
    const matchedChunk = matchCitationToChunk(citation, chunks);

    if (!matchedChunk) {
      logger.warn('No chunk match for citation', { title: citation.title });
      return {
        ...citation,
        matched: false,
        sourceUrls: [],
        docId: null,
        score: null,
      };
    }

    const sourceUrls = matchedChunk.metadata?.source_urls
      ?.split(',')
      .filter(Boolean) || [];

    return {
      ...citation,
      matched: true,
      sourceUrls,
      docId: matchedChunk.metadata?.doc_id || null,
      score: matchedChunk.score || null,
      fullTitle: matchedChunk.metadata?.title || citation.title,
    };
  });
}

/**
 * Format citations as markdown list.
 *
 * @param {Array} citations - Enriched citations
 * @returns {string} Markdown formatted citation list
 */
export function formatCitationsMarkdown(citations) {
  const uniqueCitations = deduplicateCitations(citations);

  if (uniqueCitations.length === 0) {
    return '';
  }

  const lines = ['', '---', '**Sources:**'];

  uniqueCitations.forEach((citation, index) => {
    const title = citation.fullTitle || citation.title;
    const section = citation.section ? ` > ${citation.section}` : '';

    if (citation.sourceUrls && citation.sourceUrls.length > 0) {
      lines.push(`${index + 1}. [${title}${section}](${citation.sourceUrls[0]})`);
    } else {
      lines.push(`${index + 1}. ${title}${section} *(Internal Document)*`);
    }
  });

  return lines.join('\n');
}

/**
 * Remove duplicate citations by title.
 *
 * @param {Array} citations - Citations array
 * @returns {Array} Deduplicated citations
 */
export function deduplicateCitations(citations) {
  const seen = new Set();
  return citations.filter(citation => {
    const key = citation.title.toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

/**
 * Process LLM response to extract and enrich all citations.
 *
 * @param {string} responseText - LLM response text
 * @param {Array} chunks - Retrieved chunks used for context
 * @returns {Object} Processed result with citations
 */
export function processCitations(responseText, chunks) {
  const extracted = extractCitations(responseText);
  const enriched = enrichCitations(extracted, chunks);
  const markdown = formatCitationsMarkdown(enriched);

  logger.info('Citations processed', {
    found: extracted.length,
    matched: enriched.filter(c => c.matched).length,
  });

  return {
    citations: enriched,
    markdown,
    stats: {
      total: extracted.length,
      matched: enriched.filter(c => c.matched).length,
      unmatched: enriched.filter(c => !c.matched).length,
    },
  };
}
