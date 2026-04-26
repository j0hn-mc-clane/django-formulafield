"""Admin configuration for the sales app."""

from django.contrib import admin
from .models import SalesPerformance


@admin.register(SalesPerformance)
class SalesPerformanceAdmin(admin.ModelAdmin):
    """Admin view for SalesPerformance with formula result displayed."""

    list_display = ("sold", "cost_per_sale", "total_per_sale")
    readonly_fields = ("placeholder_1","placeholder_2",)
    fieldsets = (
        ("Details", {
            "fields": ("sold", "cost_per_sale", "total_per_sale"),
        }),
        ("Placeholder Formulas", {
            "fields": ("placeholder_1_formula", "placeholder_1", "placeholder_2_formula", "placeholder_2"),
            "description": "Enter a formula using field names as variables.",
        }),
    )