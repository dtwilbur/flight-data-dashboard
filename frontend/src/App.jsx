import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FlightTable from './components/FlightTable.jsx';
import FlightDetails from './components/FlightDetails.jsx';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <header className="bg-blue-600 text-white p-4 shadow">
          <h1 className="text-2xl font-semibold">Flight Data Dashboard</h1>
        </header>
        <main className="flex-1 container mx-auto p-4">
          <Routes>
            <Route path="/" element={<FlightTable />} />
            <Route path="/flights/:id" element={<FlightDetails />} />
          </Routes>
        </main>
        <footer className="text-center py-4 text-sm text-gray-500">
          © {new Date().getFullYear()} Flight Data Dashboard
        </footer>
      </div>
    </Router>
  );
}

export default App;