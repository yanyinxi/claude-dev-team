/// <reference types="vitest" />

import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// =====================================================
// Vitest 配置 - 前端单元测试框架
// =====================================================
// 用途：Vue 3 + Vite 项目的原生测试解决方案
// 替代方案：Jest（需要额外配置转换器）
// =====================================================

export default defineConfig({
  // 加载 Vue 插件，支持 Vue 组件测试
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, '.')
    }
  },
  
  // 测试配置
  test: {
    // 使用 jsdom 模拟浏览器环境
    // 用途：无需真实浏览器即可运行组件测试
    environment: 'jsdom',
    
    // 全局 API 简化测试代码
    // 用途：每个测试文件自动可用 describe, it, expect, vi
    globals: true,
    
    // 包含的测试文件匹配模式
    include: [
      '**/*.test.{ts,js,vue}',
      '**/*.spec.{ts,js,vue}'
    ],
    
    // 覆盖率配置
    coverage: {
      // 覆盖率提供者：v8（Node.js 原生支持，速度快）
      provider: 'v8',
      
      // 覆盖率报告格式
      reporter: ['text', 'json', 'html'],
      
      // 覆盖率阈值（根据 CLAUDE.md 要求 > 80%）
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80
      },
      
      // 排除目录（不计算覆盖率）
      exclude: [
        'node_modules/',
        'dist/',
        '.git/',
        '**/*.d.ts',
        '**/*.config.{ts,js}'
      ]
    },
    
    // 依赖全局设置优化测试执行
    // 用途：提高测试执行速度
    deps: {
      inline: ['@vue', 'vue-router', 'pinia']
    }
  }
})
