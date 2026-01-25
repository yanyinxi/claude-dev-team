#!/usr/bin/env python3
"""
日志工具模块
Logging Utilities Module

功能：
1. 结构化日志记录
2. 支持多种日志级别
3. 上下文信息追踪
4. JSON 格式输出
5. 日志轮转
6. 函数装饰器
"""

import logging
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from functools import wraps
import traceback


class StructuredLogger:
    """结构化日志记录器"""

    def __init__(
        self,
        name: str,
        log_file: Optional[str] = None,
        level: int = logging.INFO,
        json_format: bool = False
    ):
        """
        初始化日志记录器

        Args:
            name: 日志记录器名称
            log_file: 日志文件路径
            level: 日志级别
            json_format: 是否使用 JSON 格式
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.json_format = json_format

        # 清除现有处理器
        self.logger.handlers.clear()

        # 添加控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(console_handler)

        # 添加文件处理器
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(self._get_formatter())
            self.logger.addHandler(file_handler)

    def _get_formatter(self) -> logging.Formatter:
        """获取日志格式化器"""
        if self.json_format:
            return JsonFormatter()
        else:
            return logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

    def _add_context(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """添加上下文信息到日志消息"""
        if not context:
            return message

        if self.json_format:
            return json.dumps({
                "message": message,
                "context": context,
                "timestamp": datetime.now().isoformat()
            })
        else:
            context_str = " | ".join(f"{k}={v}" for k, v in context.items())
            return f"{message} | {context_str}"

    def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        """记录 DEBUG 级别日志"""
        self.logger.debug(self._add_context(message, context))

    def info(self, message: str, context: Optional[Dict[str, Any]] = None):
        """记录 INFO 级别日志"""
        self.logger.info(self._add_context(message, context))

    def warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        """记录 WARNING 级别日志"""
        self.logger.warning(self._add_context(message, context))

    def error(self, message: str, context: Optional[Dict[str, Any]] = None, exc_info: bool = False):
        """记录 ERROR 级别日志"""
        self.logger.error(self._add_context(message, context), exc_info=exc_info)

    def critical(self, message: str, context: Optional[Dict[str, Any]] = None, exc_info: bool = False):
        """记录 CRITICAL 级别日志"""
        self.logger.critical(self._add_context(message, context), exc_info=exc_info)

    def exception(self, message: str, context: Optional[Dict[str, Any]] = None):
        """记录异常信息"""
        if context is None:
            context = {}
        context["traceback"] = traceback.format_exc()
        self.logger.error(self._add_context(message, context), exc_info=True)


class JsonFormatter(logging.Formatter):
    """JSON 格式化器"""

    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录为 JSON"""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        # 添加异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


class AuditLogger:
    """审计日志记录器"""

    def __init__(self, log_file: str = ".claude/autonomous/logs/audit.log"):
        """
        初始化审计日志记录器

        Args:
            log_file: 审计日志文件路径
        """
        self.logger = StructuredLogger(
            name="audit",
            log_file=log_file,
            level=logging.INFO,
            json_format=True
        )

    def log_event(
        self,
        event_type: str,
        description: str,
        user: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        记录审计事件

        Args:
            event_type: 事件类型
            description: 事件描述
            user: 触发用户
            metadata: 额外元数据
        """
        context = {
            "event_type": event_type,
            "user": user or "system",
            "metadata": metadata or {}
        }
        self.logger.info(description, context=context)

    def log_task_created(self, task_id: str, task_type: str, priority: int):
        """记录任务创建事件"""
        self.log_event(
            event_type="task_created",
            description=f"Task {task_id} created",
            metadata={"task_id": task_id, "task_type": task_type, "priority": priority}
        )

    def log_task_executed(self, task_id: str, status: str, duration: float):
        """记录任务执行事件"""
        self.log_event(
            event_type="task_executed",
            description=f"Task {task_id} executed with status {status}",
            metadata={"task_id": task_id, "status": status, "duration_seconds": duration}
        )

    def log_approval_required(self, task_id: str, reason: str):
        """记录需要审批事件"""
        self.log_event(
            event_type="approval_required",
            description=f"Task {task_id} requires approval",
            metadata={"task_id": task_id, "reason": reason}
        )

    def log_rollback_triggered(self, task_id: str, reason: str):
        """记录回滚触发事件"""
        self.log_event(
            event_type="rollback_triggered",
            description=f"Rollback triggered for task {task_id}",
            metadata={"task_id": task_id, "reason": reason}
        )


def log_function_call(logger: StructuredLogger):
    """
    函数调用日志装饰器

    Args:
        logger: 日志记录器实例

    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 记录函数调用
            logger.debug(
                f"Calling {func.__name__}",
                context={
                    "function": func.__name__,
                    "args": str(args)[:100],  # 限制长度
                    "kwargs": str(kwargs)[:100]
                }
            )

            try:
                # 执行函数
                result = func(*args, **kwargs)

                # 记录成功
                logger.debug(
                    f"Function {func.__name__} completed successfully",
                    context={"function": func.__name__}
                )

                return result

            except Exception as e:
                # 记录异常
                logger.exception(
                    f"Function {func.__name__} failed",
                    context={
                        "function": func.__name__,
                        "error": str(e)
                    }
                )
                raise

        return wrapper
    return decorator


def log_execution_time(logger: StructuredLogger):
    """
    执行时间日志装饰器

    Args:
        logger: 日志记录器实例

    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                logger.info(
                    f"Function {func.__name__} execution time",
                    context={
                        "function": func.__name__,
                        "duration_seconds": duration
                    }
                )

        return wrapper
    return decorator


# 全局日志记录器实例
_loggers: Dict[str, StructuredLogger] = {}


def get_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    json_format: bool = False
) -> StructuredLogger:
    """
    获取或创建日志记录器

    Args:
        name: 日志记录器名称
        log_file: 日志文件路径
        level: 日志级别
        json_format: 是否使用 JSON 格式

    Returns:
        StructuredLogger: 日志记录器实例
    """
    if name not in _loggers:
        _loggers[name] = StructuredLogger(
            name=name,
            log_file=log_file,
            level=level,
            json_format=json_format
        )
    return _loggers[name]


def main():
    """测试日志工具"""
    print("🧪 Testing Logging Utilities...")

    # 创建日志记录器
    logger = get_logger(
        name="test",
        log_file=".claude/autonomous/logs/test.log",
        level=logging.DEBUG
    )

    # 测试不同级别的日志
    logger.debug("This is a debug message")
    logger.info("This is an info message", context={"user": "test_user"})
    logger.warning("This is a warning message", context={"task_id": "task-123"})
    logger.error("This is an error message", context={"error_code": 500})

    # 测试异常日志
    try:
        raise ValueError("Test exception")
    except Exception:
        logger.exception("An exception occurred", context={"operation": "test"})

    # 测试审计日志
    audit_logger = AuditLogger()
    audit_logger.log_task_created("task-1", "time_based", 5)
    audit_logger.log_task_executed("task-1", "success", 1.5)

    # 测试装饰器
    @log_function_call(logger)
    @log_execution_time(logger)
    def test_function(x: int, y: int) -> int:
        """测试函数"""
        return x + y

    result = test_function(10, 20)
    print(f"\n✅ Test function result: {result}")

    print("\n✅ Logging utilities test completed!")


if __name__ == "__main__":
    main()
