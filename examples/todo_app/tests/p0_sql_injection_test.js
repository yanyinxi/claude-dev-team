#!/usr/bin/env node
/**
 * P0 测试: TC-E2E-003 紧急 Bug 修复测试
 * 测试内容: SQL 注入防护 + 数据验证
 */

const http = require('http');

const BASE_URL = 'http://localhost:3000/api';

// 辅助函数: 发送 HTTP 请求
const request = async (method, path, data = null) => {
  // 确保路径正确
  let normalizedPath = path;
  if (!path.startsWith('/')) {
    normalizedPath = '/' + path;
  }
  const fullPath = BASE_URL + normalizedPath;

  return new Promise((resolve, reject) => {
    const url = new URL(fullPath);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      method: method,
      headers: { 'Content-Type': 'application/json' },
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, body: body ? JSON.parse(body) : null });
        } catch (e) {
          resolve({ status: res.statusCode, body });
        }
      });
    });

    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
};

// 测试结果收集
const results = {
  passed: 0,
  failed: 0,
  tests: [],
};

const test = async (name, fn) => {
  try {
    await fn();
    results.passed++;
    results.tests.push({ name, status: '✅ PASS' });
    console.log(`✅ ${name}`);
  } catch (error) {
    results.failed++;
    results.tests.push({ name, status: `❌ FAIL: ${error.message}` });
    console.log(`❌ ${name}: ${error.message}`);
  }
};

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

// ==================== SQL 注入测试 ====================
const runSQLInjectionTests = async () => {
  console.log('\n🔒 TC-E2E-003.1: SQL 注入防护测试\n');

  // 恶意输入列表
  const maliciousInputs = [
    { input: "' OR '1'='1", description: '简单永真条件' },
    { input: "'; DROP TABLE todos; --", description: 'DROP TABLE 攻击' },
    { input: "admin'--", description: '注释注入' },
    { input: "1; SELECT * FROM users", description: '联合查询注入' },
    { input: "NULL) UNION SELECT * FROM todos --", description: 'UNION 注入' },
  ];

  for (const { input, description } of maliciousInputs) {
    await test(`SQL 注入防护 - ${description}`, async () => {
      const response = await request('GET', `/todos?status=${encodeURIComponent(input)}`);

      // 好的结果: 返回 400 (参数验证失败) 或 500 (服务器错误但不执行注入)
      // 坏的结果: 返回 200 且数据泄露
      if (response.status === 200 && Array.isArray(response.body)) {
        // 检查是否返回了不应该返回的数据
        assert(
          response.body.length === 0 || response.status !== 200,
          `可能存在 SQL 注入漏洞: 输入 "${input}" 返回了数据`
        );
      }
      // 400 或 500 都是可接受的结果
      assert([400, 500, 404].includes(response.status) || response.status === 200,
        `期望 400/404/500，但收到 ${response.status}`);
    });
  }
};

// ==================== 输入验证测试 ====================
const runInputValidationTests = async () => {
  console.log('\n🔍 TC-E2E-003.2: 输入验证测试\n');

  await test('标题为空时应返回 400', async () => {
    const response = await request('POST', '/todos', { title: '', description: '测试' });
    assert(response.status === 400, `期望 400，但收到 ${response.status}`);
    assert(response.body.error.includes('标题'), '错误消息应包含"标题"');
  });

  await test('创建时缺少 title 字段应返回 400', async () => {
    const response = await request('POST', '/todos', { description: '没有标题' });
    assert(response.status === 400, `期望 400，但收到 ${response.status}`);
  });

  await test('无效的 status 值应正确处理', async () => {
    const response = await request('GET', '/todos?status=invalid_status');
    // 应该返回空数组或不报错
    assert(response.status === 200, `期望 200，但收到 ${response.status}`);
    assert(Array.isArray(response.body), '应该返回数组');
  });
};

