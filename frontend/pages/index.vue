<template>
  <div class="page">
    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <div class="brand animate-slideUp">
          <span class="brand-mark">R</span>
          <span class="brand-name">Red Checking</span>
        </div>
        <h1 class="hero-title animate-slideUp">
          输入一个小红书链接<br />快速看懂它为什么值得研究
        </h1>
        <p class="hero-sub animate-slideUp">
          自动抓取公开内容 · AI 生成结构化报告 · 支持一键分享
        </p>

        <!-- Input -->
        <div class="input-group animate-slideUp">
          <input
            v-model="url"
            class="input"
            type="url"
            placeholder="粘贴小红书账号或帖子链接..."
            @keydown.enter="startAnalysis"
          />
          <button
            class="btn btn-primary w-full mt-12"
            :disabled="!url.trim() || loading"
            @click="startAnalysis"
          >
            <span v-if="loading" class="spinner" />
            <span v-else>开始检测</span>
          </button>
          <p v-if="error" class="error-msg mt-8">{{ error }}</p>
        </div>

        <p class="support-note animate-slideUp">
          支持 <span class="text-accent">账号链接</span> 与 <span class="text-accent">帖子链接</span>
        </p>
      </div>
    </section>

    <!-- Value Props -->
    <section class="value-section">
      <div class="container">
        <div class="value-grid stagger">
          <div class="value-card card animate-slideUp">
            <div class="value-icon">🔍</div>
            <h3>自动抓取</h3>
            <p>智能识别链接类型，提取账号/帖子的公开内容与互动数据</p>
          </div>
          <div class="value-card card animate-slideUp">
            <div class="value-icon">🧠</div>
            <h3>AI 结构化洞察</h3>
            <p>基于内容与评论区输出定位分析、爆文规律、策略建议</p>
          </div>
          <div class="value-card card animate-slideUp">
            <div class="value-icon">📤</div>
            <h3>可分享报告</h3>
            <p>生成精致报告页，直接转发给同事、客户或老板</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Use Cases -->
    <section class="cases-section">
      <div class="container">
        <p class="section-title">适用场景</p>
        <div class="cases stagger">
          <div class="case-tag animate-slideUp">竞品账号诊断</div>
          <div class="case-tag animate-slideUp">爆文拆解分析</div>
          <div class="case-tag animate-slideUp">汇报级报告输出</div>
          <div class="case-tag animate-slideUp">选题与内容启发</div>
        </div>
      </div>
    </section>

    <!-- Demo Reports -->
    <section class="demo-section">
      <div class="container">
        <p class="section-title">示例报告</p>
        <div class="demo-list stagger">
          <NuxtLink to="/report/rpt_demo_account_001" class="demo-item card animate-slideUp">
            <div class="demo-type badge badge-red">账号检测</div>
            <div class="demo-title">美妆护肤实验室</div>
            <div class="demo-desc">12.8万粉成分党测评博主，爆文规律与评论区洞察</div>
          </NuxtLink>
          <NuxtLink to="/report/rpt_demo_post_001" class="demo-item card animate-slideUp">
            <div class="demo-type badge badge-red">帖子检测</div>
            <div class="demo-title">这瓶精华液我用了28天</div>
            <div class="demo-desc">12800点赞爆文，标题结构与传播因子拆解</div>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- Footer note -->
    <section class="footer-note">
      <div class="container text-center">
        <p class="text-xs text-muted">
          仅分析公开可见内容 · 报告生成约需 20-60 秒
        </p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { createTask } = useApi()
const router = useRouter()

const url = ref('')
const loading = ref(false)
const error = ref('')

const startAnalysis = async () => {
  if (!url.value.trim()) return
  loading.value = true
  error.value = ''
  try {
    const res = await createTask(url.value.trim())
    router.push(`/analyzing/${res.taskId}`)
  } catch (e: any) {
    error.value = e?.data?.detail || '创建任务失败，请检查链接格式'
    loading.value = false
  }
}
</script>

<style scoped>
.hero {
  padding: 60px 0 40px;
}
.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 28px;
}
.brand-mark {
  width: 36px;
  height: 36px;
  background: var(--accent);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.125rem;
  color: white;
}
.brand-name {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}
.hero-title {
  font-size: 1.625rem;
  line-height: 1.3;
  margin-bottom: 12px;
  color: var(--text-primary);
}
.hero-sub {
  font-size: 0.875rem;
  margin-bottom: 32px;
}
.input-group {
  margin-bottom: 12px;
}
.support-note {
  font-size: 0.75rem;
  text-align: center;
}
.error-msg {
  color: var(--accent);
  font-size: 0.8125rem;
  text-align: center;
}
.value-section {
  padding: 32px 0;
}
.value-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.value-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.value-icon {
  font-size: 1.5rem;
}
.value-card h3 {
  font-size: 0.9375rem;
}
.value-card p {
  font-size: 0.8125rem;
}
.cases-section {
  padding: 0 0 32px;
}
.cases {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.case-tag {
  padding: 8px 14px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 99px;
  font-size: 0.8125rem;
  color: var(--text-secondary);
}
.demo-section {
  padding: 0 0 100px;
}
.demo-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.demo-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-decoration: none;
  transition: border-color 0.2s;
}
.demo-item:hover {
  border-color: var(--accent);
}
.demo-type {
  align-self: flex-start;
  margin-bottom: 4px;
}
.demo-title {
  font-weight: 700;
  font-size: 0.9375rem;
  color: var(--text-primary);
}
.demo-desc {
  font-size: 0.8125rem;
  color: var(--text-muted);
}
.footer-note {
  padding: 16px 0 32px;
}
</style>
