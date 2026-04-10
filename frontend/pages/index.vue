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
          <div class="input-wrap" :class="{ 'input-wrap--error': validationError }">
            <input
              v-model="url"
              class="input"
              type="url"
              placeholder="粘贴小红书账号或帖子链接..."
              :disabled="loading"
              @input="validationError = ''"
              @keydown.enter="url.value.trim() && startAnalysis()"
            />
            <button
              v-if="url"
              class="clear-btn"
              tabindex="-1"
              aria-label="清除"
              @click="url = ''; validationError = ''"
            >
              ×
            </button>
          </div>

          <!-- Validation hint -->
          <p v-if="validationError" class="validation-msg">{{ validationError }}</p>
          <p v-else-if="url && !validationError" class="validation-hint">
            检测到：<span class="text-accent">{{ detectedType }}</span>
          </p>

          <button
            class="btn btn-primary w-full mt-12"
            :disabled="!url.value.trim() || loading"
            @click="startAnalysis"
          >
            <span v-if="loading" class="spinner" />
            <span v-else>开始检测</span>
          </button>
        </div>

        <p class="support-note animate-slideUp">
          支持 <span class="text-accent">账号链接</span> 与 <span class="text-accent">帖子链接</span>
        </p>
      </div>
    </section>

    <!-- URL format hints -->
    <section v-if="showHints" class="hints-section">
      <div class="container">
        <div class="hints-card card animate-slideUp">
          <p class="hints-title">支持的链接格式：</p>
          <div class="hint-item">
            <span class="hint-icon">👤</span>
            <div>
              <p class="hint-type">账号链接</p>
              <p class="hint-example">xhslink.com/xxx/profile/xxx</p>
            </div>
          </div>
          <div class="hint-item">
            <span class="hint-icon">📝</span>
            <div>
              <p class="hint-type">帖子链接</p>
              <p class="hint-example">xiaohongshu.com/explore/xxx</p>
            </div>
          </div>
        </div>
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
        <p class="section-label">适用场景</p>
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
        <p class="section-label">示例报告</p>
        <div class="demo-list stagger">
          <NuxtLink to="/report/rpt_demo_account_001" class="demo-item card animate-slideUp">
            <div class="demo-top">
              <span class="badge badge-red">账号检测</span>
            </div>
            <div class="demo-title">美妆护肤实验室</div>
            <div class="demo-desc">12.8万粉成分党测评博主，爆文规律与评论区洞察</div>
            <div class="demo-stats">
              <span>👥 12.8万粉丝</span>
              <span>❤️ 98.6万获赞</span>
            </div>
          </NuxtLink>

          <NuxtLink to="/report/rpt_demo_post_001" class="demo-item card animate-slideUp">
            <div class="demo-top">
              <span class="badge badge-red">帖子检测</span>
            </div>
            <div class="demo-title">这瓶精华液我用了28天，真实反馈来了</div>
            <div class="demo-desc">12800点赞爆文，标题结构与传播因子拆解</div>
            <div class="demo-stats">
              <span>❤️ 1.28万点赞</span>
              <span>⭐ 4200收藏</span>
            </div>
          </NuxtLink>

          <NuxtLink to="/report/rpt_demo_small_001" class="demo-item card animate-slideUp">
            <div class="demo-top">
              <span class="badge badge-red">账号检测</span>
              <span class="demo-new-tag">新账号</span>
            </div>
            <div class="demo-title">护肤新手日记</div>
            <div class="demo-desc">386粉新手博主，成长瓶颈与定位分析</div>
            <div class="demo-stats">
              <span>👥 386粉丝</span>
              <span>📝 18篇笔记</span>
            </div>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- Footer -->
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
const validationError = ref('')

// ── Client-side URL type detection for instant feedback ──────────

const XHS_ACCOUNT_PATTERNS = [
  /xhslink\.com\/[^/]+\/profile\//i,
  /xiaohongshu\.com\/user\/profile\//i,
]
const XHS_POST_PATTERNS = [
  /xhslink\.com\/[^/]+\/explore\//i,
  /xiaohongshu\.com\/explore\//i,
  /xiaohongshu\.com\/discovery\/item\//i,
]

