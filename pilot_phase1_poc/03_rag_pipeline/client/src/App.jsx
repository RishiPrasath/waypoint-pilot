import { useState } from 'react';
import QueryInput from './components/QueryInput';
import Response from './components/Response';
import Loading from './components/Loading';
import { submitQuery } from './api/query';

/**
 * Main application component.
 * Manages state and orchestrates the query flow.
 */
function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (queryText) => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await submitQuery(queryText, controller.signal);
      setResponse(result);
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError(err.message || 'An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-3xl mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-sky-500 rounded-lg flex items-center justify-center">
              <svg
                className="w-5 h-5 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-lg font-semibold text-slate-900">
                Waypoint Co-Pilot
              </h1>
              <p className="text-sm text-slate-500">
                Customer Service Assistant
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-3xl mx-auto px-4 py-6 md:py-8">
        {/* Query Input */}
        <div className="mb-6">
          <QueryInput onSubmit={handleSubmit} loading={loading} />
        </div>

        {/* Response Area */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4 md:p-6">
          {loading ? (
            <Loading />
          ) : (
            <Response data={response} error={error} />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="max-w-3xl mx-auto px-4 py-6 text-center text-xs text-slate-400">
        Waypoint Phase 1 POC &bull; Powered by RAG Pipeline
      </footer>
    </div>
  );
}

export default App;
