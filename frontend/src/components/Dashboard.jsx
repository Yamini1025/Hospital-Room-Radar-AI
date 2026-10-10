import { useEffect, useRef, useState } from 'react';
import mockRooms from '../data/mockRooms.json';
import mockReports from '../data/mockReports.json';
import RoomCard from './RoomCard.jsx';
import SafetyReport from './SafetyReport.jsx';
import './Dashboard.css';

function Dashboard() {
  const rooms = mockRooms;
  const [roomStates, setRoomStates] = useState({});
  const [selectedReport, setSelectedReport] = useState(null);
  const timers = useRef({});

  useEffect(() => () => {
    Object.values(timers.current).forEach((timer) => window.clearTimeout(timer));
  }, []);

  const startAnalysis = (roomId) => {
    if (timers.current[roomId]) {
      window.clearTimeout(timers.current[roomId]);
    }

    setRoomStates((currentStates) => ({
      ...currentStates,
      [roomId]: 'loading',
    }));

    timers.current[roomId] = window.setTimeout(() => {
      setRoomStates((currentStates) => ({
        ...currentStates,
        [roomId]: 'completed',
      }));
      delete timers.current[roomId];
    }, 1500);
  };

  return (
    <section className="dashboard">
      <header className="dashboard-intro">
        <h1 className="dashboard-title">Hospital Rooms</h1>
        <p className="dashboard-description">
          Click any room card to initiate autonomous multi-agent analysis. The specialized agents evaluate
          fall safety, equipment clearance, and patient-care pathways before generating a consensus clinical
          report.
        </p>
      </header>

      <div className="dashboard-cards">
        {rooms.map((room) => (
          <RoomCard
            key={room.id}
            room={room}
            agents={room.agents.map((agent) => ({
              ...agent,
              state: roomStates[room.id] || 'pending',
            }))}
            onStartAnalysis={() => startAnalysis(room.id)}
            onViewReport={() => setSelectedReport(mockReports[room.id])}
            reportReady={roomStates[room.id] === 'completed'}
          />
        ))}
      </div>

      {selectedReport && (
        <SafetyReport
          report={selectedReport}
          onClose={() => setSelectedReport(null)}
        />
      )}
    </section>
  );
}

export default Dashboard;