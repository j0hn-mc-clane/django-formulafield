from django.contrib import admin
from django_formulafield.models import FormulaRegistry


@admin.register(FormulaRegistry)
class FormulaRegistryAdmin(admin.ModelAdmin):
    list_display = ("content_type", "att_name", "formula", "reevaluate_on_update")
    list_filter = ("content_type", "reevaluate_on_update")
    search_fields = ("att_name", "formula")
    fieldsets = (
        ("Target", {
            "fields": ("content_type", "att_name"),
            "description": "The model and field this formula writes to.",
        }),
        ("Formula", {
            "fields": ("formula", "reevaluate_on_update"),
            "description": (
                "Excel-style formula using model field names as variables. "
                "Example: (sold * total_per_sale) - (sold * cost_per_sale)"
            ),
        }),
    )