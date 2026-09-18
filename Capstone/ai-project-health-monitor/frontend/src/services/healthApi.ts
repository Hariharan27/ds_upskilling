const API_BASE_URL = 'http://localhost:8000/api/v1'

export interface Project {
  project_id: string
}

export interface RiskSignal {
  signal_id: string
  risk_type: string
  severity: string
  confidence: number
  evidence_quote: string
  rationale: string
}

export interface ProjectHealthResponse {
  project_id: string
  health_score: number
  health_status: string
  rationale: string
  risks: RiskSignal[]
  summary: ProjectHealthSummary | null
  alert_triggered: boolean
}

export interface ProjectHealthSummary {
  project_id: string
  overall_summary: string
  key_risks: RiskSignal[]
  recommended_actions: string[]
}

export interface HealthTrendResponse {
  project_id: string
  current_score: number
  previous_score: number | null
  current_status: string
  score_change: number | null
}

export interface HealthHistoryPoint {
  score: number
  status: string
  calculated_at: string
}

export interface HealthHistoryResponse {
  project_id: string
  points: HealthHistoryPoint[]
}

export interface WeeklyHealthSummaryResponse {
  project_id: string
  start_date: string
  end_date: string
  starting_score: number
  ending_score: number
  score_change: number
  starting_status: string
  ending_status: string
  health_improved: boolean
  health_deteriorated: boolean
  key_risks: RiskSignal[]
  summary: string
  outlook: string
  recommended_actions: string[]
}

export async function getProjects(): Promise<Project[]> {
  const response = await fetch(`${API_BASE_URL}/projects`)

  if (!response.ok) {
    throw new Error('Failed to fetch projects')
  }

  return response.json()
}

export async function refreshProjectHealth(
  projectId: string,
): Promise<ProjectHealthResponse> {
  const response = await fetch(
    `${API_BASE_URL}/projects/${projectId}/health/refresh`,
    {
      method: 'POST',
    },
  )

  if (!response.ok) {
    throw new Error('Failed to refresh project health')
  }

  return response.json()
}

export async function getProjectHealth(
  projectId: string,
): Promise<ProjectHealthResponse> {
  const response = await fetch(
    `${API_BASE_URL}/projects/${projectId}/health`,
  )

  if (!response.ok) {
    throw new Error('Failed to fetch project health')
  }

  return response.json()
}

export async function getHealthTrend(
  projectId: string,
): Promise<HealthTrendResponse> {
  const response = await fetch(
    `${API_BASE_URL}/projects/${projectId}/health/trend`,
  )

  if (!response.ok) {
    throw new Error('Failed to fetch health trend')
  }

  return response.json()
}

export async function getHealthHistory(
  projectId: string,
): Promise<HealthHistoryResponse> {
  const response = await fetch(
    `${API_BASE_URL}/projects/${projectId}/health/history`,
  )

  if (!response.ok) {
    throw new Error('Failed to fetch health history')
  }

  return response.json()
}

export async function getWeeklyHealthSummary(
  projectId: string,
  startDate: Date,
  endDate: Date,
): Promise<WeeklyHealthSummaryResponse> {
  const params = new URLSearchParams({
    start_date: startDate.toISOString(),
    end_date: endDate.toISOString(),
  })

  const response = await fetch(
    `${API_BASE_URL}/projects/${projectId}/health/weekly-summary?${params.toString()}`,
  )

  if (!response.ok) {
    throw new Error('Failed to fetch weekly health summary')
  }

  return response.json()
}