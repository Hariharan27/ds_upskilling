import { useEffect, useMemo, useState } from 'react'

import './App.css'
import {
  getHealthHistory,
  getProjectHealth,
  getProjects,
  getWeeklyHealthSummary,
  refreshProjectHealth,
  type HealthHistoryResponse,
  type Project,
  type ProjectHealthResponse,
  type WeeklyHealthSummaryResponse,
} from './services/healthApi'

function App() {
  const [projects, setProjects] = useState<Project[]>([])
  const [projectId, setProjectId] = useState('')
  const [health, setHealth] =
    useState<ProjectHealthResponse | null>(null)
  const [history, setHistory] =
    useState<HealthHistoryResponse | null>(null)
  const [weeklySummary, setWeeklySummary] =
    useState<WeeklyHealthSummaryResponse | null>(null)

  const [selectedWeek, setSelectedWeek] = useState('')
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [projectsLoading, setProjectsLoading] = useState(true)
  const [weeklySummaryLoading, setWeeklySummaryLoading] =
    useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadProjectData = async (selectedProjectId: string) => {
    try {
      setLoading(true)
      setError(null)

      const [healthResult, historyResult] = await Promise.all([
        getProjectHealth(selectedProjectId),
        getHealthHistory(selectedProjectId),
      ])

      setHealth(healthResult)
      setHistory(historyResult)
    } catch (err) {
      setHealth(null)
      setHistory(null)
      setWeeklySummary(null)

      setError(
        err instanceof Error
          ? err.message
          : 'Failed to load project health',
      )
    } finally {
      setLoading(false)
    }
  }

  const loadProjects = async () => {
    try {
      setProjectsLoading(true)
      setError(null)

      const projectResults = await getProjects()

      setProjects(projectResults)

      if (projectResults.length === 0) {
        setProjectId('')
        setHealth(null)
        setHistory(null)
        setWeeklySummary(null)
        return
      }

      setProjectId((currentProjectId) => {
        if (
          currentProjectId &&
          projectResults.some(
            (project) =>
              project.project_id === currentProjectId,
          )
        ) {
          return currentProjectId
        }

        return projectResults[0].project_id
      })
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to load projects',
      )
    } finally {
      setProjectsLoading(false)
    }
  }

  const handleRefresh = async () => {
    if (!projectId) {
      return
    }

    try {
      setRefreshing(true)
      setError(null)

      const [healthResult, historyResult] = await Promise.all([
        refreshProjectHealth(projectId),
        getHealthHistory(projectId),
      ])

      setHealth(healthResult)
      setHistory(historyResult)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to refresh project health',
      )
    } finally {
      setRefreshing(false)
    }
  }

  useEffect(() => {
    void loadProjects()
  }, [])

  useEffect(() => {
    if (!projectId || projectsLoading) {
      return
    }

    void loadProjectData(projectId)
  }, [projectId, projectsLoading])

  const risks = health?.risks ?? []

  const highRisks = risks.filter(
    (risk) => risk.severity.toLowerCase() === 'high',
  ).length

  const mediumRisks = risks.filter(
    (risk) => risk.severity.toLowerCase() === 'medium',
  ).length

  const lowRisks = risks.filter(
    (risk) => risk.severity.toLowerCase() === 'low',
  ).length

  const healthScore = health?.health_score
  const healthStatus = health?.health_status
  const historyPoints = history?.points ?? []

  const chartWidth = 760
  const chartHeight = 220

  const chartPadding = {
    top: 20,
    right: 24,
    bottom: 38,
    left: 42,
  }

  const chartInnerWidth =
    chartWidth -
    chartPadding.left -
    chartPadding.right

  const chartInnerHeight =
    chartHeight -
    chartPadding.top -
    chartPadding.bottom

  const chartMinScore = 0
  const chartMaxScore = 100

  const getChartX = (index: number) => {
    if (historyPoints.length <= 1) {
      return (
        chartPadding.left +
        chartInnerWidth / 2
      )
    }

    return (
      chartPadding.left +
      (index / (historyPoints.length - 1)) *
        chartInnerWidth
    )
  }

  const getChartY = (score: number) => {
    const normalized =
      (score - chartMinScore) /
      (chartMaxScore - chartMinScore)

    return (
      chartPadding.top +
      chartInnerHeight -
      normalized * chartInnerHeight
    )
  }

  const chartPoints = historyPoints.map(
    (point, index) => ({
      ...point,
      x: getChartX(index),
      y: getChartY(point.score),
    }),
  )

  const chartLine = chartPoints
    .map((point) => `${point.x},${point.y}`)
    .join(' ')

  const chartArea = [
    `${chartPadding.left},${
      chartPadding.top + chartInnerHeight
    }`,
    ...chartPoints.map(
      (point) => `${point.x},${point.y}`,
    ),
    `${chartPadding.left + chartInnerWidth},${
      chartPadding.top + chartInnerHeight
    }`,
  ].join(' ')

  const healthProgress =
    healthScore !== undefined
      ? `${healthScore}%`
      : '0%'

  const selectedProject = projects.find(
    (project) => project.project_id === projectId,
  )

  const availableWeeks = useMemo(() => {
    const weekMap = new Map<
      string,
      {
        start: Date
        end: Date
      }
    >()

    for (const point of historyPoints) {
      const date = new Date(point.calculated_at)

      if (Number.isNaN(date.getTime())) {
        continue
      }

      const day = date.getDay()
      const daysFromMonday = day === 0 ? 6 : day - 1

      const start = new Date(date)
      start.setHours(0, 0, 0, 0)
      start.setDate(
        start.getDate() - daysFromMonday,
      )

      const end = new Date(start)
      end.setDate(end.getDate() + 6)
      end.setHours(23, 59, 59, 999)

      const key = start.toISOString()

      if (!weekMap.has(key)) {
        weekMap.set(key, {
          start,
          end,
        })
      }
    }

    return Array.from(weekMap.values()).sort(
      (a, b) =>
        b.start.getTime() -
        a.start.getTime(),
    )
  }, [historyPoints])

  useEffect(() => {
    if (availableWeeks.length === 0) {
      setSelectedWeek('')
      setWeeklySummary(null)
      return
    }

    setSelectedWeek((currentWeek) => {
      if (
        currentWeek &&
        availableWeeks.some(
          (week) =>
            week.start.toISOString() ===
            currentWeek,
        )
      ) {
        return currentWeek
      }

      return availableWeeks[0].start.toISOString()
    })
  }, [availableWeeks])

  useEffect(() => {
    if (!projectId || !selectedWeek) {
      setWeeklySummary(null)
      return
    }

    const selectedWeekRange = availableWeeks.find(
      (week) =>
        week.start.toISOString() === selectedWeek,
    )

    if (!selectedWeekRange) {
      return
    }

    const loadWeeklySummary = async () => {
      try {
        setWeeklySummaryLoading(true)
        setError(null)

        const result =
          await getWeeklyHealthSummary(
            projectId,
            selectedWeekRange.start,
            selectedWeekRange.end,
          )

        setWeeklySummary(result)
      } catch (err) {
        setWeeklySummary(null)

        setError(
          err instanceof Error
            ? err.message
            : 'Failed to load weekly health summary',
        )
      } finally {
        setWeeklySummaryLoading(false)
      }
    }

    void loadWeeklySummary()
  }, [
    projectId,
    selectedWeek,
    availableWeeks,
  ])

  const formatWeekRange = (
    start: Date,
    end: Date,
  ) => {
    const startLabel =
      start.toLocaleDateString(
        'en-IN',
        {
          day: '2-digit',
          month: 'short',
        },
      )

    const endLabel =
      end.toLocaleDateString(
        'en-IN',
        {
          day: '2-digit',
          month: 'short',
          year: 'numeric',
        },
      )

    return `${startLabel} – ${endLabel}`
  }

  const selectedWeekRange =
    availableWeeks.find(
      (week) =>
        week.start.toISOString() === selectedWeek,
    )

  return (
    <div className="app">
      <header className="app-header">
        <div className="brand">
          <div className="brand-mark">AI</div>

          <div>
            <h1>AI Project Health Monitor</h1>
            <p>
              Project health, risks, and actionable insights
            </p>
          </div>
        </div>

        <div className="header-actions">
          <div className="project-selector">
            <span className="label">PROJECT</span>

            <select
              value={projectId}
              onChange={(event) => {
                setProjectId(event.target.value)
              }}
              disabled={
                projectsLoading ||
                refreshing ||
                projects.length === 0
              }
              aria-label="Select project"
            >
              {projects.length === 0 ? (
                <option value="">
                  {projectsLoading
                    ? 'Loading projects...'
                    : 'No projects available'}
                </option>
              ) : (
                projects.map((project) => (
                  <option
                    key={project.project_id}
                    value={project.project_id}
                  >
                    {project.project_id}
                  </option>
                ))
              )}
            </select>
          </div>

          <button
            type="button"
            className="refresh-button"
            onClick={() => void handleRefresh()}
            disabled={
              refreshing ||
              loading ||
              !projectId
            }
          >
            <span
              className={
                refreshing
                  ? 'refresh-icon spinning'
                  : 'refresh-icon'
              }
            >
              ↻
            </span>

            {refreshing
              ? 'Analyzing...'
              : 'Refresh'}
          </button>
        </div>
      </header>

      <main className="dashboard">
        <section className="project-header">
          <div className="project-identity">
            <span className="label">PROJECT</span>

            <h2>
              {selectedProject?.project_id ??
                (projectId || 'No project selected')}
            </h2>

            <span className="project-name">
              {selectedProject
                ? 'Monitored project'
                : 'Select a project to view health'}
            </span>
          </div>

          <div className="project-status">
            <span className="status-dot" />
            <span>Active</span>
          </div>

          <div className="last-analyzed">
            <span className="label">
              LAST ANALYZED
            </span>

            <span>
              {health
                ? 'Health data loaded'
                : 'Not analyzed yet'}
            </span>
          </div>
        </section>

        {error && (
          <section className="error-banner">
            <strong>
              Unable to load project health
            </strong>

            <span>{error}</span>
          </section>
        )}

        <section className="health-overview">
          <div className="health-card">
            <div className="health-card-content">
              <span className="label">
                CURRENT HEALTH SCORE
              </span>

              <div className="health-score-line">
                <span className="health-score">
                  {loading
                    ? '--'
                    : healthScore ?? '--'}
                </span>

                <span className="health-max">
                  / 100
                </span>
              </div>

              <div className="health-status">
                <span className="status-warning-icon">
                  ⚠
                </span>

                {loading
                  ? 'Loading...'
                  : healthStatus ??
                    'Waiting for analysis'}
              </div>

              <p className="health-description">
                {healthScore !== undefined
                  ? 'Project health is being monitored based on current project evidence.'
                  : 'Run the monitoring pipeline to calculate project health.'}
              </p>
            </div>

            <div
              className="health-ring"
              style={
                {
                  '--health-progress':
                    healthProgress,
                } as React.CSSProperties
              }
            >
              <div className="health-ring-inner">
                <strong>
                  {loading
                    ? '--'
                    : healthScore ?? '--'}
                </strong>
              </div>
            </div>
          </div>

          <div className="metric-card metric-high">
            <div className="metric-icon">!</div>

            <div className="metric-content">
              <span className="label">
                HIGH RISKS
              </span>

              <strong>
                {loading ? '--' : highRisks}
              </strong>

              <span className="metric-description">
                Requires immediate attention
              </span>
            </div>

            <span className="metric-arrow">›</span>
          </div>

          <div className="metric-card metric-medium">
            <div className="metric-icon">!</div>

            <div className="metric-content">
              <span className="label">
                MEDIUM RISKS
              </span>

              <strong>
                {loading ? '--' : mediumRisks}
              </strong>

              <span className="metric-description">
                Need monitoring and mitigation
              </span>
            </div>

            <span className="metric-arrow">›</span>
          </div>

          <div className="metric-card metric-low">
            <div className="metric-icon">✓</div>

            <div className="metric-content">
              <span className="label">
                LOW RISKS
              </span>

              <strong>
                {loading ? '--' : lowRisks}
              </strong>

              <span className="metric-description">
                Currently under control
              </span>
            </div>

            <span className="metric-arrow">›</span>
          </div>
        </section>

        <section className="dashboard-section">
          <div className="section-header">
            <div>
              <span className="label">
                PROJECT RISKS
              </span>

              <h2>Current Risks</h2>
            </div>
          </div>

          {loading ? (
            <div className="empty-state">
              <p>Loading project risks...</p>
            </div>
          ) : risks.length === 0 ? (
            <div className="empty-state">
              <p>No active risks detected.</p>

              <span>
                The latest project analysis did not
                identify any active risk signals.
              </span>
            </div>
          ) : (
            <div className="risk-list">
              {risks.map((risk) => {
                const severity =
                  risk.severity.toLowerCase()

                const riskIcon =
                  risk.risk_type.toLowerCase() ===
                  'delay'
                    ? '◈'
                    : risk.risk_type.toLowerCase() ===
                        'blocker'
                      ? '▣'
                      : risk.risk_type.toLowerCase() ===
                          'client_sentiment'
                        ? '♧'
                        : risk.risk_type.toLowerCase() ===
                            'scope_creep'
                          ? '◌'
                          : '•'

                return (
                  <article
                    className={`risk-card risk-card-${severity}`}
                    key={risk.signal_id}
                  >
                    <div className="risk-card-header">
                      <div className="risk-title-group">
                        <div
                          className={`risk-icon risk-icon-${severity}`}
                        >
                          {riskIcon}
                        </div>

                        <div>
                          <span className="label">
                            RISK TYPE
                          </span>

                          <h3>
                            {risk.risk_type.replace(
                              /_/g,
                              ' ',
                            )}
                          </h3>
                        </div>
                      </div>

                      <span
                        className={`risk-severity risk-${severity}`}
                      >
                        {risk.severity}
                      </span>
                    </div>

                    <p className="risk-evidence">
                      “{risk.evidence_quote}”
                    </p>

                    <div className="risk-divider" />

                    <p className="risk-rationale">
                      {risk.rationale}
                    </p>

                    <div className="risk-meta">
                      <div className="risk-meta-item">
                        <span className="risk-meta-icon">
                          ◎
                        </span>

                        <div>
                          <span>Confidence</span>

                          <strong>
                            {Math.round(
                              risk.confidence * 100,
                            )}
                            %
                          </strong>
                        </div>
                      </div>

                      <div className="risk-meta-item">
                        <span className="risk-meta-icon">
                          ✓
                        </span>

                        <div>
                          <span>
                            Evidence grounded
                          </span>

                          <strong>
                            Verified
                          </strong>
                        </div>
                      </div>
                    </div>
                  </article>
                )
              })}
            </div>
          )}
        </section>

        <section className="dashboard-section health-history-section">
          <div className="section-header">
            <div>
              <span className="label">
                HEALTH HISTORY
              </span>

              <h2>Project Health Trend</h2>
            </div>

            <span className="history-count">
              {historyPoints.length} snapshot
              {historyPoints.length === 1
                ? ''
                : 's'}
            </span>
          </div>

          {historyPoints.length === 0 ? (
            <div className="empty-state">
              <p>
                No health history available.
              </p>

              <span>
                Run the monitoring pipeline to create
                the first health snapshot.
              </span>
            </div>
          ) : (
            <div className="health-history-content">
              <div className="health-chart">
                <svg
                  viewBox={`0 0 ${chartWidth} ${chartHeight}`}
                  role="img"
                  aria-label="Project health score history"
                  preserveAspectRatio="none"
                >
                  {[0, 25, 50, 75, 100].map(
                    (score) => {
                      const y = getChartY(score)

                      return (
                        <g key={score}>
                          <line
                            x1={chartPadding.left}
                            y1={y}
                            x2={
                              chartPadding.left +
                              chartInnerWidth
                            }
                            y2={y}
                            className="chart-grid-line"
                          />

                          <text
                            x={
                              chartPadding.left - 10
                            }
                            y={y + 4}
                            textAnchor="end"
                            className="chart-axis-label"
                          >
                            {score}
                          </text>
                        </g>
                      )
                    },
                  )}

                  {chartPoints.length > 1 && (
                    <polyline
                      points={chartArea}
                      className="chart-area"
                    />
                  )}

                  {chartPoints.length > 1 && (
                    <polyline
                      points={chartLine}
                      className="chart-line"
                    />
                  )}

                  {chartPoints.map((point) => (
                    <g
                      key={point.calculated_at}
                    >
                      <circle
                        cx={point.x}
                        cy={point.y}
                        r="5"
                        className="chart-point"
                      />

                      <circle
                        cx={point.x}
                        cy={point.y}
                        r="2"
                        className="chart-point-inner"
                      />
                    </g>
                  ))}

                  {chartPoints.map((point) => (
                    <text
                      key={`${point.calculated_at}-date`}
                      x={point.x}
                      y={chartHeight - 12}
                      textAnchor="middle"
                      className="chart-date-label"
                    >
                      {new Date(
                        point.calculated_at,
                      ).toLocaleDateString(
                        'en-IN',
                        {
                          day: '2-digit',
                          month: 'short',
                        },
                      )}
                    </text>
                  ))}
                </svg>
              </div>

              <div className="history-list">
                {historyPoints.map((point) => (
                  <div
                    className="history-item"
                    key={point.calculated_at}
                  >
                    <div className="history-date">
                      <strong>
                        {new Date(
                          point.calculated_at,
                        ).toLocaleDateString(
                          'en-IN',
                          {
                            day: '2-digit',
                            month: 'short',
                            year: 'numeric',
                          },
                        )}
                      </strong>

                      <span>
                        {new Date(
                          point.calculated_at,
                        ).toLocaleTimeString(
                          'en-IN',
                          {
                            hour: '2-digit',
                            minute: '2-digit',
                          },
                        )}
                      </span>
                    </div>

                    <div className="history-status">
                      <span
                        className={`history-status-dot history-status-${point.status.toLowerCase()}`}
                      />

                      <span>
                        {point.status.replace(
                          /_/g,
                          ' ',
                        )}
                      </span>
                    </div>

                    <div className="history-score">
                      <strong>
                        {point.score.toFixed(1)}
                      </strong>

                      <span>/ 100</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>

        <section className="dashboard-section ai-insights-section">
          <div className="section-header">
            <div>
              <span className="label">
                AI INSIGHTS
              </span>

              <h2>Weekly Summary</h2>
            </div>

            <div className="weekly-controls">
              {availableWeeks.length > 0 && (
                <select
                  className="week-selector"
                  value={selectedWeek}
                  onChange={(event) =>
                    setSelectedWeek(
                      event.target.value,
                    )
                  }
                  disabled={weeklySummaryLoading}
                  aria-label="Select health summary week"
                >
                  {availableWeeks.map((week) => (
                    <option
                      key={week.start.toISOString()}
                      value={week.start.toISOString()}
                    >
                      {formatWeekRange(
                        week.start,
                        week.end,
                      )}
                    </option>
                  ))}
                </select>
              )}

              <div className="ai-badge">
                <span>✦</span>
                AI Generated
              </div>
            </div>
          </div>

          {weeklySummaryLoading ? (
            <div className="summary-empty">
              <div className="summary-empty-icon">
                ✦
              </div>

              <div>
                <p>
                  Loading weekly summary...
                </p>

                <span>
                  Generating the selected week's
                  project health view.
                </span>
              </div>
            </div>
          ) : weeklySummary ? (
            <>
              <div className="weekly-overview">
                <div className="weekly-score-card">
                  <span className="insight-label">
                    STARTING HEALTH
                  </span>

                  <strong>
                    {weeklySummary.starting_score.toFixed(
                      1,
                    )}
                  </strong>

                  <span>
                    {weeklySummary.starting_status.replace(
                      /_/g,
                      ' ',
                    )}
                  </span>
                </div>

                <div className="weekly-score-card">
                  <span className="insight-label">
                    ENDING HEALTH
                  </span>

                  <strong>
                    {weeklySummary.ending_score.toFixed(
                      1,
                    )}
                  </strong>

                  <span>
                    {weeklySummary.ending_status.replace(
                      /_/g,
                      ' ',
                    )}
                  </span>
                </div>

                <div className="weekly-score-card">
                  <span className="insight-label">
                    SCORE CHANGE
                  </span>

                  <strong>
                    {weeklySummary.score_change >= 0
                      ? '+'
                      : ''}
                    {weeklySummary.score_change.toFixed(
                      1,
                    )}
                  </strong>

                  <span>
                    {weeklySummary.health_improved
                      ? 'Improved'
                      : weeklySummary.health_deteriorated
                        ? 'Deteriorated'
                        : 'Stable'}
                  </span>
                </div>

                <div className="weekly-score-card weekly-date-card">
                  <span className="insight-label">
                    ANALYSIS PERIOD
                  </span>

                  <strong>
                    {selectedWeekRange
                      ? formatWeekRange(
                          selectedWeekRange.start,
                          selectedWeekRange.end,
                        )
                      : 'Selected week'}
                  </strong>
                </div>
              </div>

              <div className="insights-layout">
                <div className="summary-main">
                  <div className="insight-icon">
                    ✦
                  </div>

                  <div>
                    <span className="insight-label">
                      EXECUTIVE SUMMARY
                    </span>

                    <p className="summary-text">
                      {weeklySummary.summary}
                    </p>

                    <div className="weekly-outlook">
                      <span className="insight-label">
                        OUTLOOK
                      </span>

                      <p>
                        {weeklySummary.outlook}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="actions-panel">
                  <div className="actions-header">
                    <div className="actions-icon">
                      ✓
                    </div>

                    <div>
                      <span className="insight-label">
                        NEXT STEPS
                      </span>

                      <h3>
                        Recommended Actions
                      </h3>
                    </div>
                  </div>

                  {weeklySummary
                    .recommended_actions.length >
                  0 ? (
                    <ol className="action-list">
                      {weeklySummary.recommended_actions.map(
                        (action, index) => (
                          <li key={action}>
                            <span className="action-number">
                              {index + 1}
                            </span>

                            <span>{action}</span>
                          </li>
                        ),
                      )}
                    </ol>
                  ) : (
                    <p className="no-actions">
                      No recommended actions at
                      this time.
                    </p>
                  )}
                </div>
              </div>

              {weeklySummary.key_risks.length >
                0 && (
                <div className="weekly-key-risks">
                  <div className="weekly-subsection-header">
                    <span className="insight-label">
                      KEY RISKS
                    </span>

                    <span>
                      {
                        weeklySummary.key_risks
                          .length
                      }{' '}
                      identified
                    </span>
                  </div>

                  <div className="weekly-risk-list">
                    {weeklySummary.key_risks.map(
                      (risk) => (
                        <div
                          className="weekly-risk-item"
                          key={risk.signal_id}
                        >
                          <div>
                            <strong>
                              {risk.risk_type.replace(
                                /_/g,
                                ' ',
                              )}
                            </strong>

                            <span>
                              {risk.severity}
                            </span>
                          </div>

                          <p>
                            {risk.evidence_quote}
                          </p>
                        </div>
                      ),
                    )}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="summary-empty">
              <div className="summary-empty-icon">
                ✦
              </div>

              <div>
                <p>
                  No weekly summary available.
                </p>

                <span>
                  A weekly summary requires health
                  history for the selected project.
                </span>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App