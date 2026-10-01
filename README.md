# 运筹学 学习助手

北航「运筹学(1)」课程（2026秋季学期）的 AI 学习伙伴，沿用「概率统计-Study」的引导式学习方法（Guided Learning），按运筹学的特点改造成**建模 / 算法迭代 / 理论解释**三种学习模式。

## 这是什么

- **建模题**：不直接给模型，引导你自己找决策变量、写目标函数和约束，再逐条检查漏洞
- **算法题**（单纯形表、大M法、两阶段法……）：一张表一张表推进，每张表都自检，最后给出可誊抄的完整解答
- **理论题**：几何直观（可行域、顶点）和代数表示（基可行解、检验数）来回对照
- 分步解题生成可交互 HTML（KaTeX 渲染、单纯形表逐张展开、主元高亮）
- 每道题用 Python 求解器（`/models/`）交叉验证
- 每次学习对话记录 session notes，更新唯一的进度总账 `/progress/operations-research-tracker.md`

具体教学规则都写在 `CLAUDE.md` 里。

## 两种用法

### 方式一：Claude Code 仓库（推荐，记录会同步到 GitHub）

```bash
cd 运筹学-Study
claude
```

直接开始问运筹学相关的问题，Claude 会按 `CLAUDE.md` 引导你，把记录写进 `/sessions/`、更新 tracker、把解答存进 `/solutions/`、验证脚本存进 `/models/`，结束时合并进 GitHub `main`。

每次老师发了新课件/作业，放进 `/materials/`（作业放 `/materials/作业/`），下次对话时提一句"我上传了新材料"。

### 方式二：claude.ai Project 内使用

把 `claude-ai-project-instructions.md` 的内容复制粘贴进 Project 的「自定义说明 / Custom instructions」，课件作为 Project 知识文件上传。

## 文件夹结构

```
materials/        课件 PDF（chNN-第N节-标题.pdf）
materials/作业/   作业 PDF（hwNN-第NN次作业题.pdf）
solutions/        分步解题 HTML（浏览器直接打开）
models/           标准模型 + 求解器验证脚本（需要 pip install scipy numpy）
summaries/        每章知识点/易错点总结
sessions/         每次学习的 session notes
progress/         唯一进度总账
```