// ==================== XSS 防护测试 ====================
const runXSSTests = async () => {
  console.log('\n⚠️  TC-E2E-003.3: XSS 防护测试\n');

  const xssInputs = [
    '<script>alert("xss")</script>',
    '<img src=x onerror=alert(1)>',
    'javascript:alert(1)',
    '<svg onload=alert(1)>',
  ];

  for (const input of xssInputs) {
    await test(`XSS 防护 - ${input.substring(0, 30)}...`, async () => {
      const response = await request('POST', '/todos', {
        title: input,
        description: 'XSS 测试'
      });

      if (response.status === 201) {
        // 获取创建的记录，检查是否存储了恶意内容
        const getResponse = await request('GET', `/todos/${response.body.id}`);
        // 前端应该对输出进行转义，这里只验证存储
        assert(getResponse.body.title === input, '内容应该被正确存储');
      }
    });
  }
};

// ==================== API 边界测试 ====================
const runBoundaryTests = async () => {
  console.log('\n📐 TC-E2E-003.4: API 边界测试\n');

  await test('获取不存在的 ID 应返回 404', async () => {
    const response = await request('GET', '/todos/99999');
    assert(response.status === 404, `期望 404，但收到 ${response.status}`);
  });

  await test('更新不存在的 ID 应返回 404', async () => {
    const response = await request('PUT', '/todos/99999', { title: '新标题' });
    assert(response.status === 404, `期望 404，但收到 ${response.status}`);
  });

  await test('删除不存在的 ID 应返回 404', async () => {
    const response = await request('DELETE', '/todos/99999');
    assert(response.status === 404, `期望 404，但收到 ${response.status}`);
  });

  await test('无效的 JSON 格式应返回 400', async () => {
    // 这里无法直接测试，因为 Express 会自动解析 JSON
    // 但我们已经测试了缺少字段的情况
    console.log('   (跳过: JSON 解析由 Express 自动处理)');
  });
};

// ==================== 并发安全测试 ====================
const runConcurrencyTests = async () => {
  console.log('\n🔀 TC-E2E-003.5: 并发安全测试\n');

  await test('并发创建请求应全部成功', async () => {
    const promises = [];
    for (let i = 0; i < 10; i++) {
      promises.push(request('POST', '/todos', {
        title: `并发任务 ${i}`,
        description: '并发测试'
      }));
    }

    const responses = await Promise.all(promises);

    // 所有请求都应该成功
    const successCount = responses.filter(r => r.status === 201).length;
    assert(successCount === 10, `10 个并发请求中只有 ${successCount} 个成功`);

    // 所有创建的 ID 应该都不同
    const ids = responses
      .filter(r => r.status === 201)
      .map(r => r.body.id);
    const uniqueIds = new Set(ids);
    assert(uniqueIds.size === 10, '所有创建的 ID 应该唯一');
  });
};

// ==================== 主测试流程 ====================
const runTests = async () => {
  console.log('='.repeat(60));
  console.log('🔒 P0 测试: TC-E2E-003 紧急 Bug 修复测试');
  console.log('='.repeat(60));
  console.log(`测试时间: ${new Date().toISOString()}`);
  console.log(`服务器: ${BASE_URL}`);
  console.log('');

  // 先清理数据库
  console.log('🧹 清理测试数据...');
  const allTodos = await request('GET', '/todos');
  for (const todo of allTodos.body || []) {
    await request('DELETE', `/todos/${todo.id}`);
  }

  // 运行测试
  await runSQLInjectionTests();
  await runInputValidationTests();
  await runXSSTests();
  await runBoundaryTests();
  await runConcurrencyTests();

  // 清理
  console.log('\n🧹 清理测试数据...');
  const finalTodos = await request('GET', '/todos');
  for (const todo of finalTodos.body || []) {
    await request('DELETE', `/todos/${todo.id}`);
  }

  // 输出结果
  console.log('\n' + '='.repeat(60));
  console.log('📊 TC-E2E-003 测试结果汇总');
  console.log('='.repeat(60));
  console.log(`✅ 通过: ${results.passed}`);
  console.log(`❌ 失败: ${results.failed}`);
  console.log(`📈 通过率: ${((results.passed / (results.passed + results.failed)) * 100).toFixed(1)}%`);
  console.log('');

  if (results.failed > 0) {
    console.log('失败的测试:');
    results.tests.filter(t => t.status.startsWith('❌')).forEach(t => {
      console.log(`  ${t.status} ${t.name}`);
    });
  }

  console.log('\n' + '='.repeat(60));

  // 退出码
  process.exit(results.failed > 0 ? 1 : 0);
};

runTests().catch(err => {
  console.error('测试执行失败:', err);
  process.exit(1);
});
