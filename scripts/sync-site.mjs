import { cp, mkdir, rm } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const dist = resolve(root, 'docs/.vitepress/dist')
const site = resolve(root, 'site')

await rm(site, { recursive: true, force: true })
await mkdir(site, { recursive: true })
await cp(dist, site, { recursive: true })
console.log(`已同步构建结果到 ${site}`)
