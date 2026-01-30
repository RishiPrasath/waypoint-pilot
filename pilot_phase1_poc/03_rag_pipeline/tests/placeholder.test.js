/**
 * Placeholder test to verify Jest is working
 */

describe('Project Setup', () => {
  test('Jest is configured correctly', () => {
    expect(true).toBe(true);
  });

  test('Environment can be loaded', async () => {
    const { config } = await import('../src/config.js');
    expect(config.port).toBeDefined();
    expect(typeof config.port).toBe('number');
  });
});
