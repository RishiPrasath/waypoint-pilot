/**
 * Structured logging utility
 * Provides consistent logging format across the application.
 */

import { config } from '../config.js';

/**
 * Log levels
 */
const LOG_LEVELS = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

/**
 * Get current log level from environment
 */
const currentLevel = LOG_LEVELS[process.env.LOG_LEVEL || 'info'] || LOG_LEVELS.info;

/**
 * Format a log message with timestamp and level
 *
 * @param {string} level - Log level
 * @param {string} message - Log message
 * @param {Object} data - Additional data to log
 * @returns {string} Formatted log string
 */
function formatLog(level, message, data = {}) {
  const timestamp = new Date().toISOString();
  const logObj = {
    timestamp,
    level: level.toUpperCase(),
    message,
    ...data,
  };

  if (config.nodeEnv === 'development') {
    return `[${timestamp}] ${level.toUpperCase()}: ${message} ${Object.keys(data).length ? JSON.stringify(data) : ''}`;
  }

  return JSON.stringify(logObj);
}

/**
 * Logger object with level methods
 */
export const logger = {
  /**
   * Debug level log
   * @param {string} message - Log message
   * @param {Object} data - Additional data
   */
  debug(message, data = {}) {
    if (currentLevel <= LOG_LEVELS.debug) {
      console.log(formatLog('debug', message, data));
    }
  },

  /**
   * Info level log
   * @param {string} message - Log message
   * @param {Object} data - Additional data
   */
  info(message, data = {}) {
    if (currentLevel <= LOG_LEVELS.info) {
      console.log(formatLog('info', message, data));
    }
  },

  /**
   * Warning level log
   * @param {string} message - Log message
   * @param {Object} data - Additional data
   */
  warn(message, data = {}) {
    if (currentLevel <= LOG_LEVELS.warn) {
      console.warn(formatLog('warn', message, data));
    }
  },

  /**
   * Error level log
   * @param {string} message - Log message
   * @param {Object} data - Additional data
   */
  error(message, data = {}) {
    if (currentLevel <= LOG_LEVELS.error) {
      console.error(formatLog('error', message, data));
    }
  },
};
