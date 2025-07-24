import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchFlights } from '../api.js';

function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleString();
}

export default function FlightTable() {
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchFlights();
        setFlights(data);
      } catch (err) {
        setError(err.message || 'Failed to load flights');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <p>Loading flights…</p>;
  if (error) return <p className="text-red-600">Error: {error}</p>;

  return (
    <div className="overflow-x-auto">
      <h2 className="text-xl font-semibold mb-4">Flights</h2>
      <table className="min-w-full divide-y divide-gray-300 bg-white shadow rounded">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">ID</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Callsign</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Departure</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Arrival</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">First Seen</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Last Seen</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {flights.map((flight) => (
            <tr key={flight.id} className="hover:bg-gray-50">
              <td className="px-4 py-2">
                <Link to={`/flights/${flight.id}`} className="text-blue-600 hover:underline">
                  {flight.id}
                </Link>
              </td>
              <td className="px-4 py-2">{flight.callsign}</td>
              <td className="px-4 py-2">{flight.departure}</td>
              <td className="px-4 py-2">{flight.arrival}</td>
              <td className="px-4 py-2">{formatDate(flight.first_seen)}</td>
              <td className="px-4 py-2">{formatDate(flight.last_seen)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}