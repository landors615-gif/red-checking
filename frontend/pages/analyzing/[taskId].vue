<template>
  <div class="page analyzing-page">
    <div class="container">
      <!-- Header -->
      <div class="header animate-slideUp">
        <div class="brand">
          <NuxtLink to="/" class="back-btn">←</NuxtLink>
          <span class="brand-mark">R</span>
          <span class="brand-name">Red Checking</span>
        </div>
      </div>

      <!-- Main content -->
      <div class="content">
        <div v-if="task">
          <!-- Status title -->
          <div class="status-hero animate-slideUp">
            <div v-if="task.status === 'done'" class="status-icon done">✓</div>
            <div v-else-if="task.status === 'failed'" class="status-icon failed">✕</div>
            <div v-else class="status-icon processing">
              <div class="spinner" />
            </div>

            <h1 class="status-title">
              <template v-if="task.status === 'pending'">正在准备分析任务...</template>
              <template v-else-if="task.status === 'scraping'">正在抓取内容</template>
              <template v-else-if="task.status === 'analyzing'">正在生成分析</template>
              <template v-else-if="task.status === 'generating'">正在组织报告</template>
              <template v-else-if="task.status === 'done'">报告生成完成</template>
              <template v-else-if="task.status === 'failed'">生成失败</template>
            </h1>
          </div>

          <!-- Steps -->
          <div class="steps card animate-slideUp">
            <div
              v-for="(step, i) in steps"
              :key="i"
              class="step"
              :class="{
                active: currentStep === i,
                done: currentStep > i,
              }"
            >
              <div class="step-dot">
                <span v-if="currentStep > i">✓</span>
                <div v-else-if="currentStep === i" class="spinner" />
              </div>
              <span class="step-label">{{ step }}</span>
            </div>
          </div>

          <!-- Progress -->
          <div v-if="task.status !== 'done' && task.status !== 'failed'" class="progress-wrap animate-slideUp">
            <div class="progress-track">
              <div class="progress-fill" :style="{ width: task.progress + '%' }" />
            </div>
            <p class="progress-label text-xs text-muted mt-8">{{ task.progress }}%</p>
          </div>

          <!-- Error -->
          <div v-if="task.status === 'failed'" class="error-box card animate-slideUp">
            <div class="error-icon">!</div>
            <p class="error-title">生成失败</p>
            <p class="text-accent text-sm">{{ task.errorMessage || '分析过程中出现错误，请重试' }}</p>
            <button class="btn btn-primary mt-20 w-full" @click="retry">重新分析</button>
            <NuxtLink to="/" class="btn btn-ghost mt-8 w-full">返回首页</NuxtLink>
          </div>

          <!-- Done -->
          <div v-if="task.status === 'done'" class="done-actions animate-slideUp">
            <p class="text-secondary text-sm text-center mb-24">
              报告已生成，正在跳转...
            </p>
            <NuxtLink
              v-if="task.reportId"
              :to="`/report/${task.reportId}`"
              class="btn btn-primary w-full"
            >
              查看报告
            </NuxtLink>
          </div>

          <!-- Hint -->
          <p v-if="!['done', 'failed'].includes(task.status)" class="hint text-xs text-muted text-center animate-slideUp">
            请保持页面开启，通常需要 20-60 秒
          </p>
        </div>

        <!-- Loading initial -->
        <div v-else class="loading-state">
          <div class="spinner large" />
          <p class="text-secondary mt-16 text-sm">加载中...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const { getTaskStatus } = useApi()

const taskId = route.params.taskId as string

const task = ref<any>(null)
let pollTimer: ReturnType<typeof setTimeout> | null = null

const steps = ['抓取内容', '生成分析', '组织报告']
const stepMap: Record<string, number> = {
  pending: 0,
  scraping: 0,
  analyzing: 1,
  generating: 2,
  done: 3,
  failed: -1,
}
const currentStep = computed(() => stepMap[task.value?.status] ?? 0)

const poll = async () => {
  try {
    task.value = await getTaskStatus(taskId)
    if (task.value.status === 'done' || task.value.status === 'failed') {
      // Stop polling
      if (pollTimer) clearTimeout(pollTimer)
      // Auto redirect if done after short delay
      if (task.value.status === 'done' && task.value.reportId) {
        setTimeout(() => {
          router.push(`/report/${task.value.reportId}`)
        }, 1500)
      }
    } else {
      pollTimer = setTimeout(poll, 1200)
    }
  } catch (e) {
    console.error('Poll error', e)
    pollTimer = setTimeout(poll, 2000)
  }
}

const retry = () => {
  router.push('/')
}

onMounted(() => {
  poll()
})

onUnmounted(() => {
  if (pollTimer) clearTimeout(pollTimer)
})
</script>

<style scoped>
.analyzing-page {
  padding-top: 24px;
}
.header {
  margin-bottom: 48px;
}
.back-btn {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 1.25rem;
  margin-right: 12px;
}
.brand {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.brand-mark {
  width: 28px;
  height: 28px;
  background: var(--accent);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.875rem;
  color: white;
}
.brand-name {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-primary);
}
.content {
  padding-top: 40px;
}
.status-hero {
  text-align: center;
  margin-bottom: 40px;
}
.status-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  font-size: 1.5rem;
}
.status-icon.done {
  background: rgba(76, 175, 80, 0.15);
  color: var(--success);
}
.status-icon.failed {
  background: rgba(232, 64, 64, 0.15);
  color: var(--accent);
}
.status-icon.processing {
  background: var(--bg-card);
  border: 1px solid var(--border);
}
.status-title {
  font-size: 1.25rem;
  color: var(--text-primary);
}
.steps {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-bottom: 32px;
}
.step {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid var(--border);
  opacity: 0.4;
  transition: opacity 0.3s;
}
.step:last-child { border-bottom: none; }
.step.active, .step.done { opacity: 1; }
.step-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6875rem;
  flex-shrink: 0;
  background: var(--bg-card);
}
.step.done .step-dot {
  background: rgba(76, 175, 80, 0.15);
  border-color: var(--success);
  color: var(--success);
}
.step.active .step-dot {
  border-color: var(--accent);
}
.step-label {
  font-size: 0.9375rem;
  color: var(--text-secondary);
}
.step.active .step-label { color: var(--text-primary); font-weight: 600; }
.step.done .step-label { color: var(--text-secondary); }
.progress-wrap {
  margin-bottom: 24px;
}
.progress-label { text-align: right; }
.hint {
  margin-top: 32px;
}
.done-actions {
  padding-top: 16px;
}
.error-box {
  border-color: rgba(232, 64, 64, 0.3);
  text-align: center;
  padding: 32px 20px;
}
.error-icon {
  width: 48px; height: 48px;
  border-radius: 50%;
  background: var(--accent-dim);
  color: var(--accent);
  font-size: 1.5rem; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
}
.error-title {
  font-size: 1.125rem; font-weight: 700;
  color: var(--text-primary); margin-bottom: 8px;
}
.loading-state {
  text-align: center;
  padding-top: 80px;
}
.spinner.large {
  width: 40px;
  height: 40px;
  border-width: 3px;
  margin: 0 auto;
}
</style>
