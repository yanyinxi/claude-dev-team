import React, { useState, useEffect } from 'react';
import { TodoList } from './components/TodoList';
import { TodoForm } from './components/TodoForm';
import { Todo, TodoStatus } from '../types';
import './styles/TodoApp.css';

const API_URL = 'http://localhost:3000/api';

export const TodoApp: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<TodoStatus | 'all'>('all');

  // 获取所有待办事项
  const fetchTodos = async () => {
    try {
      const response = await fetch(`${API_URL}/todos`);
      const data = await response.json();
      setTodos(data);
    } catch (error) {
      console.error('获取待办事项失败:', error);
    }
  };

  // 初始加载
  useEffect(() => {
    fetchTodos();
  }, []);

  // 创建待办事项
  const handleCreateTodo = async (todo: Omit<Todo, 'id' | 'status' | 'createdAt' | 'updatedAt'>) => {
    try {
      const response = await fetch(`${API_URL}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(todo),
      });
      const newTodo = await response.json();
      setTodos([...todos, newTodo]);
    } catch (error) {
      console.error('创建待办事项失败:', error);
    }
  };

  // 更新待办事项
  const handleUpdateTodo = async (id: number, updates: Partial<Todo>) => {
    try {
      const response = await fetch(`${API_URL}/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
      });
      const updatedTodo = await response.json();
      setTodos(todos.map(todo => todo.id === id ? updatedTodo : todo));
    } catch (error) {
      console.error('更新待办事项失败:', error);
    }
  };

  // 删除待办事项
  const handleDeleteTodo = async (id: number) => {
    try {
      await fetch(`${API_URL}/todos/${id}`, { method: 'DELETE' });
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (error) {
      console.error('删除待办事项失败:', error);
    }
  };

  // 筛选待办事项
  const filteredTodos = todos.filter(todo => {
    if (filter === 'all') return true;
    return todo.status === filter;
  });

  return (
    <div className="todo-app">
      <h1>Todo List</h1>
      
      <TodoForm onSubmit={handleCreateTodo} />
      
      <div className="filter-section">
        <button onClick={() => setFilter('all')}>全部</button>
        <button onClick={() => setFilter('pending')}>待办</button>
        <button onClick={() => setFilter('completed')}>已完成</button>
      </div>
      
      <TodoList
        todos={filteredTodos}
        onUpdate={handleUpdateTodo}
        onDelete={handleDeleteTodo}
      />
    </div>
  );
};
