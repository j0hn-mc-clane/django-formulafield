
from django.db import models
from django_formulafield.fields import EvaluatedFormulaField
from django_formulafield.mixins import FormulaRegistryMixin


class ProductCategoryChoices(models.TextChoices):
    """Available product categories."""

    SHOES = "shoes"
    ELECTRONICS = "electronics"


class SalesPerformance(FormulaRegistryMixin, models.Model):
    """Tracks sales performance with formula-evaluated totals."""

    sold = models.IntegerField()
    cost_per_sale = models.FloatField()
    total_per_sale = models.FloatField()
    product = models.CharField(max_length=255, null=True, blank=True)
    product_category = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=ProductCategoryChoices,
    )

    # Per-instance formulas via EvaluatedFormulaField
    placeholder_1_formula = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Per-instance formula. e.g. (sold * total_per_sale) - (sold * cost_per_sale)",
    )
    placeholder_1 = EvaluatedFormulaField(
        formula_field="placeholder_1_formula",
        reevaluate_on_update=True,
    )
    placeholder_2_formula = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Per-instance formula. e.g. IF(sold > 100, \"good\", \"bad\")",
    )
    placeholder_2 = EvaluatedFormulaField(
        formula_field="placeholder_2_formula",
        reevaluate_on_update=True,
    )

    # Shared formula results — written exclusively by FormulaRegistry
    registry_kpi_1 = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Managed by FormulaRegistry. Do not edit manually.",
    )
    registry_kpi_2 = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Managed by FormulaRegistry. Do not edit manually.",
    )

    class Meta:
        verbose_name = "Sales Performance"
        verbose_name_plural = "Sales Performances"

    def __str__(self):
        return f"{self.product or 'Unknown'} — sold: {self.sold}"