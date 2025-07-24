import React from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

export default function ChartView({ positions = [] }) {
  if (!positions.length) return <p>No chart data available.</p>;
  // Sort positions by timestamp
  const sorted = [...positions].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  const labels = sorted.map((p) => new Date(p.timestamp).toLocaleTimeString());
  const altitudes = sorted.map((p) => (p.altitude != null ? p.altitude : null));
  const speeds = sorted.map((p) => (p.speed != null ? p.speed : null));
  const data = {
    labels,
    datasets: [
      {
        label: 'Altitude (m)',
        data: altitudes,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        yAxisID: 'y1',
      },
      {
        label: 'Speed (knots)',
        data: speeds,
        borderColor: 'rgb(234, 88, 12)',
        backgroundColor: 'rgba(234, 88, 12, 0.5)',
        yAxisID: 'y2',
      },
    ],
  };
  const options = {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    stacked: false,
    scales: {
      y1: {
        type: 'linear',
        display: true,
        position: 'left',
        title: { display: true, text: 'Altitude (m)' },
      },
      y2: {
        type: 'linear',
        display: true,
        position: 'right',
        grid: {
          drawOnChartArea: false,
        },
        title: { display: true, text: 'Speed (knots)' },
      },
    },
  };
  return <Line data={data} options={options} />;
}