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
    placeholder_1_eval_no_update = EvaluatedFormulaField(
        formula_field="placeholder_1",
        reevaluate_on_update=False,
    )
    placeholder_2 = EvaluatedFormulaField(
        formula_field="get_formula",
        reevaluate_on_update=False,
    )

    def get_formula(self):
        return "sold"
    
    class Meta:
        app_label = "tests"
