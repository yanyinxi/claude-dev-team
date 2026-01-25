export type TodoStatus = 'pending' | 'completed';

export interface Todo {
  id: number;
  title: string;
  description?: string;
  dueDate?: string;
  status: TodoStatus;
  createdAt: string;
  updatedAt: string;
}

export interface TodoInput {
  title: string;
  description?: string;
  dueDate?: string;
}
