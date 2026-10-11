import './SafetyReport.css';

function SafetyReport({ report, onClose }) {
  return (
    <div className="report-modal" role="presentation">
      <button
        className="report-backdrop"
        type="button"
        aria-label="Close report"
        onClick={onClose}
      />

      <section
        className="report-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="report-title"
      >
        <header className="report-header">
          <div>
            <p className="report-label">AI SAFETY REPORT</p>
            <h2 id="report-title">{report.room}</h2>
            <p className="report-ward">{report.ward}</p>
          </div>

          <button
            className="report-close"
            type="button"
            aria-label="Close report"
            onClick={onClose}
          >
            ×
          </button>
        </header>

        <div className="report-content">
          <div className="report-confidence">
            <span>Analysis status</span>
            <strong>{report.confidence}</strong>
          </div>

          <section className="report-overview">
            <h3>Summary</h3>
            <p className="report-summary">{report.summary}</p>
            <p className="report-details">{report.details}</p>
          </section>

          <h3 className="findings-heading">
            Findings <span>{report.findings.length}</span>
          </h3>

          <div className="report-findings">
            {report.findings.length === 0 ? (
              <div className="no-findings">
                <strong>No hazards flagged</strong>
                <p>
                  The AI agents did not report any clear hazards.
                  This does not certify the room as safe.
                </p>
              </div>
            ) : (
              report.findings.map((finding, index) => (
                <article
                  className="finding"
                  key={finding.key || `${finding.label}-${index}`}
                >
                  <div className="finding-heading">
                    <span className="finding-number">
                      {String(index + 1).padStart(2, '0')}
                    </span>
                    <h4>{finding.label}</h4>
                    <span
                      className={`risk-badge risk-${finding.risk.toLowerCase()}`}
                    >
                      {finding.risk} risk
                    </span>
                  </div>

                  <div className="finding-section">
                    <span className="finding-section-label">
                      EVIDENCE
                    </span>
                    <p>{finding.evidence}</p>
                  </div>

                  <div className="finding-section">
                    <span className="finding-section-label">
                      DETECTED BY
                    </span>
                    <div className="source-list">
                      {finding.sources.length ? (
                        finding.sources.map((source, sourceIndex) => (
                          <span
                            className="source-tag"
                            key={`${source}-${sourceIndex}`}
                          >
                            {source}
                          </span>
                        ))
                      ) : (
                        <span className="source-tag">AI analysis</span>
                      )}
                    </div>
                  </div>

                  <div className="finding-action">
                    <span className="finding-section-label">
                      RECOMMENDED ACTION
                    </span>
                    <p>{finding.action}</p>
                  </div>

                  <p className="finding-verification">
                    Human verification required
                  </p>
                </article>
              ))
            )}
          </div>

          <div className="report-recommendation">
            <strong>Next step</strong>
            <p>{report.recommendation}</p>
          </div>

          <p className="report-disclaimer">
            AI-assisted visual screening only. Verify findings against
            the actual room before taking action. This report does not
            certify room safety.
          </p>
        </div>
      </section>
    </div>
  );
}

export default SafetyReport;