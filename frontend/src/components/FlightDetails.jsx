import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchFlight } from '../api.js';
import MapView from './MapView.jsx';
import ChartView from './ChartView.jsx';

function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleString();
}

export default function FlightDetails() {
  const { id } = useParams();
  const [flight, setFlight] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchFlight(id);
        setFlight(data);
      } catch (err) {
        setError(err.message || 'Failed to load flight');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  if (loading) return <p>Loading flight…</p>;
  if (error) return <p className="text-red-600">Error: {error}</p>;
  if (!flight) return <p>Flight not found</p>;

  return (
    <div className="space-y-6">
      <div>
        <Link to="/" className="text-blue-600 hover:underline">← Back to flights</Link>
      </div>
      <div className="bg-white shadow rounded p-4">
        <h2 className="text-xl font-semibold mb-2">Flight {flight.callsign || flight.id}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <p><span className="font-medium">Departure:</span> {flight.departure || 'N/A'}</p>
            <p><span className="font-medium">Arrival:</span> {flight.arrival || 'N/A'}</p>
            <p><span className="font-medium">First Seen:</span> {formatDate(flight.first_seen)}</p>
            <p><span className="font-medium">Last Seen:</span> {formatDate(flight.last_seen)}</p>
          </div>
          <div>
            <p><span className="font-medium">Number of Positions:</span> {flight.positions.length}</p>
          </div>
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-white shadow rounded p-4 h-96">
          <h3 className="font-semibold mb-2">Flight Path</h3>
          <MapView positions={flight.positions} />
        </div>
        <div className="bg-white shadow rounded p-4 h-96">
          <h3 className="font-semibold mb-2">Altitude & Speed</h3>
          <ChartView positions={flight.positions} />
        </div>
      </div>
    </div>
  );
}