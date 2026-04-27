"""Admin configuration for the sales app."""

from django.contrib import admin
from .models import SalesPerformance


@admin.register(SalesPerformance)
class SalesPerformanceAdmin(admin.ModelAdmin):
    """Admin view for SalesPerformance."""

    list_display = (
        "product",
        "product_category",
        "sold",
        "cost_per_sale",
        "total_per_sale",
        "placeholder_1",
        "placeholder_2",
        "registry_kpi_1",
        "registry_kpi_2",
    )
    readonly_fields = (
        "placeholder_1",
        "placeholder_2",
        "registry_kpi_1",
        "registry_kpi_2",
    )
    fieldsets = (
        ("Product", {
            "fields": ("product", "product_category"),
        }),
        ("Sales Data", {
            "fields": ("sold", "cost_per_sale", "total_per_sale"),
        }),
        ("Per-instance Formulas", {
            "fields": (
                "placeholder_1_formula", "placeholder_1",
                "placeholder_2_formula", "placeholder_2",
            ),
            "description": "Evaluated per instance — use field names as variables.",
        }),
        ("Registry KPIs", {
            "fields": ("registry_kpi_1", "registry_kpi_2"),
            "description": (
                "Read-only. Values are computed and written by FormulaRegistry entries. "
                "To change the formula, update the corresponding entry in the Formula Registry admin."
            ),
        }),
    )