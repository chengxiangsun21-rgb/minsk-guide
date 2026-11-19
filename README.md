# 明斯克城市漫游指南 —— Python 生成网页作业

主题：白俄罗斯首都明斯克的城市漫游指南（景点、美食、三日行程、实用贴士）。
实现：纯 Python 标准库，不依赖任何第三方包；内容写在脚本的数据区，
运行脚本即可生成完整的静态网页 `index.html`。

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `generate.py` | 唯一的源码：数据区（景点/美食/行程/贴士）+ 渲染函数 + HTML 模板 |
| `index.html` | 运行 `generate.py` 后生成的网页，浏览器直接打开即可查看 |
| `README.md` | 本说明，含发布步骤 |
| `keyword-report.md` | 关键词优化报告：两组关键词、选词依据、布置位置（课堂展示用） |
| `trends-short-tail.pdf` | Google Trends 短尾组对比截图（选词证据） |
| `trends-long-tail.pdf` | Google Trends 长尾组对比截图（选词证据） |

## 本地运行

```bash
python generate.py
```

运行后同目录会生成 `index.html`，双击用浏览器打开就能看。
想改内容（换个景点、改一句话）时，只改 `generate.py` 数据区的文字，
再运行一次脚本，页面就更新了。

## 关键词优化（2026-11-19 晚，按老师分享会要求做）

按老师清单的三步顺序执行：① 用 Google Trends 查热度 → ② 筛选两组关键词 →
③ 自然布置到网站上。完整过程和选词依据见 `keyword-report.md`，
工具截图在 `trends-short-tail.pdf` 和 `trends-long-tail.pdf`。

- 短尾组（1–2 个词）：Minsk（Trends 平均 61）、Belarus travel（4）、Minsk travel（1）、Minsk guide（1）
- 长尾组（3–5 个词）：best places in Minsk（4）、things to do in Minsk（3）、Minsk city guide（2）
- 筛掉的词（Trends 平均 0、无数据）：visit Minsk、Minsk travel guide、Minsk 3 day itinerary
- 布置位置：标题标签 + H1 + 页脚（Minsk city guide / Minsk guide）、H2 景点标题（best places in Minsk）、
  Meta 描述 + 景点导语（things to do in Minsk）、首段正文（Minsk travel / Belarus travel）
- 合规：每个词在可见内容中只出现 1–2 次，无堆砌、无隐藏文字

## 发布到 GitHub Pages（免费，不用敲命令行）

1. 打开 <https://github.com>，注册并登录账号（免费）。
2. 点右上角 `+` → `New repository`，仓库名填 `minsk-guide`，
   选 Public（公开），点 `Create repository`。
3. 空仓库没有 `Add file` 按钮：在页面中间深蓝色 `Quick setup` 框里点
   `uploading an existing file`，把文件夹里的 3 个网站文件
   （`index.html`、`generate.py`、`README.md`）
   一起拖进去，点 `Commit changes`。
   （`keyword-report.md` 和两张 Trends 截图是课堂展示材料，不用上传。）
   （传完之后仓库里有文件了，以后才会出现 `Add file` 按钮。）
   已有仓库要更新时：打开仓库点 `Add file` → `Upload files`，
   重新上传改过的文件即可。
4. 点仓库上方的 `Settings` → 左侧 `Pages`。
5. `Build and deployment` 下的 Source 选 `Deploy from a branch`，
   Branch 选 `main`，文件夹选 `/ (root)`，点 `Save`。
6. 等 1–2 分钟，刷新 Pages 页面，会看到一行绿色提示和你的网址：
   `https://chengxiangsun21-rgb.github.io/minsk-guide/`
   把这个链接交给老师就可以了。

## 备选免费平台

- **Netlify Drop**：打开 <https://app.netlify.com/drop>，
  把装有 `index.html` 的文件夹拖进去，立刻得到一个网址（需要注册账号）。
- **Vercel**：<https://vercel.com> 注册后导入项目或直接拖文件夹部署，
  同样免费，步骤和 Netlify 类似。

## 页面功能

- 响应式布局：电脑和手机打开都正常显示。
- 景点卡片带星标收藏按钮，点一下收藏，刷新页面后还在
  （用浏览器 localStorage 记住选择）。
- 单文件、无外部依赖：不加载任何外部图片或字体，离线也能完整显示。
