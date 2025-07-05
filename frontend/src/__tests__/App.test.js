import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'

describe('App', () => {
  it('renders properly', () => {
    const wrapper = mount(App)
    expect(wrapper.exists()).toBe(true)
  })

  it('contains navigation links', () => {
    const wrapper = mount(App)
    const links = wrapper.findAll('a')
    expect(links.length).toBeGreaterThan(0)
  })

  it('contains router-view', () => {
    const wrapper = mount(App)
    const routerView = wrapper.findComponent({ name: 'RouterView' })
    expect(routerView.exists()).toBe(true)
  })
}) 