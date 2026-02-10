/**
 * Citation Extractor Service
 * Parses and enriches citations from LLM responses.
 */

import { logger } from '../utils/logger.js';

/**
 * Citation pattern for extracting references from text.
 * Only supports [Title] and [Title > Section] bracket format.
 * The system prompt enforces this format; no fallback patterns needed.
 */
const CITATION_PATTERN = /\[([^\]]+)\]/g;

/**
 * Similarity threshold for fuzzy matching (lowered from 0.7 for better recall)
 */
const SIMILARITY_THRESHOLD = 0.5;

/**
 * Extract citations from LLM response text.
 * Only extracts [Title] and [Title > Section] bracket-format citations.
 * The system prompt enforces this format, so no fallback patterns are needed.
 *
 * @param {string} text - LLM response text
 * @returns {Array<Object>} Extracted citations with text and position
 */
export function extractCitations(text) {
  const citations = [];
  const seenTitles = new Set();
  let match;

  // [Title] or [Title > Section]
  while ((match = CITATION_PATTERN.exec(text)) !== null) {
    const fullMatch = match[0];
    const content = match[1];

    // Parse title and section
    const parts = content.split('>').map(p => p.trim());
    const title = parts[0];
    const section = parts[1] || null;

    // Skip if we've already seen this title
    if (!seenTitles.has(title.toLowerCase())) {
      seenTitles.add(title.toLowerCase());
      citations.push({
        raw: fullMatch,
        title,
        section,
        position: match.index,
      });
    }
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

  // Try partial/fuzzy match with lowered threshold for better recall
  match = chunks.find(chunk => {
    const chunkTitle = chunk.metadata?.title?.toLowerCase() || '';
    const citationTitle = citation.title.toLowerCase();

    return chunkTitle.includes(citationTitle) ||
           citationTitle.includes(chunkTitle) ||
           similarity(chunkTitle, citationTitle) > SIMILARITY_THRESHOLD;
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
      .map(u => u.trim())
      .filter(u => u && u !== 'N/A' && u.startsWith('http')) || [];

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
 * Category prefix mapping from KB folder names to frontend category names.
 */
const CATEGORY_MAP = {
  '01_regulatory': 'regulatory',
  '02_carriers': 'carrier',
  '03_reference': 'reference',
  '04_internal_synthetic': 'internal',
};

/**
 * Build sources array for the frontend Sources section.
 * Extracts external URLs from matched citations' chunk metadata.
 *
 * @param {Array} enrichedCitations - Enriched citations from enrichCitations()
 * @param {Array} chunks - Retrieved chunks with metadata
 * @returns {Array<{title: string, org: string, url: string, section: string|null}>}
 */
export function buildSources(enrichedCitations, chunks) {
  const sources = [];
  const seenUrls = new Set();

  for (const citation of enrichedCitations) {
    if (!citation.matched || !citation.sourceUrls || citation.sourceUrls.length === 0) {
      continue;
    }

    // Find the matched chunk to get source_org
    const matchedChunk = chunks.find(c =>
      c.metadata?.doc_id === citation.docId
    );
    const org = matchedChunk?.metadata?.source_org || '';

    for (const url of citation.sourceUrls) {
      if (seenUrls.has(url)) continue;
      seenUrls.add(url);

      sources.push({
        title: citation.fullTitle || citation.title,
        org,
        url,
        section: citation.section || null,
      });
    }
  }

  return sources;
}

/**
 * Build relatedDocs array for the frontend Related Documents section.
 * Extracts unique parent documents from all retrieved chunks.
 *
 * @param {Array} chunks - All retrieved chunks with metadata
 * @returns {Array<{title: string, category: string, docId: string, url: string|null}>}
 */
export function buildRelatedDocs(chunks) {
  const docs = [];
  const seenDocIds = new Set();

  for (const chunk of chunks) {
    const docId = chunk.metadata?.doc_id;
    if (!docId || seenDocIds.has(docId)) continue;
    seenDocIds.add(docId);

    const rawCategory = chunk.metadata?.category || '';
    const category = CATEGORY_MAP[rawCategory] || rawCategory;

    const sourceUrls = chunk.metadata?.source_urls
      ?.split(',')
      .map(u => u.trim())
      .filter(u => u && u !== 'N/A' && u.startsWith('http')) || [];

    docs.push({
      title: chunk.metadata?.title || 'Unknown Document',
      category,
      docId,
      url: sourceUrls.length > 0 ? sourceUrls[0] : null,
    });
  }

  return docs;
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
