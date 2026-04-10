/**
 * Red Checking - Report Schema Types
 * Strictly mirrors backend/schemas/models.py Pydantic models.
 * Any change to backend schema must be reflected here.
 */

// ---- Shared ----

export type InputType = 'account' | 'post'
export type TaskStatus = 'pending' | 'scraping' | 'analyzing' | 'generating' | 'done' | 'failed'

// ---- Task ----

export interface CreateTaskResponse {
  taskId: string
  type: InputType
  status: TaskStatus
}

export interface TaskStatusResponse {
  taskId: string
  type: InputType
  status: TaskStatus
  reportId?: string
  errorMessage?: string
  progress: number // 0-100
}

// ---- Report ----

// AI analysis payload for account type
export interface AccountAnalysis {
  account_summary: string
  positioning: string
  target_audience: string
  content_topics: string[]
  viral_posts: Array<{ title: string; reason: string }>
  title_patterns: string[]
  content_patterns: string[]
  comment_insights: {
    high_freq_questions: string[]
    user_sentiment: string
    key_demands: string
  }
  strengths: string[]
  weaknesses: string[]
  benchmarking: {
    similar_accounts: string[]
    data_reference: string
  }
  action_suggestions: string[]
}

// AI analysis payload for post type
export interface PostAnalysis {
  post_summary: string
  theme: string
  title_analysis: {
    structure: string
    techniques: string[]
    keywords: string[]
  }
  structure_analysis: {
    outline: string[]
    length: string
    format: string
  }
  emotional_hooks: string[]
  value_points: string[]
  conflict_points: string[]
  spread_factors: string[]
  comment_insights: {
    high_freq_questions: string[]
    user_sentiment: string
    key_demands: string
  }
  benchmark_reference: {
    avg_likes_in_category: number
    this_post_likes: number
    percentile: string
  }
  improvement_suggestions: string[]
}

// Top post item shared between account and post report
export interface TopPost {
  title: string
  cover: string
  likes: number
  collects: number
  comments: number
}

// Stats for account
export interface AccountStats {
  followers: string
  following: number
  likes_received: string
  posts_count: number
  avg_likes: number
  avg_collects: number
  avg_comments: number
}

// Stats for post
export interface PostStats {
  likes: number
  collects: number
  comments: number
  shares: number
  cover: string
}

// Full report response
export interface ReportResponse {
  reportId: string
  taskId: string
  type: InputType
  generatedAt: string

  // Account fields
  nickname?: string
  bio?: string

  // Post fields
  post_title?: string
  post_tags?: string[]
  published_at?: string

  // Common
  stats?: AccountStats | PostStats
  top_posts?: TopPost[]
  analysis?: AccountAnalysis | PostAnalysis
}

// Narrowed types for convenience
export interface AccountReport extends ReportResponse {
  type: 'account'
  nickname: string
  bio: string
  stats: AccountStats
  analysis: AccountAnalysis
}

export interface PostReport extends ReportResponse {
  type: 'post'
  post_title: string
  post_tags: string[]
  published_at: string
  stats: PostStats
  analysis: PostAnalysis
}

// Validation helpers
export function isAccountReport(r: ReportResponse): r is AccountReport {
  return r.type === 'account'
}

export function isPostReport(r: ReportResponse): r is PostReport {
  return r.type === 'post'
}
