import { useEffect, useRef, useState } from 'react';
import mockReports from '../data/mockReports.json';
import RoomCard from './RoomCard.jsx';
import SafetyReport from './SafetyReport.jsx';
import './Dashboard.css';

function Dashboard() {
  const [rooms, setRooms] = useState([]);
  const [imageError, setImageError] = useState('');
  const [roomStates, setRoomStates] = useState({});
  const [selectedReport, setSelectedReport] = useState(null);
  const timers = useRef({});

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/images')
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Image request failed with status ${response.status}`);
        }

        return response.json();
      })
      .then((result) => {
        if (!Array.isArray(result.data)) {
          throw new Error('Image response did not include a data array');
        }

        setRooms(result.data.map((image) => {
          const roomNumber = image.room_number ?? image.image_id;
          const roomId = `room-${roomNumber}`;

          return {
            id: roomId,
            image: image.url || image.image_url,
            imageAlt: `Room ${roomNumber}`,
            title: `Room ${roomNumber}`,
            agents: [
              { name: 'Fall Safety Agent', status: 'Analyzing fall risks' },
              { name: 'Equipment Clearance Agent', status: 'Checking clearance' },
              { name: 'Patient-Care & Hygiene Agent', status: 'Reviewing care conditions' },
            ],
          };
        }));
      })
      .catch((error) => {
        console.error('Failed to load room images:', error);
        setImageError('Unable to load hospital rooms right now.');
      });
  }, []);

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
        {imageError ? (
          <p className="dashboard-error">{imageError}</p>
        ) : (
          rooms.map((room) => (
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
          ))
        )}
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