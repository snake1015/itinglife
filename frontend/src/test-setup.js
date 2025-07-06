// 测试环境设置
import { vi } from 'vitest'

// 模拟Vue Router
vi.mock('vue-router', () => ({
  createRouter: vi.fn(() => ({
    push: vi.fn(),
    replace: vi.fn(),
    go: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
  })),
  createWebHistory: vi.fn(),
  createWebHashHistory: vi.fn(),
  createMemoryHistory: vi.fn(),
}))

// 模拟window对象
global.window = global.window || {}

// 模拟localStorage
global.localStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}

// 模拟sessionStorage
global.sessionStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}

// 处理console错误
const originalError = console.error
console.error = (...args) => {
  if (
    typeof args[0] === 'string' &&
    args[0].includes('Warning: ReactDOM.render is deprecated')
  ) {
    return
  }
  originalError.call(console, ...args)
}
