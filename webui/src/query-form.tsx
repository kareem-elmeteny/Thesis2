import { useState } from 'react';
import { queryAPI } from './query';

function formatTime(seconds: number): string {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes} minute(s) and ${remainingSeconds} second(s)`;
}


function QueryForm() {
    const [query, setQuery] = useState('');
    const [ragResult, setRagResult] = useState<string | null>(null);
    const [ragTime, setRagTime] = useState<number | null>(null);
    const [noRagTime, setNoRagTime] = useState<number | null>(null);
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
                setRagTime(null);
            } else {
                setRagResult(ragResponse.response || 'No response from RAG.');
                setRagTime(ragResponse.time_taken || null);
            }

            // Query without RAG
            const noRagResponse = await queryAPI({ query, RAG: false });
            if (noRagResponse.error) {
                setError(`No RAG Error: ${noRagResponse.error}`);
                setNoRagTime(null);
            } else {
                setNoRagResult(noRagResponse.response || 'No response from No RAG.');
                setNoRagTime(noRagResponse.time_taken || null);
            }
        } catch (err: any) {
            setError(err.message || 'An unknown error occurred.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit} className="my-4">
                <div className="mb-3">
                    <textarea
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Enter your query here..."
                        rows={5}
                        className="form-control"
                    />
                </div>
                <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                    {loading ? 'Loading...' : 'Submit'}
                </button>
            </form>

            {error && (
                <div className="alert alert-danger mt-3" role="alert">
                    {error}
                </div>
            )}

            <div className="mt-4">
                <h4>Result with RAG:</h4>
                <small className="text-muted">
                    {ragTime !== null ? `Time taken: ${formatTime(ragTime)}` : ''}
                </small>
                <div className="border p-3 rounded bg-light">
                    {ragResult || 'No result yet.'}
                </div>
            </div>

            <div className="mt-4">
                <h4>Result without RAG:</h4>
                <small className="text-muted">
                    {noRagTime !== null ? `Time taken: ${formatTime(noRagTime)}` : ''}
                </small>
                <div className="border p-3 rounded bg-light">
                    {noRagResult || 'No result yet.'}
                </div>
            </div>
        </>
    );
}

export default QueryForm;