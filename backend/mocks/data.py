"""
Mock data for Red Checking MVP.
Provides realistic mock data for both account and post analysis.
"""

MOCK_ACCOUNT_REPORT = {
    "reportId": "rpt_demo_account_001",
    "taskId": "task_demo_account_001",
    "type": "account",
    "generatedAt": "2026-04-10T15:00:00+08:00",
    "nickname": "美妆护肤实验室",
    "bio": "专注成分党测评 | 真实使用反馈 | 护肤干货分享\n📩合作请私信",
    "stats": {
        "followers": "12.8万",
        "following": 486,
        "likes_received": "98.6万",
        "posts_count": 328,
        "avg_likes": 3008,
        "avg_collects": 892,
        "avg_comments": 156,
    },
    "top_posts": [
        {
            "title": "这瓶精华液我用了28天，真实反馈来了",
            "cover": "https://placehold.co/600x400/pink/white?text=精华测评",
            "likes": 12800,
            "collects": 4200,
            "comments": 892,
        },
        {
            "title": "油皮夏季控油指南｜10款产品横向对比",
            "cover": "https://placehold.co/600x400/orange/white?text=控油对比",
            "likes": 9600,
            "collects": 3100,
            "comments": 643,
        },
        {
            "title": "早C晚A入门指南｜新手必看",
            "cover": "https://placehold.co/600x400/yellow/white?text=早C晚A",
            "likes": 8700,
            "collects": 2900,
            "comments": 521,
        },
        {
            "title": "敏感肌修护红宝书｜皮肤科医生推荐",
            "cover": "https://placehold.co/600x400/red/white?text=敏感肌",
            "likes": 7400,
            "collects": 2600,
            "comments": 478,
        },
    ],
    "analysis": {
        "account_summary": "该账号定位为「成分党美妆测评博主」，主要面向20-35岁对护肤成分有进阶需求的用户群体。内容以产品横评、单品深度测评、护肤知识科普为主，兼顾护肤步骤分享。账号内容质量稳定，互动数据健康，具备较高的商业合作价值和内容参考价值。",
        "positioning": "成分党美妆测评博主 — 强调专业性、真实性和科学护肤理念",
        "target_audience": "20-35岁都市女性，护肤进阶用户，注重成分与功效，对美妆产品有较高认知和选购需求",
        "content_topics": [
            "护肤品成分分析与横评",
            "早C晚A、抗氧化、敏感肌修护等功效护肤",
            "新品开箱与使用体验",
            "护肤步骤与产品搭配建议",
            "皮肤问题成因与解决方案",
        ],
        "viral_posts": [
            {
                "title": "这瓶精华液我用了28天，真实反馈来了",
                "reason": "28天实测周期建立信任感，结果导向的标题引发点击好奇",
            },
            {
                "title": "油皮夏季控油指南｜10款产品横向对比",
                "reason": "横向对比满足选购决策需求，数字具体增强可信度",
            },
        ],
        "title_patterns": [
            "效果+时间周期：'用了XX天，真实反馈来了'",
            "数字罗列型：'XX款产品横向对比'",
            "人群+痛点型：'敏感肌修护指南'",
            "知识科普型：'入门指南｜新手必看'",
        ],
        "content_patterns": [
            "封面统一风格，人物+产品组合出镜",
            "正文结构：痛点引入→成分分析→使用感受→效果对比→总结推荐",
            "高频使用对比图：使用前后、多个产品并列",
            "评论区主动回复，建立互动和信任感",
        ],
        "comment_insights": {
            "high_freq_questions": [
                "XX产品适合我吗？",
                "和XX比哪个好？",
                "敏感肌可以用吗？",
                "多少钱？哪里买？",
            ],
            "user_sentiment": "正面为主，用户信任度高，评论区互动意愿强",
            "key_demands": "个性化产品推荐、使用方法指导、购买渠道确认",
        },
        "strengths": [
            "内容垂直度高，目标用户精准",
            "实测周期长，数据可信度高",
            "标题结构稳定，SEO友好",
            "评论区运营好，用户粘性强",
        ],
        "weaknesses": [
            "内容形式单一，缺乏视频/直播内容",
            "爆款内容依赖标题，长期来看存在疲劳风险",
            "缺乏清晰的账号人设故事线",
        ],
        "benchmarking": {
            "similar_accounts": ["KOL A（50万粉）", "KOL B（20万粉）"],
            "data_reference": "同类账号平均互动率约2.8%，该账号约2.9%，略高于均值",
        },
        "action_suggestions": [
            "可借鉴其横向测评的内容框架",
            "标题可参考'数字+对比+效果'的结构",
            "建议补充人设故事线，提升账号辨识度",
            "评论区高频问题可作为选题参考",
        ],
    },
}


