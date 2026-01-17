import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { TodoList } from '../../src/frontend/components/TodoList';

describe('TodoList 组件', () => {
  const mockOnUpdate = jest.fn();
  const mockOnDelete = jest.fn();
  
  const mockTodos = [
    {
      id: 1,
      title: '测试任务1',
      description: '测试描述1',
      status: 'pending',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    },
    {
      id: 2,
      title: '测试任务2',
      status: 'completed',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  ];

  beforeEach(() => {
    mockOnUpdate.mockClear();
    mockOnDelete.mockClear();
    jest.spyOn(window, 'confirm').mockReturnValue(true);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('应该正确渲染待办事项列表', () => {
    render(
      <TodoList
        todos={mockTodos}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('测试任务1')).toBeInTheDocument();
    expect(screen.getByText('测试任务2')).toBeInTheDocument();
  });

  it('应该在没有待办事项时显示空状态', () => {
    render(
      <TodoList
        todos={[]}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('暂无待办事项')).toBeInTheDocument();
  });

  it('点击完成按钮应该调用onUpdate', () => {
    render(
      <TodoList
        todos={[mockTodos[0]]}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const completeButton = screen.getByRole('button', { name: /标记为完成/i });
    fireEvent.click(completeButton);

    expect(mockOnUpdate).toHaveBeenCalledWith(1, { status: 'completed' });
  });

  it('点击删除按钮应该调用onDelete', () => {
    render(
      <TodoList
        todos={[mockTodos[0]]}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const deleteButton = screen.getByRole('button', { name: /删除/i });
    fireEvent.click(deleteButton);

    expect(mockOnDelete).toHaveBeenCalledWith(1);
  });

  it('已完成的任务应该有完成状态', () => {
    render(
      <TodoList
        todos={[mockTodos[1]]}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const todoItem = screen.getByText('测试任务2').closest('li');
    expect(todoItem).toHaveClass('completed');
  });

  it('应该显示截止日期', () => {
    const todoWithDueDate = {
      ...mockTodos[0],
      dueDate: '2025-12-31'
    };

    render(
      <TodoList
        todos={[todoWithDueDate]}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText(/截止日期/i)).toBeInTheDocument();
  });
});
