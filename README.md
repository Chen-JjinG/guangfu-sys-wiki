# 国华光伏建设管理系统 · 使用说明

这是一份可维护的静态文档站，用 VitePress 编写，风格接近常见的左侧可展收目录文档（顶栏、左侧分组目录、右侧本页目录、站内搜索、上一页 / 下一页）。内容按当前演示环境可以完成的操作整理，对外名称是 **国华光伏建设管理系统**。

在线演示系统（业务系统，不是本说明站）：

- 电脑端：<http://47.111.226.121/>
- 现场端：<http://47.111.226.121/h5/>

本仓库用于把使用说明挂出来给客户阅读。不要把服务器、数据库或其他基础设施的密码写进文档。

## 目录说明

| 路径 | 用途 |
| --- | --- |
| `docs/` | Markdown 正文和 VitePress 配置 |
| `docs/.vitepress/config.mts` | 站点标题、侧栏、搜索、base |
| `docs/images/` | 正文配图（来自当前演示环境，已核对外名称） |
| `docs/public/` | 站点图标等静态资源 |
| `site/` | 本地构建后可直接打开或部署的静态文件副本（不要只把产出留在 `dist` 里） |
| `.github/workflows/deploy-docs.yml` | GitHub Pages 自动构建与发布 |

## 怎样修改内容

1. 在 `docs/` 下编辑或新增 `.md` 文件。侧栏分组在 `docs/.vitepress/config.mts` 的 `themeConfig.sidebar` 里维护。
2. 配图放到 `docs/images/`，在 Markdown 里用相对路径引用，例如 `![说明](../images/h5-home.png)`。
3. 每一页尽量写清：这个模块干什么、谁来用、从哪里进入、怎样一步步操作、列表上有哪些状态和按钮、提交之后会发生什么、使用时要注意什么。
4. 只写当前系统能用的操作。不要把尚未开放的能力写成已经开通。
5. 正文不要出现已停用的旧品牌名称。地名「余杭」「余姚」可以保留。

## 本地预览

需要已安装 Node.js（建议 20 或更高版本）。

```bash
cd guohua-pv-user-guide
npm install
npm run docs:dev
```

浏览器打开终端里提示的地址（默认是 <http://127.0.0.1:5173/guangfu-sys-wiki/>）。默认 base 是 `/guangfu-sys-wiki/`，与 GitHub Pages 项目站路径一致。

若希望在站点根路径预览，可以执行：

```bash
DOCS_BASE=/ npm run docs:dev
```

## 构建，并同步到 site/

发布到 GitHub Pages 时使用默认 base `/guangfu-sys-wiki/`：

```bash
npm run docs:build
```

构建结果在 `docs/.vitepress/dist/`。请再同步一份到仓库根目录的 `site/`，避免盒子重置时只丢掉名为 `dist` 的目录：

```bash
npm run site
```

`npm run site` 默认同样使用 `/guangfu-sys-wiki/`。如果要得到一套可用相对路径打开的静态文件（例如以后挂到别的目录），请执行：

```bash
DOCS_BASE=./ npm run site
```

然后可用任意静态服务器打开 `site/`，例如：

```bash
npx --yes serve site -p 4173
```

## GitHub Pages

仓库发布地址预定为：<https://chen-jjing.github.io/guangfu-sys-wiki/>

在仓库设置里把 GitHub Pages 的 Source 选为 **GitHub Actions**。推送到 `main` 后，工作流 `.github/workflows/deploy-docs.yml` 会安装依赖、构建并发布。首次启用 Pages 后，如未自动挂出，请在仓库的 Settings → Pages 中确认已授权该工作流。

## 演示账号

登录租户名称填写 **国华光伏建设管理系统**。账号和密码写在「总体说明」和「演示账号」两页，来自演示环境种子数据。**那些密码是演示环境种子密码，正式环境请更改。**