MOCK_POST_REPORT = {
    "reportId": "rpt_demo_post_001",
    "taskId": "task_demo_post_001",
    "type": "post",
    "generatedAt": "2026-04-10T15:05:00+08:00",
    "post_title": "这瓶精华液我用了28天，真实反馈来了",
    "published_at": "2026-03-28",
    "post_tags": ["精华液", "护肤测评", "成分党", "敏感肌", "早C晚A"],
    "stats": {
        "likes": 12800,
        "collects": 4200,
        "comments": 892,
        "shares": 1203,
        "cover": "https://placehold.co/600x400/pink/white?text=精华测评",
    },
    "top_posts": [
        {
            "title": "这瓶精华液我用了28天，真实反馈来了",
            "cover": "https://placehold.co/600x400/pink/white?text=精华测评",
            "likes": 12800,
            "collects": 4200,
            "comments": 892,
        },
    ],
    "analysis": {
        "post_summary": "这是一篇典型的护肤品测评帖子，作者以28天实测为切入点，通过图文并茂的方式展示产品使用效果。帖子结构清晰，从痛点引入到成分分析，再到使用感受和效果对比，最后给出总结推荐。整体内容质量较高，互动数据优异，具备较强的种草属性。",
        "theme": "精华液产品测评 — 功效护肤、成分党风格",
        "title_analysis": {
            "structure": "效果+时间周期型",
            "techniques": [
                "设置悬念：'真实反馈来了'引发点击",
                "时间锚定：'28天'建立专业感和可信度",
                "结果导向：直接点明用户最关心的'效果'",
            ],
            "keywords": ["精华液", "28天", "真实反馈"],
        },
        "structure_analysis": {
            "outline": [
                "开场：皮肤问题和选购痛点引入",
                "产品介绍：外观、成分、适用肤质",
                "使用感受：质地、吸收、肤感",
                "效果展示：使用前后对比、阶段记录",
                "总结：推荐指数、适合人群、购买建议",
            ],
            "length": "中等篇幅，约500-800字",
            "format": "图文结合，封面图+正文图片+总结图",
        },
        "emotional_hooks": [
            "真实使用记录消除了用户对'恰饭推广'的戒备",
            "28天周期给人'认真做了这件事'的信任感",
            "皮肤改善对比图直接刺激用户欲望",
        ],
        "value_points": [
            "提供了购买决策所需的功效信息",
            "明确适合人群，降低选购门槛",
            "客观呈现优缺点，可信度高",
        ],
        "conflict_points": [
            "实测周期较长，用户等待成本高",
            "单人使用感受不代表普遍效果",
            "价格信息缺失，用户需要主动搜索",
        ],
        "spread_factors": [
            "封面图对比强烈，刺激收藏动机",
            "评论区有大量'求链接'互动，带动二次传播",
            "护肤测评类内容搜索流量稳定，长尾效应明显",
        ],
        "comment_insights": {
            "high_freq_questions": [
                "适合油皮吗？",
                "和某某精华比怎么样？",
                "多少钱？",
                "敏感肌能用吗？",
            ],
            "user_sentiment": "正面为主，用户购买意愿强，评论区互动活跃",
            "key_demands": "个性化适用性判断、价格信息、产品对比",
        },
        "benchmark_reference": {
            "avg_likes_in_category": 6500,
            "this_post_likes": 12800,
            "percentile": "前15%",
        },
        "improvement_suggestions": [
            "建议补充价格区间和购买渠道信息",
            "可增加不同肤质的对比使用反馈",
            "建议固定更新频率，建立粉丝预期",
            "视频版内容可能带来更高的完播率和转化",
        ],
    },
}


