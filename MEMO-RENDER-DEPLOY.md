# MEMO: Render 部署配置问题

**日期**: 2026-04-25
**问题**: GitHub push 不触发 Render 后端自动部署

## 诊断

```bash
gh api repos/landors615-gif/red-checking/hooks
# 返回: {"secrets":[],"total_count":0,"variables":[{"name":"NUXT_PUBLIC_API_BASE","value":"https://red-checking-backend.onrender.com"}]}
```

**结论**：GitHub repo 上没有任何 webhook。Render 也不是通过 GitHub Actions 部署后端。

Render 后端服务 `red-checking-backend.onrender.com` 疑似是**手动部署**的，之后没有再更新过。

## 解决方案

### 方案 A: Render 手动 Trigger Deploy（快速，最快 2 分钟）

1. 访问 https://dashboard.render.com
2. 登录 → 选择 `red-checking-api` 服务
3. 点击 **Manual Deploy** → **Deploy latest commit**
4. 等待部署完成（约 1-2 分钟）
5. 验证：新代码 `scraper_errors.py` 已加载

### 方案 B: 连接 GitHub 自动部署（长期，推荐）

1. 访问 https://dashboard.render.com
2. 选择 `red-checking-api` 服务 → **Settings**
3. 找到 **GitHub** 部分，点击 **Connect**
4. 选择 `landors615-gif/red-checking` repo
5. 选择要部署的分支（通常是 `main`）
6. 设置 **Root Directory** 为 `backend`（因为 main.py 在 backend/ 下）
7. 保存。以后 push 到 main 会自动触发部署

### 方案 C: GitHub Actions + Render Deploy Hook（需 RENDER_DEPLOY_HOOK_URL）

1. 在 Render Dashboard → `red-checking-api` 服务 → **Settings** → 找到 **Deploy Hook** URL
2. 在 GitHub repo 添加 secret: `RENDER_DEPLOY_HOOK_URL`
3. 创建 `.github/workflows/deploy-backend.yml`（参考下面模板）

**deploy-backend.yml 模板**:
```yaml
name: Deploy Backend to Render

on:
  push:
    branches: [main]
    paths: [backend/**]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Trigger Render Deploy
        run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
```

## 当前状态

| 项目 | 状态 |
|------|------|
| 后端代码 | `64867ec` 已 push 到 GitHub，未部署 |
| 新代码 | 本地验证 import 正常，错误分类逻辑正确 |
| 回归测试 | 待 Render 部署完成后执行 |
