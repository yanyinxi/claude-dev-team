const express = require('express');
const router = express.Router();
const { query, execute } = require('../models/database');

// 获取所有待办事项
router.get('/', async (req, res) => {
  try {
    const { status } = req.query;
    let sql = 'SELECT * FROM todos';
    const params = [];
    
    if (status) {
      sql += ' WHERE status = ?';
      params.push(status);
    }
    
    sql += ' ORDER BY createdAt DESC';
    
    const todos = await query(sql, params);
    res.json(todos);
  } catch (error) {
    console.error('获取待办事项失败:', error);
    res.status(500).json({ error: '获取待办事项失败' });
  }
});

// 获取单个待办事项
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const todos = await query('SELECT * FROM todos WHERE id = ?', [id]);
    
    if (todos.length === 0) {
      return res.status(404).json({ error: '待办事项不存在' });
    }
    
    res.json(todos[0]);
  } catch (error) {
    console.error('获取待办事项失败:', error);
    res.status(500).json({ error: '获取待办事项失败' });
  }
});

// 创建待办事项
router.post('/', async (req, res) => {
  try {
    const { title, description, dueDate } = req.body;
    
    if (!title) {
      return res.status(400).json({ error: '标题为必填项' });
    }
    
    const result = await execute(
      'INSERT INTO todos (title, description, dueDate) VALUES (?, ?, ?)',
      [title, description || null, dueDate || null]
    );
    
    const newTodo = await query('SELECT * FROM todos WHERE id = ?', [result.lastID]);
    res.status(201).json(newTodo[0]);
  } catch (error) {
    console.error('创建待办事项失败:', error);
    res.status(500).json({ error: '创建待办事项失败' });
  }
});

// 更新待办事项
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { title, description, dueDate, status } = req.body;
    
    // 先获取现有数据
    const todos = await query('SELECT * FROM todos WHERE id = ?', [id]);
    if (todos.length === 0) {
      return res.status(404).json({ error: '待办事项不存在' });
    }
    
    const existing = todos[0];
    
    // 使用现有值或新值
    const newTitle = title !== undefined ? title : existing.title;
    const newDescription = description !== undefined ? description : existing.description;
    const newDueDate = dueDate !== undefined ? dueDate : existing.dueDate;
    const newStatus = status !== undefined ? status : existing.status;
    
    await execute(
      'UPDATE todos SET title = ?, description = ?, dueDate = ?, status = ?, updatedAt = CURRENT_TIMESTAMP WHERE id = ?',
      [newTitle, newDescription, newDueDate, newStatus, id]
    );
    
    const updatedTodo = await query('SELECT * FROM todos WHERE id = ?', [id]);
    res.json(updatedTodo[0]);
  } catch (error) {
    console.error('更新待办事项失败:', error);
    res.status(500).json({ error: '更新待办事项失败' });
  }
});

// 删除待办事项
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    const todos = await query('SELECT * FROM todos WHERE id = ?', [id]);
    if (todos.length === 0) {
      return res.status(404).json({ error: '待办事项不存在' });
    }
    
    await execute('DELETE FROM todos WHERE id = ?', [id]);
    res.status(204).send();
  } catch (error) {
    console.error('删除待办事项失败:', error);
    res.status(500).json({ error: '删除待办事项失败' });
  }
});

module.exports = router;
