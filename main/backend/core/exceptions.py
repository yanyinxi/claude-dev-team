"""
自定义异常定义
"""
from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """资源不存在异常"""
    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id {resource_id} not found"
        )


class UnauthorizedException(HTTPException):
    """未授权异常"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )


class ForbiddenException(HTTPException):
    """禁止访问异常"""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


class ValidationException(HTTPException):
    """数据验证异常"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
