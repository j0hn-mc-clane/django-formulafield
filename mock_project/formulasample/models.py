"""Sales app models demonstrating EvaluatedFormulaField usage."""

from django.db import models
from django_formulafield.fields import EvaluatedFormulaField


class SalesPerformance(models.Model):
    """Tracks sales performance with formula-evaluated totals."""

    sold = models.IntegerField()
    cost_per_sale = models.FloatField()
    total_per_sale = models.FloatField()
    

    placeholder_1_formula = models.CharField(
        max_length=500,
        help_text="e.g. (sold * total_per_sale) - (sold * cost_per_sale)",
    )
    placeholder_1 = EvaluatedFormulaField(
        formula_field="placeholder_1_formula",
        reevaluate_on_update=True,
    )

    placeholder_2_formula = models.CharField(
        max_length=500,
        help_text="e.g. (sold * total_per_sale) - (sold * cost_per_sale)",
    )
    placeholder_2 = EvaluatedFormulaField(
        formula_field="placeholder_2_formula",
        reevaluate_on_update=True,
    )

    class Meta:
        verbose_name = "Sales Performance"
        verbose_name_plural = "Sales Performances"