const detectedType = computed(() => {
  const u = url.value.trim().toLowerCase()
  if (!u) return ''
  if (XHS_ACCOUNT_PATTERNS.some((p) => p.test(u))) return '账号'
  if (XHS_POST_PATTERNS.some((p) => p.test(u))) return '帖子'
  return ''
})

const showHints = computed(() => {
  return !url.trim() || detectedType.value === ''
})

// ── Validation ───────────────────────────────────────────────────

const validateInput = (): boolean => {
  const u = url.value.trim()
  if (!u) {
    validationError.value = '请输入小红书链接'
    return false
  }
  const hasXHS = /xiaohongshu|xhslink/i.test(u)
  if (!hasXHS) {
    validationError.value = '请输入小红书链接（目前仅支持小红书）'
    return false
  }
  validationError.value = ''
  return true
}

// ── Submit ────────────────────────────────────────────────────────

const startAnalysis = async () => {
  if (!validateInput()) return
  loading.value = true
  validationError.value = ''
  try {
    const res = await createTask(url.value.trim())
    router.push(`/analyzing/${res.taskId}`)
  } catch (e: any) {
    const detail = e?.data?.detail
    if (detail) {
      validationError.value = String(detail)
    } else {
      validationError.value = '网络错误，请检查链接后重试'
    }
    loading.value = false
  }
}
</script>

<style scoped>
.hero { padding: 60px 0 40px; }
.brand { display: inline-flex; align-items: center; gap: 10px; margin-bottom: 28px; }
.brand-mark {
  width: 36px; height: 36px;
  background: var(--accent);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 1.125rem; color: white;
}
.brand-name { font-size: 1rem; font-weight: 700; color: var(--text-primary); }
.hero-title { font-size: 1.625rem; line-height: 1.3; margin-bottom: 12px; color: var(--text-primary); }
.hero-sub { font-size: 0.875rem; margin-bottom: 32px; }
.input-group { margin-bottom: 12px; }

.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}
.input-wrap .input {
  padding-right: 40px;
}
.input-wrap--error .input {
  border-color: var(--accent);
}
.clear-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 1.25rem;
  cursor: pointer;
  padding: 4px;
  line-height: 1;
}
.clear-btn:hover { color: var(--text-primary); }

.validation-msg { font-size: 0.8125rem; color: var(--accent); margin-top: 6px; }
.validation-hint { font-size: 0.8125rem; color: var(--text-muted); margin-top: 6px; }
.support-note { font-size: 0.75rem; text-align: center; }

.hints-section { padding: 0 0 24px; }
.hints-card { display: flex; flex-direction: column; gap: 12px; }
.hints-title { font-size: 0.8125rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px; }
.hint-item { display: flex; gap: 10px; align-items: flex-start; }
.hint-icon { font-size: 1.125rem; flex-shrink: 0; }
.hint-type { font-size: 0.8125rem; font-weight: 600; color: var(--text-primary); }
.hint-example { font-size: 0.75rem; color: var(--text-muted); font-family: monospace; }

.value-section { padding: 0 0 32px; }
.value-grid { display: flex; flex-direction: column; gap: 12px; }
.value-card { display: flex; flex-direction: column; gap: 8px; }
.value-icon { font-size: 1.5rem; }
.value-card h3 { font-size: 0.9375rem; }
.value-card p { font-size: 0.8125rem; }

.cases-section { padding: 0 0 32px; }
.cases { display: flex; flex-wrap: wrap; gap: 8px; }
.case-tag {
  padding: 8px 14px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 99px;
  font-size: 0.8125rem; color: var(--text-secondary);
}

.demo-section { padding: 0 0 100px; }
.demo-list { display: flex; flex-direction: column; gap: 12px; }
.demo-item {
  display: flex; flex-direction: column; gap: 6px;
  text-decoration: none;
  transition: border-color 0.2s, transform 0.2s;
}
.demo-item:hover { border-color: var(--accent); transform: translateY(-1px); }
.demo-top { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; }
.demo-new-tag {
  padding: 2px 8px;
  background: rgba(76, 175, 80, 0.15);
  color: var(--success);
  border-radius: 99px;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.demo-title { font-weight: 700; font-size: 0.9375rem; color: var(--text-primary); }
.demo-desc { font-size: 0.8125rem; color: var(--text-muted); }
.demo-stats { display: flex; gap: 16px; font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }

.footer-note { padding: 16px 0 32px; }
</style>
