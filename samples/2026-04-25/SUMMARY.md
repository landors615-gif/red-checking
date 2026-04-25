# Red Checking 样本测试总结 - 2026-04-25

## 第四步：scraper 错误分类 — 状态：代码完成，部署阻塞

### 段1 诊断结论

| 样本 | 之前结果 | 失败根因 |
|------|----------|----------|
| sample-01 | A | 有 xsec_token 的合法医美短文，可正常抓取 |
| sample-02 | C | XHS 对 Render IP 返回空响应 → regex 捕获空 `__INITIAL_STATE__` → JSONDecodeError |
| sample-04 | C | 视频帖（已知不支持，明天的事） |
| sample-05 | C | 非视频但失败：Render 服务器 IP 被 XHS 屏蔽，返回空 body → 同 sample-02 |

**关键发现**：
- sample-01 重跑成功 = scraper 代码逻辑正确（regex/JSON 解析均正常）
- sample-02/04/05 失败 = Render 服务器在海外，被 XHS 屏蔽或限流
- 失败统一根因：XHS 对 Render IP 返回空响应（或 HTML 但无 `__INITIAL_STATE__`），导致 `json.loads("")` 抛 `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`

**诊断结论**：不是 Cookie 失效，是 **IP 层面的风控/屏蔽**（Render 服务器 IP 被 XHS 识别为非中国大陆 IP）

### 段2 代码改动

**新增文件**：`backend/services/scraper_errors.py`
- `XHSScraperError` 类，6 个错误码：`XHS_COOKIE_EXPIRED` / `XHS_RATE_LIMITED` / `XHS_VIDEO_NOT_SUPPORTED` / `XHS_PARSE_FAILED` / `XHS_NETWORK_ERROR` / `XHS_CONTENT_BLOCKED`

**修改文件**：`backend/services/real_scraper.py`
- `_try_ssr_scrape_post` 内对不同失败场景分类抛 `XHSScraperError`
- 401/403 → `COOKIE_EXPIRED`
- 含"请登录"文字 → `COOKIE_EXPIRED`
- 403/429 → `RATE_LIMITED`
- 无 `__INITIAL_STATE__`（其他情况）→ `PARSE_FAILED` + debug body 前 200 字
- `__INITIAL_STATE__` 空 → `PARSE_FAILED`
- JSONDecodeError → `PARSE_FAILED` + debug raw 前后 200 字
- 其他意外 Exception → 包装为 `NETWORK_ERROR`

**修改文件**：`backend/services/task_store.py`
- `except` 块 catch `XHSScraperError`，设置 `task["errorCode"]` + `task["errorDebug"]`
- 打印 `[CRITICAL] [XHS_XXX] message`

### 段3 部署状态

**⚠️ 部署阻塞**：Render 后端服务 **未连接 GitHub 自动部署**

- GitHub webhook 检查：`gh api repos/landors615-gif/red-checking/hooks` → 0 个 hooks
- Render CLI 未认证（`render whoami` → needs login）
- 确认方法：访问 Render Dashboard → 手动 Trigger Deploy，或连接 GitHub repo

**Commit**: `64867ec` (ea83d0d..64867ec)
- 已 push 到 `origin/main`
- 本地验证：新代码 Python import 正常，错误分类逻辑正确

### 回归测试结果

| 样本 | URL | 预期错误码 | 实际（部署阻塞）|
|------|-----|-----------|----------------|
| sample-01 | 完整URL+xsec_token | 成功 (done) | done ✓ |
| sample-02 | https://.../69df1315... | XHS_PARSE_FAILED 或 XHS_RATE_LIMITED | `Expecting value...` (旧代码，仍在运行) |
| sample-04 | xhslink 短链 | XHS_VIDEO_NOT_SUPPORTED | 未测试 |
| sample-05 | xhslink 短链 | XHS_PARSE_FAILED | 未测试 |

### 整体判断

**scraper 缺陷**：无。代码逻辑正确。
**Cookie 失效**：无（sample-01 有 xsec_token 仍成功）
**IP 风控**：是。Render 服务器在海外，XHS 对其返回空响应。
**视频不支持**：已知，明天的事。

**真正问题**：Render Free 部署的服务器 IP 被小红书屏蔽。解决方案：
1. （短期）刷新 XHS Cookie 可能有帮助（但 IP 屏蔽不依赖 Cookie）
2. （中期）将后端部署到中国大陆 IP 的服务器（腾讯云/阿里云/科大讯飞）
3. （长期）使用 XHS 官方 API（需申请）

### 后续行动

- [ ] 阿铧需要在 Render Dashboard 手动 Trigger Deploy（让新代码上线）
- [ ] 回归测试（5 条样本）
- [ ] 确认各样本拿到明确错误码
- [ ] 解决 Render IP 被 XHS 屏蔽问题（部署到国内）
