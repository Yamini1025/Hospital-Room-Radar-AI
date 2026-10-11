import { useEffect, useState } from 'react';
import './RoomCard.css';

const defaultAgents = [
  { name: 'Fall Safety', state: 'loading', status: 'Analyzing fall risks' },
  { name: 'Infection and Hygiene', state: 'loading', status: 'Checking infection and hygiene risks' },
  { name: 'Equipment Readiness', state: 'loading', status: 'Checking equipment readiness' },
];

function AgentStateIcon({ state }) {
  if (state === 'completed') {
    return <span className="agent-icon agent-success" aria-label="Completed">✓</span>;
  }

  if (state === 'error') {
    return <span className="agent-icon agent-error" aria-label="Error">×</span>;
  }

  if (state === 'loading') {
    return <span className="agent-spinner" aria-label="Loading" />;
  }

  return <span className="agent-pending" aria-label="Not started" />;
}

function RoomCard({
  room = {},
  agents = defaultAgents,
  onViewReport,
  onStartAnalysis,
  reportReady = false,
}) {
  const [isImageOpen, setIsImageOpen] = useState(false);

  useEffect(() => {
    if (!isImageOpen) {
      return undefined;
    }

    function handleKeyDown(event) {
      if (event.key === 'Escape') {
        setIsImageOpen(false);
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isImageOpen]);

  const imageAlt = room.imageAlt || room.title || 'Hospital room';

  return (
    <>
      <article className="room-card">
        <button
          className="room-image-wrap"
          type="button"
          onClick={() => setIsImageOpen(true)}
          aria-label={`Open ${imageAlt} for closer inspection`}
        >
          <img className="room-image" src={room.image} alt={imageAlt} />
        </button>

        <h2 className="room-title">{room.title || 'Evaluating Room Geometry'}</h2>

        <div className="room-agents" aria-label="AI agent loading states">
          {agents.map((agent) => (
            <div className="agent-status" key={agent.name}>
              <AgentStateIcon state={agent.state} />
              <span className="agent-name">{agent.name}</span>
              <span className="agent-state">{agent.status}</span>
            </div>
          ))}
        </div>

        <div className="room-actions">
          <button
            className="room-button room-button-secondary"
            type="button"
            onClick={onViewReport}
            disabled={!reportReady}
          >
            View Report
          </button>
          <button className="room-button room-button-primary" type="button" onClick={onStartAnalysis}>
            Start Analysis
          </button>
        </div>
      </article>

      {isImageOpen && (
        <div
          className="image-modal"
          role="dialog"
          aria-modal="true"
          aria-label={`${imageAlt} full image`}
          onClick={() => setIsImageOpen(false)}
        >
          <div className="image-modal-content" onClick={(event) => event.stopPropagation()}>
            <button
              className="image-modal-close"
              type="button"
              onClick={() => setIsImageOpen(false)}
              aria-label="Close image"
            >
              ×
            </button>
            <img className="image-modal-image" src={room.image} alt={imageAlt} />
          </div>
        </div>
      )}
    </>
  );
}

export default RoomCard;