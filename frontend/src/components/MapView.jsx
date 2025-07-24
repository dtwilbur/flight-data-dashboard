import React from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix default marker icon path for Leaflet in Vite environment
// eslint-disable-next-line
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

export default function MapView({ positions = [] }) {
  if (!positions.length) {
    return <p>No position data available.</p>;
  }
  // Compute map centre as the average of all coordinates
  const lats = positions.map((p) => p.latitude);
  const lons = positions.map((p) => p.longitude);
  const center = [
    lats.reduce((sum, v) => sum + v, 0) / lats.length,
    lons.reduce((sum, v) => sum + v, 0) / lons.length,
  ];
  // Create polyline positions
  const path = positions.map((p) => [p.latitude, p.longitude]);
  return (
    <MapContainer center={center} zoom={5} scrollWheelZoom={false} className="h-full w-full rounded">
      <TileLayer
        attribution="&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Polyline positions={path} color="blue" />
      {/* Start marker */}
      <Marker position={path[0]}>
        <Popup>Start</Popup>
      </Marker>
      {/* End marker */}
      <Marker position={path[path.length - 1]}>
        <Popup>End</Popup>
      </Marker>
    </MapContainer>
  );
}