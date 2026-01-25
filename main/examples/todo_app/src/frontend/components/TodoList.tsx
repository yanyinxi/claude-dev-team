import React from 'react';
import { Todo } from '../types';
import './TodoList.css';

interface TodoListProps {
  todos: Todo[];
  onUpdate: (id: number, updates: Partial<Todo>) => void;
  onDelete: (id: number) => void;
}

export const TodoList: React.FC<TodoListProps> = ({ todos, onUpdate, onDelete }) => {
  if (todos.length === 0) {
    return <div className="empty-state">暂无待办事项</div>;
  }

  return (
    <ul className="todo-list">
      {todos.map(todo => (
        <li key={todo.id} className={`todo-item ${todo.status}`}>
          <div className="todo-content">
            <h3>{todo.title}</h3>
            {todo.description && <p>{todo.description}</p>}
            {todo.dueDate && (
              <span className="due-date">
                截止日期: {new Date(todo.dueDate).toLocaleDateString()}
              </span>
            )}
          </div>
          
          <div className="todo-actions">
            <button
              className="complete-btn"
              onClick={() => onUpdate(todo.id, { 
                status: todo.status === 'completed' ? 'pending' : 'completed' 
              })}
            >
              {todo.status === 'completed' ? '标记为待办' : '标记为完成'}
            </button>
            
            <button
              className="delete-btn"
              onClick={() => {
                if (window.confirm('确定要删除这个待办事项吗？')) {
                  onDelete(todo.id);
                }
              }}
            >
              删除
            </button>
          </div>
        </li>
      ))}
    </ul>
  );
};
