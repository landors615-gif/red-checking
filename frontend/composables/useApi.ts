// composables/useApi.ts
import type {
  CreateTaskResponse,
  TaskStatusResponse,
  ReportResponse,
} from '~/types/report'

export { type CreateTaskResponse, type TaskStatusResponse, type ReportResponse }

export const useApi = () => {
  // Use Nuxt 3 runtime config (NUXT_PUBLIC_API_BASE from nuxt.config.ts)
  // Falls back to localhost:8000 for local dev
  const config = useRuntimeConfig()
  const baseUrl = (config.public.apiBase as string | undefined) || 'http://localhost:8000'

  const createTask = async (url: string): Promise<CreateTaskResponse> => {
    const res = await $fetch<CreateTaskResponse>(`${baseUrl}/api/analysis`, {
      method: 'POST',
      body: { url },
    })
    return res
  }

  const getTaskStatus = async (taskId: string): Promise<TaskStatusResponse> => {
    const res = await $fetch<TaskStatusResponse>(`${baseUrl}/api/analysis/${taskId}`)
    return res
  }

  const getReport = async (reportId: string): Promise<ReportResponse> => {
    const res = await $fetch<ReportResponse>(`${baseUrl}/api/report/${reportId}`)
    return res
  }

  return { createTask, getTaskStatus, getReport }
}
