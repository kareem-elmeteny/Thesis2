import axios from 'axios';

interface QueryResponse {
    response?: string;
    error?: string;
}

interface QueryRequest {
    query: string;
    RAG: boolean;
}

const serverUrl = import.meta.env.VITE_RAG_SERVER;


export async function queryAPI(requestData: QueryRequest): Promise<QueryResponse> {
    const apiUrl = `${serverUrl}/query`;
    try {
        const response = await axios.post<QueryResponse>(apiUrl, requestData, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error: any) {
        if (error.response) {
            // Server responded with a status code outside the 2xx range
            return { error: error.response.data.error || 'An error occurred on the server.' };
        } else if (error.request) {
            // Request was made but no response was received
            return { error: 'No response received from the server.' };
        } else {
            // Something else happened
            return { error: error.message || 'An unknown error occurred.' };
        }
    }
}