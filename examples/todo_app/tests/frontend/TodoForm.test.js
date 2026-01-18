import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { TodoForm } from '../../src/frontend/components/TodoForm';

describe('TodoForm 组件', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
    global.alert = jest.fn();
  });

  afterEach(() => {
    delete global.alert;
  });

  it('应该渲染表单输入框', () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    expect(screen.getByPlaceholderText('添加新的待办事项...')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('添加描述（可选）...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /添加/i })).toBeInTheDocument();
  });

  it('输入标题应该更新状态', () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByPlaceholderText('添加新的待办事项...');
    fireEvent.change(titleInput, { target: { value: '新任务' } });

    expect(titleInput).toHaveValue('新任务');
  });

  it('空标题提交应该显示alert', () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    const submitButton = screen.getByRole('button', { name: /添加/i });
    fireEvent.click(submitButton);

    expect(global.alert).toHaveBeenCalledWith('请输入标题');
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('正确提交应该调用onSubmit并清空表单', () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByPlaceholderText('添加新的待办事项...');
    fireEvent.change(titleInput, { target: { value: '测试任务' } });

    const descriptionInput = screen.getByPlaceholderText('添加描述（可选）...');
    fireEvent.change(descriptionInput, { target: { value: '测试描述' } });

    const submitButton = screen.getByRole('button', { name: /添加/i });
    fireEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
    expect(titleInput).toHaveValue('');
  });

  it('只输入空格不应该提交', () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByPlaceholderText('添加新的待办事项...');
    fireEvent.change(titleInput, { target: { value: '   ' } });

    const submitButton = screen.getByRole('button', { name: /添加/i });
    fireEvent.click(submitButton);

    expect(global.alert).toHaveBeenCalledWith('请输入标题');
  });
});
