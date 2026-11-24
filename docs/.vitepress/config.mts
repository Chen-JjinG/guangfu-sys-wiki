import { defineConfig } from 'vitepress'

const base = process.env.DOCS_BASE || '/guangfu-sys-wiki/'

export default defineConfig({
  lang: 'zh-CN',
  title: '国华光伏建设管理系统',
  description: '国华光伏建设管理系统使用说明：电脑端与现场端各模块的操作指南',
  base,
  srcDir: '.',
  ignoreDeadLinks: true,
  lastUpdated: false,
  cleanUrls: false,
  head: [
    ['link', { rel: 'icon', href: `${base}logo.svg`.replace('//', '/') }],
    ['meta', { name: 'theme-color', content: '#c45c26' }]
  ],
  markdown: {
    container: {
      tipLabel: '说明',
      warningLabel: '注意',
      infoLabel: '提示',
      dangerLabel: '警告'
    }
  },
  themeConfig: {
    logo: '/logo.svg',
    siteTitle: '国华光伏 使用说明',
    outline: {
      label: '本页目录',
      level: [2, 3]
    },
    nav: [
      { text: '总体说明', link: '/start/overview.html' },
      { text: '演示账号', link: '/appendix/accounts.html' },
      { text: '登录与两端', link: '/start/login.html' },
      { text: '安装施工', link: '/install/dispatch.html' },
      { text: '附录', link: '/appendix/tips.html' }
    ],
    sidebar: [
      {
        text: '开始',
        collapsed: false,
        items: [
          { text: '总体说明', link: '/start/overview.html' },
          { text: '快速上手', link: '/start/quick-start.html' },
          { text: '登录与两端', link: '/start/login.html' },
          { text: '角色与权限', link: '/start/roles.html' }
        ]
      },
      {
        text: '业主与商机',
        collapsed: false,
        items: [
          { text: '业主管理', link: '/owner/owner.html' },
          { text: '商机初勘', link: '/owner/opportunity.html' }
        ]
      },
      {
        text: '勘察与签约',
        collapsed: true,
        items: [
          { text: '电站勘察', link: '/survey/survey.html' },
          { text: '业主补贴', link: '/survey/subsidy.html' },
          { text: '合同签约', link: '/survey/contract.html' },
          { text: '备案登记', link: '/survey/filing.html' }
        ]
      },
      {
        text: '设计与开工准备',
        collapsed: true,
        items: [
          { text: '电站设计', link: '/design/design.html' },
          { text: '电站建档', link: '/design/archive.html' },
          { text: '电站备货', link: '/design/stock.html' }
        ]
      },
      {
        text: '安装施工',
        collapsed: true,
        items: [
          { text: '派工与安全打卡', link: '/install/dispatch.html' },
          { text: '工程领料', link: '/install/pick.html' },
          { text: '施工复核', link: '/install/review.html' },
          { text: '支架报装', link: '/install/bracket.html' },
          { text: '电气报装', link: '/install/electric.html' },
          { text: '电表安装', link: '/install/meter.html' },
          { text: '完工自检', link: '/install/selfcheck.html' }
        ]
      },
      {
        text: '产权与消缺',
        collapsed: true,
        items: [
          { text: '产权证明', link: '/property/property.html' },
          { text: '消缺工单', link: '/property/defect.html' }
        ]
      },
      {
        text: '审核与工单',
        collapsed: true,
        items: [
          { text: '审核中心', link: '/audit/audit.html' },
          { text: '工单中心', link: '/audit/workorder.html' }
        ]
      },
      {
        text: '系统设置',
        collapsed: true,
        items: [
          { text: '审批设置', link: '/settings/approval.html' },
          { text: '现场端品牌', link: '/settings/brand.html' },
          { text: '组织与安装队', link: '/settings/org.html' }
        ]
      },
      {
        text: '附录',
        collapsed: true,
        items: [
          { text: '常见提示', link: '/appendix/tips.html' },
          { text: '演示账号', link: '/appendix/accounts.html' },
          { text: '当前未开放的能力', link: '/appendix/not-open.html' },
          { text: '电站查询（简要）', link: '/appendix/station.html' }
        ]
      }
    ],
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索' },
          modal: {
            displayDetails: '显示详细列表',
            resetButtonTitle: '清除查询',
            backButtonTitle: '关闭搜索',
            noResultsText: '没有找到结果',
            footer: {
              selectText: '选择',
              selectKeyAriaLabel: '回车',
              navigateText: '切换',
              navigateUpKeyAriaLabel: '上箭头',
              navigateDownKeyAriaLabel: '下箭头',
              closeText: '关闭',
              closeKeyAriaLabel: 'Esc'
            }
          }
        }
      }
    },
    docFooter: { prev: '上一页', next: '下一页' },
    darkModeSwitchLabel: '外观',
    lightModeSwitchTitle: '切换到浅色',
    darkModeSwitchTitle: '切换到深色',
    sidebarMenuLabel: '目录',
    returnToTopLabel: '回到顶部',
    footer: {
      message: '国华光伏建设管理系统 · 使用说明（按当前演示环境整理）',
      copyright: '操作以线上实际界面为准'
    }
  }
})
