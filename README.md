# Inference Serving 全景：从指标、瓶颈到框架与生态

作者：**kzhoulatte** · 2026 年 10 月 · 第 1 版

这是一份面向面试准备的 inference serving 系统笔记。它沿“要求 → 限制 → 问题 → 解法”展开，从 LLM serving 讲起，再扩展到 MoE、大规模集群、推理框架、后训练（RL rollout）、Omni / 语音、扩散模型、机器人、Coding Agent、AI for Science，最后是 sandbox 等相关技术、公司与开源生态、源码导读和面试速查。

- **网页版**：[`index.html`](index.html)。打开后先看到全景地图，点击地点会在右侧打开对应章节；支持深浅色和手机。
- **PDF 版**：[`inference-serving-guide.pdf`](inference-serving-guide.pdf)，75 页。包含封面、可点击的目录，每章以全景地图的局部截面开头。

## 内容

| # | 章节 | # | 章节 |
|---|---|---|---|
| 01 | 推理服务本身：要求与指标 | 10 | 扩散模型推理 |
| 02 | 物理限制：为什么 LLM 推理难 | 11 | 机器人推理 |
| 03 | 需要解决的问题 | 12 | Coding Agent 的推理 |
| 04 | LLM serving 的核心技术 | 13 | AI for Science 的推理 |
| 05 | 扩展到 MoE | 14 | 相关技术：sandbox、网关、观测 |
| 06 | 扩展到大规模集群 | 15 | 公司与开源项目地图 |
| 07 | LLM 推理框架 | 16 | 源码导读 |
| 08 | 后训练里的推理 | 17 | 面试速查 |
| 09 | Omni / 语音 / 多模态 | 18 | 参考文献 |

文中约 180 个源码链接都固定在具体 commit，见 [`src/pins.txt`](src/pins.txt)，并附有 Google Code Wiki 链接。

## 从源码重新生成

```bash
cd src
./fetch_trees.sh        # 按 pins.txt 拉取各仓库的文件树，用于校验源码链接（需要已登录的 gh）
./build.sh              # 拼接 parts/ 并展开源码链接 → ../index.html；有路径不存在时报错退出
python make_pdf.py      # 需要 google-chrome、pypdf、reportlab → ../inference-serving-guide.pdf
```

- `src/parts/`：页面分片，包括样式、各章内容、地图（`p8_atlas.html`）和图表引擎（`p9_engine.html`）。
- `src/print_front.html`、`src/print_inject.html`：只用于 PDF 的封面、目录和章首地图。
- `src/expand.py`：展开 `{{s:owner/repo:path|label}}` 等源码链接宏，并核对路径是否存在。

## 声明

本文由 kzhoulatte 编写整理，用于个人学习与面试准备。内容整理自公开的论文、官方文档与开源代码，文中的归纳、取舍与观点仅代表作者本人，不代表任何雇主或开源项目。行业与生态信息截至约 2026 年中，可能已经变化；示意图中的曲线与数字除注明出处者外均为示意。引用或转载请注明作者与出处。
