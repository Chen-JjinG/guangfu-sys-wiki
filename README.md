# 国华光伏建设管理系统 · 使用说明

这是一份 **纯静态** 使用说明网站：只有 HTML、CSS、JavaScript 和图片，打开即可阅读。发布时 **不需要** 安装 Node.js、npm，也不需要 VitePress 或其他构建步骤。

对外名称是 **国华光伏建设管理系统**。说明按当前演示环境可以完成的操作整理。

## 怎样挂出去

### GitHub Pages（推荐：从分支部署）

1. 把本仓库的文件推送到 `main` 分支（仓库根目录已是可发布的网页）。
2. 打开仓库 Settings → Pages。
3. Source 选择 **Deploy from a branch**。
4. Branch 选择 `main`，文件夹选择 `/ (root)`。
5. 保存后，网站地址为：<https://chen-jjing.github.io/guangfu-sys-wiki/>

不需要启用 GitHub Actions 来构建。第一次打开 Pages 后通常等待一两分钟即可访问。


若是从原先的 VitePress 仓库覆盖过来，请删掉不再需要的文件，避免误用旧的构建流程：

- `.github/workflows/deploy-docs.yml`（旧的 Actions 构建与部署）
- `package.json`、`package-lock.json`、`node_modules/`
- 旧的 `docs/`（VitePress 源）和已构建的 `site/`

本仓库发布时不依赖 GitHub Actions。Pages 只需「从分支部署」。


资源路径都是相对路径，也可以把整个仓库根目录复制到任意静态主机（ Nginx、对象存储、网盘网页），或在本机直接用浏览器打开 `index.html`。

### 本机预览

用任意静态文件服务在仓库根目录启动即可，例如：

```bash
python3 -m http.server 4173
```

然后打开 <http://127.0.0.1:4173/>。也可以直接双击 `index.html`（搜索在 `file://` 下也可使用）。

## 目录说明

| 路径 | 用途 |
| --- | --- |
| `index.html` 以及 `start/`、`owner/` 等目录中的 `.html` | 已生成、可直接发布的页面 |
| `assets/css/style.css`、`assets/js/` | 样式、侧栏与搜索脚本 |
| `images/` | 页面配图和标志 |
| `markdown/` | 正文的 Markdown 源文件，方便以后修改 |
| `scripts/build-static.py` | 可选：修改 Markdown 后，在本机用 Python 3 重新生成 HTML（标准库即可，不必安装依赖） |

修改说明后如果只改一两处，可以直接改对应 HTML。如果改了 `markdown/` 里的源文件，在仓库根目录执行：

```bash
python3 scripts/build-static.py
```

生成结果会写回仓库根目录的 HTML，仍然不必使用 npm。
