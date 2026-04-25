"""Tests for RBAC module."""

from app.core.rbac import check_permission, Role


def test_admin_has_all_permissions():
    assert check_permission("ADMIN", "create_operation") is True
    assert check_permission("ADMIN", "read_audit_logs") is True
    assert check_permission("ADMIN", "manage_users") is True
    assert check_permission("ADMIN", "purge_data") is True


def test_operador_permissions():
    assert check_permission("OPERADOR", "create_operation") is True
    assert check_permission("OPERADOR", "upload_evidence") is True
    assert check_permission("OPERADOR", "generate_report") is True
    assert check_permission("OPERADOR", "read_audit_logs") is False
    assert check_permission("OPERADOR", "manage_users") is False
    assert check_permission("OPERADOR", "approve_report") is False


def test_comercial_permissions():
    assert check_permission("COMERCIAL", "read_operation") is True
    assert check_permission("COMERCIAL", "download_report") is True
    assert check_permission("COMERCIAL", "create_operation") is False
    assert check_permission("COMERCIAL", "upload_evidence") is False
    assert check_permission("COMERCIAL", "read_audit_logs") is False


def test_supervisor_permissions():
    assert check_permission("SUPERVISOR", "approve_report") is True
    assert check_permission("SUPERVISOR", "generate_report") is True
    assert check_permission("SUPERVISOR", "read_audit_logs") is False
    assert check_permission("SUPERVISOR", "manage_users") is False
