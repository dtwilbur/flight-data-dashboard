import axios from 'axios';

// Create an Axios instance with a base URL.  In development the Vite proxy
// rewrites `/api` to `http://localhost:8000`.  In production the frontend
// should be served behind a reverse proxy that forwards `/api` to the backend.
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchFlights = async () => {
  const response = await api.get('/flights');
  return response.data;
};

export const fetchFlight = async (id) => {
  const response = await api.get(`/flights/${id}`);
  return response.data;
};

export const fetchLatestPositions = async (limit = 10) => {
  const response = await api.get('/positions/latest', { params: { limit } });
  return response.data;
};

export default api;