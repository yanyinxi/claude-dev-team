const express = require('express');
const path = require('path');
const cors = require('cors');
const todoRoutes = require('./api/todos');

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(cors());
app.use(express.json());

// 请求日志中间件
app.use((req, res, next) => {
  const timestamp = new Date().toLocaleTimeString('zh-CN');
  console.log(`\n[${timestamp}] ${req.method} ${req.path}`);
  if (Object.keys(req.body).length > 0) {
    console.log('  请求体:', req.body);
  }
  if (Object.keys(req.query).length > 0) {
    console.log('  查询参数:', req.query);
  }
  next();
});

// 提供静态文件（前端应用）
app.use(express.static(path.join(__dirname, '../frontend')));

// 路由
app.use('/api/todos', todoRoutes);

// 根路径 - 提供 index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// 错误处理中间件
app.use((err, req, res, next) => {
  console.error('❌ 服务器错误:', err.stack);
  res.status(500).json({ error: '服务器内部错误' });
});

app.listen(PORT, () => {
  console.log(`\n🚀 服务器运行在 http://localhost:${PORT}`);
  console.log('📝 开始监听请求日志...\n');
});

module.exports = app;