# ── Edge case: small/new account ─────────────────────────────────────────────

MOCK_SMALL_ACCOUNT_REPORT = {
    "reportId": "rpt_demo_small_001",
    "taskId": "task_demo_small_001",
    "type": "account",
    "generatedAt": "2026-04-10T15:10:00+08:00",
    "nickname": "护肤新手日记",
    "bio": "从零开始的护肤记录｜分享真实使用感受\n偶尔踩坑偶尔种草",
    "stats": {
        "followers": "386",
        "following": 201,
        "likes_received": "1200",
        "posts_count": 18,
        "avg_likes": 67,
        "avg_collects": 12,
        "avg_comments": 3,
    },
    "top_posts": [
        {
            "title": "第一次刷酸｜新手必看记录",
            "cover": "https://placehold.co/600x400/lightblue/white?text=刷酸记录",
            "likes": 320,
            "collects": 98,
            "comments": 24,
        },
        {
            "title": "平价水乳分享｜学生党友好",
            "cover": "https://placehold.co/600x400/lightgreen/white?text=平价水乳",
            "likes": 180,
            "collects": 62,
            "comments": 11,
        },
    ],
    "analysis": {
        "account_summary": "该账号处于起步阶段，主要记录个人护肤学习过程，内容真实感强但缺乏系统性。粉丝基数小，互动数据偏低，但评论区用户多为同类新手，具有较强的共情基础。账号有一定成长空间，需要找准差异化定位。",
        "positioning": "护肤新手成长记录博主 — 真实、接地气、陪伴感",
        "target_audience": "护肤新手（18-24岁），对学生党平价产品有需求，愿意看真实记录而非专业测评",
        "content_topics": [
            "新手护肤入门记录",
            "平价产品使用反馈",
            "护肤踩坑经验分享",
            "产品开箱与平替推荐",
        ],
        "viral_posts": [
            {
                "title": "第一次刷酸｜新手必看记录",
                "reason": "高风险护肤行为的新手指南，标题锁定目标人群，收藏率高",
            },
        ],
        "title_patterns": [
            "新手/入门型：'第一次XX｜新手必看'",
            "价格锚定型：'平价分享｜学生党友好'",
            "记录型：'XX天记录｜真实反馈'",
        ],
        "content_patterns": [
            "以个人经历为线索，情感真实",
            "缺少专业数据支撑，但用户共情强",
            "封面以自拍为主，缺少统一视觉风格",
            "内容篇幅较短，信息密度有限",
        ],
        "comment_insights": {
            "high_freq_questions": [
                "用了什么产品？",
                "有爆痘吗？",
                "多少钱？",
                "适合干皮吗？",
            ],
            "user_sentiment": "正面偏好奇，用户愿意互动但基数小",
            "key_demands": "产品具体名称、价格、适合肤质",
        },
        "strengths": [
            "真实感强，不做作",
            "目标人群明确（新手党）",
            "评论区互动意愿较高",
        ],
        "weaknesses": [
            "内容同质化严重，新手赛道拥挤",
            "缺少专业性，难以建立信任壁垒",
            "粉丝基数太低，变现困难",
            "视觉风格不统一，辨识度低",
        ],
        "benchmarking": {
            "similar_accounts": ["新手护肤博主A（2000粉）", "护肤日记B（5000粉）"],
            "data_reference": "同类新账号平均互动率约1.5%，该账号约1.8%，有一定潜力",
        },
        "action_suggestions": [
            "建议选择一个垂直细分方向（如刷酸/敏感肌）做深度内容",
            "可参考'新手踩坑→解决方案'的结构化内容框架",
            "统一封面风格，提升账号视觉辨识度",
            "评论区高频问题可作为固定FAQ降低重复回复成本",
        ],
    },
}
