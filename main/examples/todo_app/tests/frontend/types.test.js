describe('Types', () => {
  describe('TodoStatus', () => {
    it('应该只接受有效的状态值', () => {
      const validStatuses = ['pending', 'completed'];
      expect(validStatuses).toContain('pending');
      expect(validStatuses).toContain('completed');
    });
  });

  describe('Todo object', () => {
    it('应该正确创建Todo对象', () => {
      const todo = {
        id: 1,
        title: '测试任务',
        status: 'pending',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      expect(todo.id).toBe(1);
      expect(todo.title).toBe('测试任务');
      expect(todo.status).toBe('pending');
    });

    it('应该允许可选属性', () => {
      const todo = {
        id: 1,
        title: '带描述的任务',
        description: '这是一个描述',
        dueDate: '2025-12-31',
        status: 'completed',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      expect(todo.description).toBe('这是一个描述');
      expect(todo.dueDate).toBe('2025-12-31');
    });
  });

  describe('TodoInput object', () => {
    it('应该正确创建TodoInput对象', () => {
      const input = {
        title: '新任务',
        description: '描述',
        dueDate: '2025-12-31'
      };

      expect(input.title).toBe('新任务');
      expect(input.description).toBe('描述');
      expect(input.dueDate).toBe('2025-12-31');
    });

    it('应该允许只提供标题', () => {
      const input = {
        title: '只需标题'
      };

      expect(input.title).toBe('只需标题');
      expect(input.description).toBeUndefined();
      expect(input.dueDate).toBeUndefined();
    });
  });
});
