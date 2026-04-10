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

// ── Demo reports (embedded — works without backend) ────────────────────

const DEMO_REPORTS: Record<string, ReportResponse> = {
  'rpt_demo_account_001': {
    reportId: 'rpt_demo_account_001',
    taskId: 'task_demo_account_001',
    type: 'account',
    generatedAt: '2026-04-10T15:00:00+08:00',
    nickname: '美妆护肤实验室',
    bio: '专注成分党测评 | 真实使用反馈 | 护肤干货分享\n📩合作请私信',
    stats: {
      followers: '12.8万',
      following: 486,
      likes_received: '98.6万',
      posts_count: 328,
      avg_likes: 3008,
      avg_collects: 892,
      avg_comments: 156,
    },
    top_posts: [
      { title: '这瓶精华液我用了28天，真实反馈来了', cover: 'https://placehold.co/600x400/pink/white?text=精华测评', likes: 12800, collects: 4200, comments: 892 },
      { title: '油皮夏季控油指南｜10款产品横向对比', cover: 'https://placehold.co/600x400/orange/white?text=控油对比', likes: 9600, collects: 3100, comments: 643 },
      { title: '早C晚A入门指南｜新手必看', cover: 'https://placehold.co/600x400/yellow/white?text=早C晚A', likes: 8700, collects: 2900, comments: 521 },
      { title: '敏感肌修护红宝书｜皮肤科医生推荐', cover: 'https://placehold.co/600x400/red/white?text=敏感肌', likes: 7400, collects: 2600, comments: 478 },
    ],
    analysis: {
      account_summary: '该账号定位为「成分党美妆测评博主」，主要面向20-35岁对护肤成分有进阶需求的用户群体。内容以产品横评、单品深度测评、护肤知识科普为主，兼顾护肤步骤分享。账号内容质量稳定，互动数据健康，具备较高的商业合作价值和内容参考价值。',
      positioning: '成分党美妆测评博主 — 强调专业性、真实性和科学护肤理念',
      target_audience: '20-35岁都市女性，护肤进阶用户，注重成分与功效，对美妆产品有较高认知和选购需求',
      content_topics: ['护肤品成分分析与横评', '早C晚A、抗氧化、敏感肌修护等功效护肤', '新品开箱与使用体验', '护肤步骤与产品搭配建议', '皮肤问题成因与解决方案'],
      viral_posts: [
        { title: '这瓶精华液我用了28天，真实反馈来了', reason: "28天实测周期建立信任感，结果导向的标题引发点击好奇" },
        { title: '油皮夏季控油指南｜10款产品横向对比', reason: '横向对比满足选购决策需求，数字具体增强可信度' },
      ],
      title_patterns: ["效果+时间周期：「用了XX天，真实反馈来了」", "数字罗列型：「XX款产品横向对比」", "人群+痛点型：「敏感肌修护指南」", "知识科普型：「入门指南｜新手必看」"],
      content_patterns: ['封面统一风格，人物+产品组合出镜', '正文结构：痛点引入→成分分析→使用感受→效果对比→总结推荐', '高频使用对比图：使用前后、多个产品并列', '评论区主动回复，建立互动和信任感'],
      comment_insights: { high_freq_questions: ['XX产品适合我吗？', '和XX比哪个好？', '敏感肌可以用吗？', '多少钱？哪里买？'], user_sentiment: '正面为主，用户信任度高，评论区互动意愿强', key_demands: '个性化产品推荐、使用方法指导、购买渠道确认' },
      strengths: ['内容垂直度高，目标用户精准', '实测周期长，数据可信度高', '标题结构稳定，SEO友好', '评论区运营好，用户粘性强'],
      weaknesses: ['内容形式单一，缺乏视频/直播内容', '爆款内容依赖标题，长期来看存在疲劳风险', '缺乏清晰的账号人设故事线'],
      benchmarking: { similar_accounts: ['KOL A（50万粉）', 'KOL B（20万粉）'], data_reference: '同类账号平均互动率约2.8%，该账号约2.9%，略高于均值' },
      action_suggestions: ['可借鉴其横向测评的内容框架', '标题可参考「数字+对比+效果」的结构', '建议补充人设故事线，提升账号辨识度', '评论区高频问题可作为选题参考'],
    },
  },
  'rpt_demo_post_001': {
    reportId: 'rpt_demo_post_001',
    taskId: 'task_demo_post_001',
    type: 'post',
    generatedAt: '2026-04-10T15:05:00+08:00',
    post_title: '这瓶精华液我用了28天，真实反馈来了',
    published_at: '2026-03-28',
    post_tags: ['精华液', '护肤测评', '成分党', '敏感肌', '早C晚A'],
    stats: { likes: 12800, collects: 4200, comments: 892, shares: 1203, cover: 'https://placehold.co/600x400/pink/white?text=精华测评' },
    top_posts: [{ title: '这瓶精华液我用了28天，真实反馈来了', cover: 'https://placehold.co/600x400/pink/white?text=精华测评', likes: 12800, collects: 4200, comments: 892 }],
    analysis: {
      post_summary: '这是一篇典型的护肤品测评帖子，作者以28天实测为切入点，通过图文并茂的方式展示产品使用效果。帖子结构清晰，从痛点引入到成分分析，再到使用感受和效果对比，最后给出总结推荐。整体内容质量较高，互动数据优异，具备较强的种草属性。',
      theme: '精华液产品测评 — 功效护肤、成分党风格',
      title_analysis: { structure: '效果+时间周期型', techniques: ['设置悬念：「真实反馈来了」引发点击', "时间锚定：「28天」建立专业感和可信度", '结果导向：直接点明用户最关心的「效果」'], keywords: ['精华液', '28天', '真实反馈'] },
      structure_analysis: { outline: ['开场：皮肤问题和选购痛点引入', '产品介绍：外观、成分、适用肤质', '使用感受：质地、吸收、肤感', '效果展示：使用前后对比、阶段记录', '总结：推荐指数、适合人群、购买建议'], length: '中等篇幅，约500-800字', format: '图文结合，封面图+正文图片+总结图' },
      emotional_hooks: ['真实使用记录消除了用户对「恰饭推广」的戒备', "28天周期给人「认真做了这件事」的信任感", '皮肤改善对比图直接刺激用户欲望'],
      value_points: ['提供了购买决策所需的功效信息', '明确适合人群，降低选购门槛', '客观呈现优缺点，可信度高'],
      conflict_points: ['实测周期较长，用户等待成本高', '单人使用感受不代表普遍效果', '价格信息缺失，用户需要主动搜索'],
      spread_factors: ['封面图对比强烈，刺激收藏动机', "评论区有大量'求链接'互动，带动二次传播", '护肤测评类内容搜索流量稳定，长尾效应明显'],
      comment_insights: { high_freq_questions: ['适合油皮吗？', '和某某精华比怎么样？', '多少钱？', '敏感肌能用吗？'], user_sentiment: '正面为主，用户购买意愿强，评论区互动活跃', key_demands: '个性化适用性判断、价格信息、产品对比' },
      benchmark_reference: { avg_likes_in_category: 6500, this_post_likes: 12800, percentile: '前15%' },
      improvement_suggestions: ['建议补充价格区间和购买渠道信息', '可增加不同肤质的对比使用反馈', '建议固定更新频率，建立粉丝预期', '视频版内容可能带来更高的完播率和转化'],
    },
  },
  'rpt_demo_small_001': {
    reportId: 'rpt_demo_small_001',
    taskId: 'task_demo_small_001',
    type: 'account',
    generatedAt: '2026-04-10T15:10:00+08:00',
    nickname: '护肤新手日记',
    bio: '从零开始的护肤记录｜分享真实使用感受\n偶尔踩坑偶尔种草',
    stats: { followers: '386', following: 201, likes_received: '1200', posts_count: 18, avg_likes: 67, avg_collects: 12, avg_comments: 3 },
    top_posts: [
      { title: '第一次刷酸｜新手必看记录', cover: 'https://placehold.co/600x400/lightblue/white?text=刷酸记录', likes: 320, collects: 98, comments: 24 },
      { title: '平价水乳分享｜学生党友好', cover: 'https://placehold.co/600x400/lightgreen/white?text=平价水乳', likes: 180, collects: 62, comments: 11 },
    ],
    analysis: {
      account_summary: '该账号处于起步阶段，主要记录个人护肤学习过程，内容真实感强但缺乏系统性。粉丝基数小，互动数据偏低，但评论区用户多为同类新手，具有较强的共情基础。账号有一定成长空间，需要找准差异化定位。',
      positioning: '护肤新手成长记录博主 — 真实、接地气、陪伴感',
      target_audience: '护肤新手（18-24岁），对学生党平价产品有需求，愿意看真实记录而非专业测评',
      content_topics: ['新手护肤入门记录', '平价产品使用反馈', '护肤踩坑经验分享', '产品开箱与平替推荐'],
      viral_posts: [{ title: '第一次刷酸｜新手必看记录', reason: '高风险护肤行为的新手指南，标题锁定目标人群，收藏率高' }],
      title_patterns: ["新手/入门型：「第一次XX｜新手必看」", "价格锚定型：「平价分享｜学生党友好」", "记录型：「XX天记录｜真实反馈」"],
      content_patterns: ['以个人经历为线索，情感真实', '缺少专业数据支撑，但用户共情强', '封面以自拍为主，缺少统一视觉风格', '内容篇幅较短，信息密度有限'],
      comment_insights: { high_freq_questions: ['用了什么产品？', '有爆痘吗？', '多少钱？', '适合干皮吗？'], user_sentiment: '正面偏好奇，用户愿意互动但基数小', key_demands: '产品具体名称、价格、适合肤质' },
      strengths: ['真实感强，不做作', '目标人群明确（新手党）', '评论区互动意愿较高'],
      weaknesses: ['内容同质化严重，新手赛道拥挤', '缺少专业性，难以建立信任壁垒', '粉丝基数太低，变现困难', '视觉风格不统一，辨识度低'],
      benchmarking: { similar_accounts: ['新手护肤博主A（2000粉）', '护肤日记B（5000粉）'], data_reference: '同类新账号平均互动率约1.5%，该账号约1.8%，有一定潜力' },
      action_suggestions: ['建议选择一个垂直细分方向（如刷酸/敏感肌）做深度内容', "可参考'新手踩坑→解决方案'的结构化内容框架", '统一封面风格，提升账号视觉辨识度', '评论区高频问题可作为固定FAQ降低重复回复成本'],
    },
  },
}

// ── Load ───────────────────────────────────────────────────────────

onMounted(async () => {
  // Demo reports work without backend
  if (DEMO_REPORTS[reportId]) {
    report.value = DEMO_REPORTS[reportId]
    loading.value = false
    return
  }
  // Live reports require backend
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
