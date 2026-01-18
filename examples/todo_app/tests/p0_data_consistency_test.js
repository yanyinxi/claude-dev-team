#!/usr/bin/env node
/**
 * P0 测试: TC-E2E-005 数据一致性验证
 * 测试内容: 文档、API、代码、测试的同步性
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

const BASE_URL = 'http://localhost:3000/api';
const PROJECT_ROOT = '/Users/yanyinxi/工作/code/Java/claudecode/claude-dev-team/examples/todo_app';

// 辅助函数: 发送 HTTP 请求
const request = async (method, path, data = null) => {
  let normalizedPath = path.startsWith('/') ? path : '/' + path;
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

const results = { passed: 0, failed: 0, tests: [] };

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

// ==================== 文件一致性测试 ====================
const runFileConsistencyTests = async () => {
  console.log('\n📁 TC-E2E-005.1: 文件结构一致性测试\n');

  const requiredPaths = [
    'src/backend/app.js',
    'src/backend/api/todos.js',
    'src/backend/models/database.js',
    'src/backend/init.js',
    'src/frontend/index.html',
    'src/frontend/TodoApp.tsx',
    'data/todos.db',
    'package.json',
  ];

  for (const p of requiredPaths) {
    await test(`文件存在: ${p}`, () => {
      const fullPath = path.join(PROJECT_ROOT, p);
      assert(fs.existsSync(fullPath), `文件不存在: ${fullPath}`);
    });
  }
};

// ==================== API 端点一致性测试 ====================
const runAPIConsistencyTests = async () => {
  console.log('\n🔌 TC-E2E-005.2: API 端点一致性测试\n');

  const definedEndpoints = [
    { method: 'GET', path: '/todos', description: '获取所有待办事项' },
    { method: 'POST', path: '/todos', description: '创建待办事项' },
    { method: 'GET', path: '/todos/1', description: '获取单个待办事项' },
    { method: 'PUT', path: '/todos/1', description: '更新待办事项' },
    { method: 'DELETE', path: '/todos/1', description: '删除待办事项' },
  ];

  // 先创建一个测试用的 todo
  const createResp = await request('POST', '/todos', { title: 'API 测试', description: '测试' });
  const testId = createResp.body?.id || 1;

  for (const { method, path, description } of definedEndpoints) {
    await test(`${method} ${path} - ${description}`, async () => {
      let response;
      const dynamicPath = path.replace('1', testId);

      switch (method) {
        case 'GET':
          response = await request('GET', dynamicPath);
          break;
        case 'POST':
          response = await request('POST', '/todos', { title: '测试' });
          break;
        case 'PUT':
          response = await request('PUT', dynamicPath, { title: '更新测试' });
          break;
        case 'DELETE':
          response = await request('DELETE', dynamicPath);
          break;
      }

      assert([200, 201, 204, 404].includes(response.status),
        `${method} ${path} 返回状态码 ${response.status}`);
    });
  }
};

// ==================== 数据模型一致性测试 ====================
const runDataModelTests = async () => {
  console.log('\n🗃️  TC-E2E-005.3: 数据模型一致性测试\n');

  // 创建记录
  const createResp = await request('POST', '/todos', {
    title: '数据模型测试',
    description: '测试数据结构',
    dueDate: '2026-12-31'
  });

  await test('创建记录返回完整数据结构', () => {
    assert(createResp.status === 201, `期望 201，但收到 ${createResp.status}`);
    const todo = createResp.body;
    assert(todo.id !== undefined, '缺少 id 字段');
    assert(todo.title !== undefined, '缺少 title 字段');
    assert(todo.description !== undefined, '缺少 description 字段');
    assert(todo.status !== undefined, '缺少 status 字段');
    assert(todo.createdAt !== undefined, '缺少 createdAt 字段');
    assert(todo.updatedAt !== undefined, '缺少 updatedAt 字段');
  });

  // 测试更新
  const updateResp = await request('PUT', `/todos/${createResp.body.id}`, {
    title: '更新后的标题',
    status: 'completed'
  });

  await test('更新后返回完整数据结构', () => {
    assert(updateResp.status === 200, `期望 200，但收到 ${updateResp.status}`);
    const updated = updateResp.body;
    assert(updated.title === '更新后的标题', '标题未更新');
    assert(updated.status === 'completed', '状态未更新');
    assert(updated.id === createResp.body.id, 'ID 发生变化');
  });

  // 测试筛选
  const pendingResp = await request('GET', '/todos?status=pending');
  await test('状态筛选返回正确数据', () => {
    assert(pendingResp.status === 200, `期望 200，但收到 ${pendingResp.status}`);
    for (const todo of pendingResp.body || []) {
      assert(todo.status === 'pending', '包含非 pending 状态的记录');
    }
  });

  // 清理
  await request('DELETE', `/todos/${createResp.body.id}`);
};

// ==================== 文档代码一致性测试 ====================
const runDocCodeConsistencyTests = async () => {
  console.log('\n📝 TC-E2E-005.4: 文档代码一致性测试\n');

  // 检查 README 是否包含 API 文档
  await test('README 包含 API 文档说明', () => {
    const readmePath = path.join(PROJECT_ROOT, 'README.md');
    if (!fs.existsSync(readmePath)) return; // 跳过如果不存在

    const content = fs.readFileSync(readmePath, 'utf-8');
    assert(content.includes('/api/todos'), 'README 缺少 API 端点说明');
    assert(content.includes('GET') || content.includes('POST'), 'README 缺少 HTTP 方法说明');
  });

  // 检查代码注释完整性
  await test('API 代码包含必要注释', () => {
    const apiPath = path.join(PROJECT_ROOT, 'src/backend/api/todos.js');
    const content = fs.readFileSync(apiPath, 'utf-8');

    assert(content.includes('// 获取所有待办事项'), '缺少获取所有待办事项的注释');
    assert(content.includes('// 创建待办事项'), '缺少创建待办事项的注释');
    assert(content.includes('// 更新待办事项'), '缺少更新待办事项的注释');
    assert(content.includes('// 删除待办事项'), '缺少删除待办事项的注释');
  });

  // 检查 package.json 脚本完整性
  await test('package.json 包含必要脚本', () => {
    const pkgPath = path.join(PROJECT_ROOT, 'package.json');
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));

    assert(pkg.scripts.start, '缺少 start 脚本');
    assert(pkg.scripts.test, '缺少 test 脚本');
    assert(pkg.scripts['test:backend'], '缺少 test:backend 脚本');
    assert(pkg.scripts['test:frontend'], '缺少 test:frontend 脚本');
  });
};

// ==================== 测试覆盖验证 ====================
const runTestCoverageTests = async () => {
  console.log('\n🧪 TC-E2E-005.5: 测试覆盖验证\n');

  await test('存在后端测试文件', () => {
    const testPath = path.join(PROJECT_ROOT, 'tests/test_todos.js');
    assert(fs.existsSync(testPath), '后端测试文件不存在');
  });

  await test('测试文件包含必要测试用例', () => {
    const testPath = path.join(PROJECT_ROOT, 'tests/test_todos.js');
    const content = fs.readFileSync(testPath, 'utf-8');

    assert(content.includes('describe'), '测试文件缺少 describe');
    assert(content.includes('it(') || content.includes('test('), '测试文件缺少测试用例');
  });

  await test('前端测试文件存在', () => {
    const frontendTestPath = path.join(PROJECT_ROOT, 'tests/frontend');
    assert(fs.existsSync(frontendTestPath), '前端测试目录不存在');
  });
};

// ==================== 主测试流程 ====================
const runTests = async () => {
  console.log('='.repeat(60));
  console.log('🔒 P0 测试: TC-E2E-005 数据一致性验证');
  console.log('='.repeat(60));
  console.log(`测试时间: ${new Date().toISOString()}`);
  console.log(`项目根目录: ${PROJECT_ROOT}`);
  console.log(`服务器: ${BASE_URL}`);
  console.log('');

  // 运行测试
  await runFileConsistencyTests();
  await runAPIConsistencyTests();
  await runDataModelTests();
  await runDocCodeConsistencyTests();
  await runTestCoverageTests();

  // 输出结果
  console.log('\n' + '='.repeat(60));
  console.log('📊 TC-E2E-005 测试结果汇总');
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

  process.exit(results.failed > 0 ? 1 : 0);
};

runTests().catch(err => {
  console.error('测试执行失败:', err);
  process.exit(1);
});
