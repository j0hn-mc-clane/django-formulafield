""" Tests """

import pytest
from django_formulafield.tests.models import SalesPerformance


@pytest.mark.django_db
class TestFormulaField:
    def test_formula_evaluates_on_create(self):
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1="=(sold * total_per_sale) - (sold * cost_per_sale)",
        )

        assert performance.placeholder_1_eval == "500.0"
    

    def test_reevaluates_on_update_when_enabled(self):
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1="(sold * total_per_sale) - (sold * cost_per_sale)",
        )

        performance.sold = 40
        performance.save()

        assert performance.placeholder_1_eval == "1000.0"

    def test_no_reevaluation_when_disabled(self):
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1="(sold * total_per_sale) - (sold * cost_per_sale)",
        )

        performance.sold = 40
        performance.save()

        assert performance.placeholder_1_eval_no_update == "500.0"

    def test_if_formula_returns_bad(self):
        """IF formula returns 'bad' when sold is below threshold."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1='IF(sold > 100, "good", "bad")',
        )
        assert performance.placeholder_1_eval == "bad"
    
    
    def test_if_formula_returns_good(self):
        """IF formula returns 'good' when sold exceeds threshold."""
        performance = SalesPerformance.objects.create(
            sold=200,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1='IF(sold > 100, "good", "bad")',
        )
        assert performance.placeholder_1_eval == "good"
    
    
    def test_if_formula_reevaluates_on_update(self):
        """IF formula result updates when sold crosses the threshold."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1='IF(sold > 100, "good", "bad")',
        )
        assert performance.placeholder_1_eval == "bad"
    
        performance.sold = 200
        performance.save()
        assert performance.placeholder_1_eval == "good"

    def test_shared_model_formula(self):
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1="=(sold * total_per_sale) - (sold * cost_per_sale)",
        )

        assert performance.placeholder_2 == "20"