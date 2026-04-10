// composables/useApi.ts

export interface CreateTaskResponse {
  taskId: string
  type: 'account' | 'post'
  status: string
}

export interface TaskStatus {
  taskId: string
  type: 'account' | 'post'
  status: 'pending' | 'scraping' | 'analyzing' | 'generating' | 'done' | 'failed'
  reportId?: string
  errorMessage?: string
  progress: number
}

export const useApi = () => {
  // Use a fixed base URL for MVP; can be overridden via env
  const baseUrl = 'http://localhost:8000'

  const createTask = async (url: string): Promise<CreateTaskResponse> => {
    const res = await $fetch<CreateTaskResponse>(`${baseUrl}/api/analysis`, {
      method: 'POST',
      body: { url },
    })
    return res
  }

  const getTaskStatus = async (taskId: string): Promise<TaskStatus> => {
    const res = await $fetch<TaskStatus>(`${baseUrl}/api/analysis/${taskId}`)
    return res
  }

  const getReport = async (reportId: string) => {
    const res = await $fetch(`${baseUrl}/api/report/${reportId}`)
    return res
  }

  return { createTask, getTaskStatus, getReport }
}
