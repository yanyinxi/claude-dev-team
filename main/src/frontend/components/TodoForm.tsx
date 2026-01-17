import React, { useState } from 'react';
import { TodoInput } from '../types';
import './TodoForm.css';

interface TodoFormProps {
  onSubmit: (todo: TodoInput) => void;
}

export const TodoForm: React.FC<TodoFormProps> = ({ onSubmit }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title.trim()) {
      alert('请输入标题');
      return;
    }

    onSubmit({
      title: title.trim(),
      description: description.trim() || undefined,
      dueDate: dueDate ? new Date(dueDate).toISOString() : undefined,
    });

    // 重置表单
    setTitle('');
    setDescription('');
    setDueDate('');
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="添加新的待办事项..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="title-input"
      />
      
      <textarea
        placeholder="添加描述（可选）..."
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        className="description-input"
      />
      
      <input
        type="date"
        value={dueDate}
        onChange={(e) => setDueDate(e.target.value)}
        className="due-date-input"
      />
      
      <button type="submit" className="submit-btn">
        添加
      </button>
    </form>
  );
};
