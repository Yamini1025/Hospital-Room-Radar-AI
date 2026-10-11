import { useEffect, useState } from 'react';
import { fetchRooms, analyzeRoom } from '../api/rooms.js';
import RoomCard from './RoomCard.jsx';
import SafetyReport from './SafetyReport.jsx';
import './Dashboard.css';

function getRiskStatus(findings, hasErrors) {
  if (hasErrors) {
    return null;
  }

  if (findings.length === 0) {
    return 'safe';
  }

  const hasHighRiskFinding = findings.some((finding) =>
    String(finding.risk_level || '').trim().toLowerCase().startsWith('high')
  );

  return hasHighRiskFinding ? 'high risk' : 'low risk';
}

function Dashboard() {
  const [rooms, setRooms] = useState([]);
  const [imageError, setImageError] = useState('');
  const [roomStates, setRoomStates] = useState({});
  const [analysisErrors, setAnalysisErrors] = useState({});
  const [reports, setReports] = useState({});
  const [selectedReport, setSelectedReport] = useState(null);

  useEffect(() => {
    fetchRooms()
      .then((result) => {
        if (!Array.isArray(result.data)) {
          throw new Error('Invalid room image response');
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
              { name: 'Fall Safety', status: 'Checking fall risks' },
              { name: 'Infection and Hygiene', status: 'Checking infection and hygiene risks' },
              { name: 'Equipment Readiness', status: 'Checking equipment readiness' },
            ],
          };
        }));
      })
      .catch((error) => {
        console.error(error);
        setImageError('Unable to load hospital rooms right now.');
      });
  }, []);

  async function startAnalysis(room) {
    setRoomStates((current) => ({
      ...current,
      [room.id]: 'loading',
    }));

    setAnalysisErrors((current) => ({
      ...current,
      [room.id]: '',
    }));

    try {
      const response = await analyzeRoom(room.id);
      const result = response.result;
      const finalReport = result.final_report;

      const rawFindings =
        finalReport?.findings ?? result.findings ?? [];
      const hasAgentErrors = Object.keys(result.errors || {}).length > 0;

      const report = {
        room: room.title,
        ward: 'AI-generated safety assessment',
        image: room.image,
        imageAlt: room.imageAlt || room.title,
        riskStatus: getRiskStatus(rawFindings, hasAgentErrors),
        confidence: hasAgentErrors
          ? 'Incomplete — human review required'
          : (result.needs_verification
            ? 'Human verification required'
            : 'No findings flagged; room not certified safe'),
        summary: finalReport?.overall_summary
          || result.message
          || 'Analysis completed.',
        details: hasAgentErrors
          ? `Some agents failed: ${Object.entries(result.errors)
              .map(([agent, error]) => `${agent}: ${error}`)
              .join('; ')}`
          : 'AI-generated assessment. Verify findings before taking action.',
        findings: rawFindings.map((finding, index) => ({
          label: finding.hazard || 'Unspecified finding',
          risk: finding.risk_level || 'Unrated',
          evidence: finding.evidence || 'No supporting evidence provided.',
          sources: (
            finding.source_agents ||
            [finding.source_agent]
          ).filter(Boolean),
          action: finding.recommended_action ||
            'Review this finding manually.',
          key: `${finding.hazard || 'finding'}-${index}`,
        })),
        recommendation: rawFindings.length
          ? 'Review each finding and verify it against the room image before taking action.'
          : 'No clear hazards were reported by the agents. This does not certify the room as safe.',
      };

      setReports((current) => ({
        ...current,
        [room.id]: report,
      }));

      setRoomStates((current) => ({
        ...current,
        [room.id]: 'completed',
      }));
    } catch (error) {
      console.error('Room analysis failed:', error);

      setAnalysisErrors((current) => ({
        ...current,
        [room.id]: error.message,
      }));

      setRoomStates((current) => ({
        ...current,
        [room.id]: 'error',
      }));
    }
  }

  return (
    <section className="dashboard">
      <header className="dashboard-intro">
        <h1 className="dashboard-title">Hospital Rooms</h1>
        <p className="dashboard-description">
          Analyze hospital room images with specialized AI agents
          and review their findings in a combined safety report.
        </p>
      </header>

      <div className="dashboard-cards">
        {imageError ? (
          <p className="dashboard-error">{imageError}</p>
        ) : (
          rooms.map((room) => (
            <div key={room.id}>
              <RoomCard
                room={room}
                agents={room.agents.map((agent) => ({
                  ...agent,
                  state: roomStates[room.id] || 'pending',
                }))}
                onStartAnalysis={() => startAnalysis(room)}
                onViewReport={() => setSelectedReport(reports[room.id])}
                reportReady={roomStates[room.id] === 'completed'}
                riskStatus={reports[room.id]?.riskStatus}
              />

              {analysisErrors[room.id] && (
                <p className="dashboard-error">
                  Analysis failed: {analysisErrors[room.id]}
                </p>
              )}
            </div>
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
