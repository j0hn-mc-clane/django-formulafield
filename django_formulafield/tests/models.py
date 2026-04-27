from django.db import models
from django_formulafield.fields import EvaluatedFormulaField
from django_formulafield.mixins import FormulaRegistryMixin

class SalesPerformance(FormulaRegistryMixin, models.Model):
    sold = models.IntegerField()
    total_per_sale = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_sale = models.DecimalField(max_digits=10, decimal_places=2)
    placeholder_1_formula = models.CharField(max_length=255, null=True)
    placeholder_1 = EvaluatedFormulaField(
        formula_field="placeholder_1_formula",
        reevaluate_on_update=True,
    )
    placeholder_1_no_update = EvaluatedFormulaField(
        formula_field="placeholder_1_formula",
        reevaluate_on_update=False,
    )
    placeholder_2 = EvaluatedFormulaField(
        formula_field="get_formula",
        reevaluate_on_update=False,
    )

    placeholder_3 = models.CharField(max_length=255, null=True)
    placeholder_4 = models.CharField(max_length=255, null=True)

    def get_formula(self):
        return "sold"
    
    class Meta:
        app_label = "tests"