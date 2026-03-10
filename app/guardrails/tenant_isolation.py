class TenantIsolationGuard:
    """Placeholder tenant isolation checks for future multi-tenant hardening."""

    @staticmethod
    def assert_tenant_access(tenant_id: str) -> None:
        if not tenant_id:
            raise ValueError("tenant_id is required")
        # Future: enforce tenant-level data partitioning and auth claims.
