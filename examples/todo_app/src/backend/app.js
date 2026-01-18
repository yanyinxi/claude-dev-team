const express = require('express');
const cors = require('cors');
const todoRoutes = require('./api/todos');

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(cors());
app.use(express.json());

// 路由
app.use('/api/todos', todoRoutes);

// 根路径
app.get('/', (req, res) => {
  res.json({ message: 'Todo List API', version: '1.0.0' });
});

// 错误处理中间件
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: '服务器内部错误' });
});

app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
});

module.exports = app;
