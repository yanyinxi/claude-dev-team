const { expect } = require('chai');
const request = require('supertest');
const app = require('../src/backend/app');
const { initializeDB, execute } = require('../src/backend/models/database');

describe('Todo API 测试', () => {
  let createdTodoId;

  // 每个测试前初始化数据库并清理数据
  before(async () => {
    await initializeDB();
    try {
      await execute('DELETE FROM todos');
    } catch (error) {
      // 表可能不存在，忽略
    }
  });

  // 测试创建待办事项
  it('应该能够创建新的待办事项', async () => {
    const todo = {
      title: '测试待办事项',
      description: '这是一个测试',
    };

    const res = await request(app)
      .post('/api/todos')
      .send(todo)
      .expect(201);

    expect(res.body).to.have.property('id');
    expect(res.body.title).to.equal(todo.title);
    
    createdTodoId = res.body.id;
  });

  // 测试获取所有待办事项
  it('应该能够获取所有待办事项', async () => {
    const res = await request(app)
      .get('/api/todos')
      .expect(200);

    expect(res.body).to.be.an('array');
  });

  // 测试获取单个待办事项
  it('应该能够获取单个待办事项', async () => {
    // 先创建一个待办事项
    const createRes = await request(app)
      .post('/api/todos')
      .send({ title: '测试项' });
    
    const newId = createRes.body.id;

    const res = await request(app)
      .get(`/api/todos/${newId}`)
      .expect(200);

    expect(res.body.id).to.equal(newId);
  });

  // 测试更新待办事项
  it('应该能够更新待办事项', async () => {
    // 先创建一个待办事项
    const createRes = await request(app)
      .post('/api/todos')
      .send({ title: '原始标题' });
    
    const newId = createRes.body.id;

    const updates = {
      title: '更新后的标题',
      status: 'completed',
    };

    const res = await request(app)
      .put(`/api/todos/${newId}`)
      .send(updates)
      .expect(200);

    expect(res.body.title).to.equal(updates.title);
    expect(res.body.status).to.equal(updates.status);
  });

  // 测试删除待办事项
  it('应该能够删除待办事项', async () => {
    // 先创建一个待办事项
    const createRes = await request(app)
      .post('/api/todos')
      .send({ title: '待删除项' });
    
    const newId = createRes.body.id;

    await request(app)
      .delete(`/api/todos/${newId}`)
      .expect(204);

    // 验证已删除
    await request(app)
      .get(`/api/todos/${newId}`)
      .expect(404);
  });
});
