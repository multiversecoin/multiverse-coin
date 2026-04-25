"""Role-Based Access Control (RBAC) — roles and permission checks."""

from enum import Enum
from functools import wraps
from typing import Callable, List

from fastapi import HTTPException, status


class Role(str, Enum):
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    OPERADOR = "OPERADOR"
    COMERCIAL = "COMERCIAL"


ROLE_HIERARCHY = {
    Role.ADMIN: 4,
    Role.SUPERVISOR: 3,
    Role.OPERADOR: 2,
    Role.COMERCIAL: 1,
}

PERMISSIONS = {
    "create_operation": [Role.ADMIN, Role.SUPERVISOR, Role.OPERADOR],
    "read_operation": [Role.ADMIN, Role.SUPERVISOR, Role.OPERADOR, Role.COMERCIAL],
    "update_operation": [Role.ADMIN, Role.SUPERVISOR, Role.OPERADOR],
    "upload_evidence": [Role.ADMIN, Role.SUPERVISOR, Role.OPERADOR],
    "read_evidence": [Role.ADMIN, Role.SUPERVISOR, Role.OPERADOR],
    "download_evidence": [Role.ADMIN, Role.SUPERVISOR, Role.OPERADOR],
    "generate_report": [Role.ADMIN, Role.SUPERVISOR, Role.OPERADOR],
    "approve_report": [Role.ADMIN, Role.SUPERVISOR],
    "download_report": [Role.ADMIN, Role.SUPERVISOR, Role.OPERADOR, Role.COMERCIAL],
    "read_audit_logs": [Role.ADMIN],
    "manage_users": [Role.ADMIN],
    "purge_data": [Role.ADMIN],
    "register_incident": [Role.ADMIN, Role.SUPERVISOR],
}


def check_permission(user_role: str, permission: str) -> bool:
    allowed_roles = PERMISSIONS.get(permission, [])
    return user_role in [r.value for r in allowed_roles]


def require_permission(permission: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if current_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuário não autenticado",
                )
            if not check_permission(current_user.role, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permissão negada: {permission}",
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_roles(allowed_roles: List[Role]):
    def checker(user_role: str):
        if user_role not in [r.value for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado para este perfil",
            )
    return checker
