from django.db import models
from django_formulafield.fields import EvaluatedFormulaField


class SalesPerformance(models.Model):
    sold = models.IntegerField()
    total_per_sale = models.DecimalField()
    cost_per_sale = models.DecimalField()
    placeholder_1 = models.CharField(max_length=255)
    placeholder_1_eval = EvaluatedFormulaField(
        formula_field="placeholder_1",
        reevaluate_on_update=True,
    )
    placeholder_2 = models.CharField(max_length=255)
    placeholder_2_eval = EvaluatedFormulaField(
        formula_field="placeholder_2",
        reevaluate_on_update=False,
    )

    class Meta:
        app_label = "tests"
