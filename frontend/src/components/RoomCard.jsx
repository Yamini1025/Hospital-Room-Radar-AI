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
  riskStatus,
}) {
  return (
    <article className="room-card">
      <div className="room-card-heading">
        <h2 className="room-title">{room.title || 'Evaluating Room Geometry'}</h2>
        {reportReady && riskStatus && (
          <span className={`room-risk-badge room-risk-${riskStatus.replace(' ', '-')}`}>
            {riskStatus}
          </span>
        )}
      </div>

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
  );
}

export default RoomCard;