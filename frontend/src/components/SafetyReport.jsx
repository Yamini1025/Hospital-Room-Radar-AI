import './SafetyReport.css';

function SafetyReport({ report, onClose }) {
  return (
    <div className="report-modal" role="presentation">
      <button className="report-backdrop" type="button" aria-label="Close report" onClick={onClose} />
      <section className="report-dialog" role="dialog" aria-modal="true" aria-labelledby="report-title">
        <header className="report-header">
          <div>
            <p className="report-label">AI SAFETY REPORT</p>
            <h2 id="report-title">{report.room}</h2>
            <p className="report-ward">{report.ward}</p>
          </div>
          <button className="report-close" type="button" aria-label="Close report" onClick={onClose}>
            ×
          </button>
        </header>

        <div className="report-content">
          <div className="report-confidence">
            <span>Analysis confidence</span>
            <strong>{report.confidence}</strong>
          </div>
          <p className="report-summary">{report.summary}</p>
          <p className="report-details">{report.details}</p>

          <h3>Agent findings</h3>
          <div className="report-findings">
            {report.findings.map((finding) => (
              <div className="finding" key={finding.label}>
                <span className={`finding-icon finding-${finding.tone}`} aria-hidden="true">
                  {finding.tone === 'success' ? '✓' : finding.tone === 'warning' ? '!' : '•'}
                </span>
                <div>
                  <strong>{finding.label}</strong>
                  <span>{finding.value}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="report-recommendation">
            <strong>Recommended action</strong>
            <p>{report.recommendation}</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default SafetyReport;