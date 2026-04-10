<template>
  <div class="page report-page">
    <div v-if="report" class="animate-fadeIn">
      <!-- Hero -->
      <section class="report-hero">
        <div class="container">
          <div class="hero-header">
            <div class="hero-meta">
              <span class="badge badge-red">{{ report.type === 'account' ? '账号检测' : '帖子检测' }}</span>
              <span class="text-xs text-muted">{{ formatDate(report.generatedAt) }}</span>
            </div>
            <div class="share-actions">
              <button class="btn btn-ghost btn-sm" @click="copyLink">
                {{ copied ? '已复制!' : '复制链接' }}
              </button>
            </div>
          </div>

          <!-- Account Hero -->
          <template v-if="report.type === 'account'">
            <h1 class="hero-title">{{ report.nickname }}</h1>
            <p class="hero-bio">{{ report.bio }}</p>
          </template>

          <!-- Post Hero -->
          <template v-else>
            <h1 class="hero-title">{{ report.post_title }}</h1>
            <div class="post-meta">
              <span v-for="tag in (report.post_tags || [])" :key="tag" class="tag">{{ tag }}</span>
              <span class="text-xs text-muted">{{ report.published_at }}</span>
            </div>
          </template>

          <!-- Summary line -->
          <div class="summary-line">
            {{ report.analysis?.account_summary || report.analysis?.post_summary }}
          </div>
        </div>
      </section>

      <!-- Stats -->
      <section class="stats-section">
        <div class="container">
          <p class="section-title">核心数据</p>
          <div class="stats-grid">
            <div v-for="(stat, key) in displayStats" :key="key" class="hero-stat">
              <div class="value">{{ stat.value }}</div>
              <div class="label">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Core Conclusions -->
      <section class="conclusions-section">
        <div class="container">
          <p class="section-title">核心结论</p>
          <div class="card conclusions-card">
            <template v-if="report.type === 'account'">
              <div class="conclusion-item">
                <div class="conclusion-icon">📍</div>
                <div>
                  <div class="conclusion-label">账号定位</div>
                  <div class="conclusion-text">{{ report.analysis?.positioning }}</div>
                </div>
              </div>
              <div class="conclusion-item">
                <div class="conclusion-icon">👥</div>
                <div>
                  <div class="conclusion-label">目标受众</div>
                  <div class="conclusion-text">{{ report.analysis?.target_audience }}</div>
                </div>
              </div>
              <div class="conclusion-item">
                <div class="conclusion-icon">📊</div>
                <div>
                  <div class="conclusion-label">内容主题</div>
                  <div class="conclusion-tags">
                    <span v-for="t in (report.analysis?.content_topics || [])" :key="t" class="tag">{{ t }}</span>
                  </div>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="conclusion-item">
                <div class="conclusion-icon">🎯</div>
                <div>
                  <div class="conclusion-label">内容主题</div>
                  <div class="conclusion-text">{{ report.analysis?.theme }}</div>
                </div>
              </div>
              <div class="conclusion-item">
                <div class="conclusion-icon">🔑</div>
                <div>
                  <div class="conclusion-label">传播因子</div>
                  <div class="conclusion-tags">
                    <span v-for="s in (report.analysis?.spread_factors || [])" :key="s" class="tag">{{ s }}</span>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </section>

      <!-- Top Posts -->
      <section v-if="report.top_posts?.length" class="topposts-section">
        <div class="container">
          <p class="section-title">
            {{ report.type === 'account' ? '爆文样本' : '代表内容' }}
          </p>
          <div class="post-list">
            <div v-for="post in report.top_posts" :key="post.title" class="post-card">
              <img
                v-if="post.cover"
                :src="post.cover"
                :alt="post.title"
                class="post-cover"
                loading="lazy"
              />
              <div v-else class="post-cover" />
              <div class="post-info">
                <div class="post-title">{{ post.title }}</div>
                <div class="post-stats">
                  <span>❤️ {{ formatNum(post.likes) }}</span>
                  <span>⭐ {{ formatNum(post.collects) }}</span>
                  <span>💬 {{ formatNum(post.comments) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Comment Insights -->
      <section class="insights-section">
        <div class="container">
          <p class="section-title">评论区洞察</p>
          <div class="card">
            <div v-if="report.type === 'account'">
              <div class="insight-item">
                <div class="insight-dot" />
                <div class="insight-text">
                  <strong class="text-secondary">高频问题：</strong>
                  {{ (report.analysis?.comment_insights?.high_freq_questions || []).join('、') }}
                </div>
              </div>
              <div class="insight-item">
                <div class="insight-dot" />
                <div class="insight-text">
                  <strong class="text-secondary">用户情绪：</strong>{{ report.analysis?.comment_insights?.user_sentiment }}
                </div>
              </div>
              <div class="insight-item">
                <div class="insight-dot" />
                <div class="insight-text">
                  <strong class="text-secondary">核心需求：</strong>{{ report.analysis?.comment_insights?.key_demands }}
                </div>
              </div>
            </div>
            <template v-else>
              <div class="insight-item">
                <div class="insight-dot" />
                <div class="insight-text">
                  <strong class="text-secondary">高频问题：</strong>
                  {{ (report.analysis?.comment_insights?.high_freq_questions || []).join('、') }}
                </div>
              </div>
              <div class="insight-item">
                <div class="insight-dot" />
                <div class="insight-text">
                  <strong class="text-secondary">用户情绪：</strong>{{ report.analysis?.comment_insights?.user_sentiment }}
                </div>
              </div>
            </template>
          </div>
        </div>
      </section>

      <!-- Strategy Suggestions -->
      <section class="suggestions-section">
        <div class="container">
          <p class="section-title">
            {{ report.type === 'account' ? '可借鉴策略建议' : '改进建议' }}
          </p>
          <div class="suggestions-list">
            <div
              v-for="(s, i) in (report.type === 'account' ? report.analysis?.action_suggestions : report.analysis?.improvement_suggestions) || []"
              :key="i"
              class="suggestion-item card"
            >
              <div class="suggestion-num">{{ String(i + 1).padStart(2, '0') }}</div>
              <div class="suggestion-text">{{ s }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Strengths / Weaknesses (account only) -->
      <section v-if="report.type === 'account' && report.analysis?.strengths?.length" class="sw-section">
        <div class="container">
          <div class="sw-grid">
            <div class="card sw-card">
              <p class="section-title">优势</p>
              <div v-for="s in (report.analysis?.strengths || [])" :key="s" class="insight-item">
                <div class="insight-dot" style="background: var(--success)" />
                <div class="insight-text">{{ s }}</div>
              </div>
            </div>
            <div class="card sw-card">
              <p class="section-title">待改进</p>
              <div v-for="w in (report.analysis?.weaknesses || [])" :key="w" class="insight-item">
                <div class="insight-dot" style="background: var(--warning)" />
                <div class="insight-text">{{ w }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="report-cta">
        <div class="container">
          <NuxtLink to="/" class="btn btn-primary w-full">
            再分析一个链接
          </NuxtLink>
          <p class="text-xs text-muted text-center mt-12">
            由 Red Checking 生成 · 仅供参考
          </p>
        </div>
      </section>
    </div>

    <!-- Loading / Error states -->
    <div v-else-if="loading" class="loading-state">
      <div class="spinner large" />
      <p class="text-secondary mt-16 text-sm">加载报告中...</p>
    </div>
    <div v-else class="error-state container">
      <p class="text-accent">报告不存在或已失效</p>
      <NuxtLink to="/" class="btn btn-ghost mt-16">返回首页</NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { getReport } = useApi()
const reportId = route.params.reportId as string

const report = ref<any>(null)
const loading = ref(true)
const copied = ref(false)

const formatDate = (iso: string) => {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

const formatNum = (n: number) => {
  if (!n && n !== 0) return '-'
  if (n >= 10000) return (n / 10000).toFixed(1) + '万'
  return n.toString()
}

const displayStats = computed(() => {
  if (!report.value?.stats) return {}
  const s = report.value.stats
  if (report.value.type === 'account') {
    return {
      followers: { value: s.followers, label: '粉丝' },
      likes: { value: s.likes_received, label: '获赞' },
      posts: { value: s.posts_count, label: '笔记' },
    }
  }
  return {
    likes: { value: formatNum(s.likes), label: '点赞' },
    collects: { value: formatNum(s.collects), label: '收藏' },
    comments: { value: formatNum(s.comments), label: '评论' },
  }
})

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href)
    copied.value = true
    setTimeout(() => (copied.value = false), 2000)
  } catch {}
}

onMounted(async () => {
  try {
    report.value = await getReport(reportId)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.report-page {
  padding-bottom: 60px;
}
.report-hero {
  padding: 32px 0 24px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}
.hero-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.hero-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}
.btn-sm {
  padding: 8px 16px;
  font-size: 0.8125rem;
}
.hero-title {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 8px;
  line-height: 1.3;
}
.hero-bio {
  font-size: 0.875rem;
  white-space: pre-line;
  margin-bottom: 16px;
}
.post-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}
.tag {
  padding: 4px 10px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 99px;
  font-size: 0.6875rem;
  color: var(--text-muted);
}
.summary-line {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.stats-section {
  padding: 0 0 24px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
.conclusions-section {
  padding: 0 0 24px;
}
.conclusions-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.conclusion-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}
.conclusion-icon {
  font-size: 1.125rem;
  flex-shrink: 0;
  margin-top: 2px;
}
.conclusion-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.conclusion-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.5;
}
.conclusion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 4px;
}
.topposts-section {
  padding: 0 0 24px;
}
.post-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.insights-section {
  padding: 0 0 24px;
}
.suggestions-section {
  padding: 0 0 24px;
}
.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.suggestion-item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}
.suggestion-num {
  font-size: 1rem;
  font-weight: 800;
  color: var(--accent);
  flex-shrink: 0;
  line-height: 1.5;
}
.suggestion-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.5;
}
.sw-section {
  padding: 0 0 24px;
}
.sw-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.sw-card .section-title {
  margin-bottom: 12px;
}
.report-cta {
  padding: 24px 0;
}
.loading-state, .error-state {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.spinner.large {
  width: 40px;
  height: 40px;
  border-width: 3px;
}
</style>
