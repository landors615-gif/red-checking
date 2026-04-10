<template>
  <div class="page report-page">
    <div v-if="report" class="animate-fadeIn">

      <!-- ── Hero ── -->
      <section class="report-hero">
        <div class="container">
          <div class="hero-header">
            <div class="hero-meta">
              <span class="badge badge-red">{{ isAccount ? '账号检测' : '帖子检测' }}</span>
              <span class="text-xs text-muted">{{ formatDate(report.generatedAt) }}</span>
            </div>
            <button class="btn btn-ghost btn-sm" @click="copyLink">
              {{ copied ? '✓ 已复制' : '复制链接' }}
            </button>
          </div>

          <!-- Account hero -->
          <template v-if="isAccount">
            <h1 class="hero-title">{{ (report as AccountReport).nickname }}</h1>
            <p class="hero-bio">{{ (report as AccountReport).bio }}</p>
          </template>

          <!-- Post hero -->
          <template v-else>
            <h1 class="hero-title">{{ (report as PostReport).post_title }}</h1>
            <div class="post-meta">
              <span v-for="tag in ((report as PostReport).post_tags || [])" :key="tag" class="tag">{{ tag }}</span>
              <span class="text-xs text-muted">{{ (report as PostReport).published_at }}</span>
            </div>
          </template>

          <!-- Summary -->
          <div class="summary-line">
            {{ summaryText }}
          </div>
        </div>
      </section>

      <!-- ── Stats ── -->
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

      <!-- ── Core Conclusions ── -->
      <section class="conclusions-section">
        <div class="container">
          <p class="section-title">核心结论</p>
          <div class="card conclusions-card">
            <!-- Account -->
            <template v-if="isAccount && analysis">
              <div class="conclusion-item">
                <div class="conclusion-icon">📍</div>
                <div>
                  <div class="conclusion-label">账号定位</div>
                  <div class="conclusion-text">{{ analysis.positioning }}</div>
                </div>
              </div>
              <div class="conclusion-item">
                <div class="conclusion-icon">👥</div>
                <div>
                  <div class="conclusion-label">目标受众</div>
                  <div class="conclusion-text">{{ analysis.target_audience }}</div>
                </div>
              </div>
              <div class="conclusion-item">
                <div class="conclusion-icon">📊</div>
                <div>
                  <div class="conclusion-label">内容主题</div>
                  <div class="conclusion-tags">
                    <span v-for="t in analysis.content_topics" :key="t" class="tag">{{ t }}</span>
                  </div>
                </div>
              </div>
            </template>
            <!-- Post -->
            <template v-else-if="!isAccount && analysis">
              <div class="conclusion-item">
                <div class="conclusion-icon">🎯</div>
                <div>
                  <div class="conclusion-label">内容主题</div>
                  <div class="conclusion-text">{{ (analysis as PostAnalysis).theme }}</div>
                </div>
              </div>
              <div class="conclusion-item">
                <div class="conclusion-icon">🔑</div>
                <div>
                  <div class="conclusion-label">传播因子</div>
                  <div class="conclusion-tags">
                    <span v-for="s in (analysis as PostAnalysis).spread_factors" :key="s" class="tag">{{ s }}</span>
                  </div>
                </div>
              </div>
              <!-- Title structure -->
              <div class="conclusion-item">
                <div class="conclusion-icon">✍️</div>
                <div>
                  <div class="conclusion-label">标题结构</div>
                  <div class="conclusion-text">{{ (analysis as PostAnalysis).title_analysis?.structure }}</div>
                  <div class="conclusion-tags mt-6">
                    <span v-for="kw in (analysis as PostAnalysis).title_analysis?.keywords" :key="kw" class="tag">{{ kw }}</span>
                  </div>
                </div>
              </div>
            </template>
            <!-- No analysis data -->
            <template v-else>
              <p class="text-muted text-sm">暂无分析数据</p>
            </template>
          </div>
        </div>
      </section>

      <!-- ── Title / Content Patterns (account only) ── -->
      <section v-if="isAccount && analysis && analysis.title_patterns?.length" class="patterns-section">
        <div class="container">
          <p class="section-title">爆款标题规律</p>
          <div class="patterns-list">
            <div v-for="(p, i) in analysis.title_patterns" :key="i" class="pattern-item card">
              <span class="pattern-num">{{ String(i + 1).padStart(2, '0') }}</span>
              <span class="pattern-text">{{ p }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ── Post structure (post only) ── -->
      <section v-if="!isAccount && analysis && (analysis as PostAnalysis).structure_analysis?.outline?.length" class="structure-section">
        <div class="container">
          <p class="section-title">内容结构</p>
          <div class="card">
            <div v-for="(step, i) in (analysis as PostAnalysis).structure_analysis.outline" :key="i" class="structure-step">
              <span class="step-num">{{ i + 1 }}</span>
              <span class="step-text">{{ step }}</span>
            </div>
            <div class="structure-meta mt-12 text-xs text-muted">
              篇幅：{{ (analysis as PostAnalysis).structure_analysis.length }} &nbsp;·&nbsp;
              格式：{{ (analysis as PostAnalysis).structure_analysis.format }}
            </div>
          </div>
        </div>
      </section>

      <!-- ── Top Posts ── -->
      <section v-if="report.top_posts?.length" class="topposts-section">
        <div class="container">
          <p class="section-title">{{ isAccount ? '爆文样本' : '代表内容' }}</p>
          <div class="post-list">
            <div v-for="post in report.top_posts" :key="post.title" class="post-card">
              <img
                v-if="post.cover"
                :src="post.cover"
                :alt="post.title"
                class="post-cover"
                loading="lazy"
              />
              <div v-else class="post-cover post-cover--empty" />
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

      <!-- ── Comment Insights ── -->
      <section v-if="analysis?.comment_insights" class="insights-section">
        <div class="container">
          <p class="section-title">评论区洞察</p>
          <div class="card">
            <div class="insight-item">
              <div class="insight-dot" />
              <div class="insight-text">
                <strong class="text-secondary">高频问题：</strong>
                {{ analysis.comment_insights.high_freq_questions.join('、') }}
              </div>
            </div>
            <div class="insight-item">
              <div class="insight-dot" />
              <div class="insight-text">
                <strong class="text-secondary">用户情绪：</strong>{{ analysis.comment_insights.user_sentiment }}
              </div>
            </div>
            <div class="insight-item">
              <div class="insight-dot" />
              <div class="insight-text">
                <strong class="text-secondary">核心需求：</strong>{{ analysis.comment_insights.key_demands }}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── Strategy / Improvement ── -->
      <section class="suggestions-section">
        <div class="container">
          <p class="section-title">{{ isAccount ? '可借鉴策略建议' : '改进建议' }}</p>
          <div class="suggestions-list">
            <div
              v-for="(s, i) in suggestionItems"
              :key="i"
              class="suggestion-item card"
            >
              <div class="suggestion-num">{{ String(i + 1).padStart(2, '0') }}</div>
              <div class="suggestion-text">{{ s }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── Strengths / Weaknesses (account only) ── -->
      <section v-if="isAccount && analysis?.strengths?.length" class="sw-section">
        <div class="container">
          <div class="sw-grid">
            <div class="card sw-card">
              <p class="section-title">优势</p>
              <div v-for="s in analysis.strengths" :key="s" class="insight-item">
                <div class="insight-dot" style="background: var(--success)" />
                <div class="insight-text">{{ s }}</div>
              </div>
            </div>
            <div v-if="analysis.weaknesses?.length" class="card sw-card">
              <p class="section-title">待改进</p>
              <div v-for="w in analysis.weaknesses" :key="w" class="insight-item">
                <div class="insight-dot" style="background: var(--warning)" />
                <div class="insight-text">{{ w }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── Benchmarking (account only) ── -->
      <section v-if="isAccount && analysis?.benchmarking" class="benchmark-section">
        <div class="container">
          <p class="section-title">对标参考</p>
          <div class="card">
            <p class="text-sm text-secondary mb-8">相似账号：{{ analysis.benchmarking.similar_accounts.join('、') }}</p>
            <p class="text-sm text-muted">{{ analysis.benchmarking.data_reference }}</p>
          </div>
        </div>
      </section>

      <!-- ── CTA ── -->
      <section class="report-cta">
        <div class="container">
          <NuxtLink to="/" class="btn btn-primary w-full">再分析一个链接</NuxtLink>
          <p class="text-xs text-muted text-center mt-12">由 Red Checking 生成 · 仅供参考</p>
        </div>
      </section>
    </div>

    <!-- Loading state -->
    <div v-else-if="loading" class="loading-state">
      <div class="spinner large" />
      <p class="text-secondary mt-16 text-sm">加载报告中...</p>
    </div>

    <!-- Not found state -->
    <div v-else class="notfound-state">
      <div class="container text-center">
        <div class="notfound-icon">!</div>
        <h2 class="text-lg mb-8">报告不存在</h2>
        <p class="text-muted text-sm mb-24">报告不存在或已过期，请重新分析</p>
        <NuxtLink to="/" class="btn btn-primary">返回首页</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type {
  ReportResponse,
  AccountReport,
  PostReport,
  AccountAnalysis,
  PostAnalysis,
} from '~/types/report'
import { isAccountReport, isPostReport } from '~/types/report'

const route = useRoute()
const { getReport } = useApi()
const reportId = route.params.reportId as string

const report = ref<ReportResponse | null>(null)
const loading = ref(true)
const copied = ref(false)

// ── Narrowed helpers ──────────────────────────────────────────────

const isAccount = computed(() => isAccountReport(report.value ?? null))

const analysis = computed<AccountAnalysis | PostAnalysis | undefined>(() => {
  return report.value?.analysis as AccountAnalysis | PostAnalysis | undefined
})

const summaryText = computed(() => {
  if (!report.value?.analysis) return ''
  return (report.value.analysis as AccountAnalysis).account_summary
    || (report.value.analysis as PostAnalysis).post_summary
    || ''
})

const suggestionItems = computed<string[]>(() => {
  if (!analysis.value) return []
  if (isAccountReport(report.value!)) {
    return (analysis.value as AccountAnalysis).action_suggestions
  }
  return (analysis.value as PostAnalysis).improvement_suggestions
})

// ── Stats display ─────────────────────────────────────────────────

const displayStats = computed<Record<string, { value: string; label: string }>>(() => {
  if (!report.value?.stats) return {}
  const s = report.value.stats as any

  if (isAccountReport(report.value)) {
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

// ── Formatters ────────────────────────────────────────────────────

const formatDate = (iso: string) => {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('zh-CN', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

const formatNum = (n: number) => {
  if (!n && n !== 0) return '-'
  if (n >= 10000) return (n / 10000).toFixed(1) + '万'
  return n.toString()
}

// ── Actions ────────────────────────────────────────────────────────

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href)
    copied.value = true
    setTimeout(() => (copied.value = false), 2000)
  } catch {
    // Silently fail
  }
}

// ── Load ───────────────────────────────────────────────────────────

onMounted(async () => {
  try {
    report.value = await getReport(reportId)
  } catch (e) {
    console.error('[report] failed to load:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.report-page { padding-bottom: 80px; }

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
.hero-meta { display: flex; align-items: center; gap: 10px; }
.btn-sm { padding: 8px 16px; font-size: 0.8125rem; }
.hero-title {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 8px;
  line-height: 1.35;
}
.hero-bio {
  font-size: 0.875rem;
  white-space: pre-line;
  margin-bottom: 16px;
  color: var(--text-secondary);
}
.post-meta { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
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
  line-height: 1.65;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.stats-section { padding: 0 0 24px; }
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }

.conclusions-section { padding: 0 0 24px; }
.conclusions-card { display: flex; flex-direction: column; gap: 16px; }
.conclusion-item { display: flex; gap: 12px; align-items: flex-start; }
.conclusion-icon { font-size: 1.125rem; flex-shrink: 0; margin-top: 2px; }
.conclusion-label { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
.conclusion-text { font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5; }
.conclusion-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.mt-6 { margin-top: 6px; }

.patterns-section { padding: 0 0 24px; }
.patterns-list { display: flex; flex-direction: column; gap: 8px; }
.pattern-item { display: flex; gap: 12px; align-items: flex-start; padding: 14px; }
.pattern-num { font-size: 0.875rem; font-weight: 800; color: var(--accent); flex-shrink: 0; }
.pattern-text { font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5; }

.structure-section { padding: 0 0 24px; }
.structure-step { display: flex; gap: 10px; align-items: flex-start; padding: 10px 0; border-bottom: 1px solid var(--border); }
.structure-step:last-of-type { border-bottom: none; }
.step-num { font-size: 0.75rem; font-weight: 700; color: var(--accent); flex-shrink: 0; min-width: 20px; }
.step-text { font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5; }
.structure-meta { padding-top: 4px; }

.topposts-section { padding: 0 0 24px; }
.post-list { display: flex; flex-direction: column; gap: 10px; }

.insights-section { padding: 0 0 24px; }

.suggestions-section { padding: 0 0 24px; }
.suggestions-list { display: flex; flex-direction: column; gap: 10px; }
.suggestion-item { display: flex; gap: 14px; align-items: flex-start; }
.suggestion-num { font-size: 1rem; font-weight: 800; color: var(--accent); flex-shrink: 0; line-height: 1.5; }
.suggestion-text { font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5; }

.sw-section { padding: 0 0 24px; }
.sw-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.sw-card .section-title { margin-bottom: 12px; }

.benchmark-section { padding: 0 0 24px; }

.report-cta { padding: 24px 0; }

.loading-state, .notfound-state {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.spinner.large { width: 40px; height: 40px; border-width: 3px; }

.notfound-icon {
  width: 64px; height: 64px;
  border-radius: 50%;
  background: var(--accent-dim);
  color: var(--accent);
  font-size: 2rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}
</style>
