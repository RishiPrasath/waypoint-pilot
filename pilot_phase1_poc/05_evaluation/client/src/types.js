/**
 * Shared JSDoc type definitions for the Waypoint frontend.
 * These typedefs document the API response shape used across components.
 *
 * @module types
 */

/**
 * @typedef {Object} Source
 * @property {string} title - Document title
 * @property {string} org - Source organization name
 * @property {string} url - External URL
 * @property {string|null} section - Document section, if applicable
 */

/**
 * @typedef {Object} RelatedDoc
 * @property {string} title - Document title
 * @property {string} category - Category key: "regulatory" | "carrier" | "internal" | "reference"
 * @property {string} docId - Unique document identifier
 * @property {string|null} url - External URL, or null for internal docs
 */

/**
 * @typedef {Object} Confidence
 * @property {"High"|"Medium"|"Low"} level - Confidence level
 * @property {string} reason - Explanation for the confidence level
 */

/**
 * @typedef {Object} ResponseMetadata
 * @property {string} query - Original query text
 * @property {number} chunksRetrieved - Total chunks retrieved from ChromaDB
 * @property {number} chunksUsed - Chunks matched by citation extraction
 * @property {number} latencyMs - Total pipeline latency in milliseconds
 * @property {string} model - LLM model identifier
 */

/**
 * @typedef {Object} QueryResponse
 * @property {string} answer - LLM-generated markdown answer
 * @property {Source[]} sources - External source URLs for the Sources section
 * @property {RelatedDoc[]} relatedDocs - Related documents for the Related Docs section
 * @property {Object[]} citations - Raw matched citations (internal use)
 * @property {Confidence} confidence - Confidence assessment
 * @property {ResponseMetadata} metadata - Pipeline metadata and stats
 */
