// API 配置
export const API_BASE_URL = 'https://mcjswtiujjjd.us-west-1.clawcloudrun.com'

// 根据环境设置不同的API地址
export const getApiUrl = endpoint => {
  return `${API_BASE_URL}${endpoint}`
}
