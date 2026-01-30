/**
 * Jest setup file
 * Runs before all tests to configure the test environment.
 */

// Set test environment
process.env.NODE_ENV = 'test';
process.env.PORT = '3001';

// Note: Jest timeout is configured in jest.config.js for ES modules
