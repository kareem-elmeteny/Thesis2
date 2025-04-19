import { useState } from 'react';
import { queryAPI } from './query';

function QueryForm() {
    const [query, setQuery] = useState('');
    const [ragResult, setRagResult] = useState<string | null>(null);
    const [noRagResult, setNoRagResult] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setRagResult(null);
        setNoRagResult(null);
        setLoading(true);

        try {
            // Query with RAG
            const ragResponse = await queryAPI({ query, RAG: true });
            if (ragResponse.error) {
                setError(`RAG Error: ${ragResponse.error}`);
            } else {
                setRagResult(ragResponse.response || 'No response from RAG.');
            }

            // Query without RAG
            const noRagResponse = await queryAPI({ query, RAG: false });
            if (noRagResponse.error) {
                setError(`No RAG Error: ${noRagResponse.error}`);
            } else {
                setNoRagResult(noRagResponse.response || 'No response from No RAG.');
            }
        } catch (err: any) {
            setError(err.message || 'An unknown error occurred.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Enter your query here..."
                    rows={5}
                    style={{ width: '100%' }}
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Loading...' : 'Submit'}
                </button>
            </form>

            {error && <div style={{ color: 'red', marginTop: '1rem' }}>Error: {error}</div>}

            <div style={{ marginTop: '1rem' }}>
                <h3>Result With RAG:</h3>
                <div style={{ border: '1px solid #ccc', padding: '1rem' }}>
                    {ragResult || 'No result yet.'}
                </div>
            </div>

            <div style={{ marginTop: '1rem' }}>
                <h3>Result Without RAG:</h3>
                <div style={{ border: '1px solid #ccc', padding: '1rem' }}>
                    {noRagResult || 'No result yet.'}
                </div>
            </div>
        </div>
    );
};

export default QueryForm;