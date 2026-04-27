"""Tests for EvaluatedFormulaField and FormulaRegistryMixin."""

import pytest
from django.contrib.contenttypes.models import ContentType
from django_formulafield.models import FormulaRegistry
from django_formulafield.tests.models import SalesPerformance


@pytest.mark.django_db
class TestEvaluatedFormulaField:
    """Tests for EvaluatedFormulaField behavior on create and update."""

    def test_arithmetic_formula_evaluates_on_create(self):
        """Basic arithmetic formula is evaluated when instance is created."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1_formula="(sold * total_per_sale) - (sold * cost_per_sale)",
        )
        assert performance.placeholder_1 == "500.0"

    def test_arithmetic_formula_with_equals_prefix(self):
        """Formula with explicit = prefix evaluates correctly."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1_formula="=(sold * total_per_sale) - (sold * cost_per_sale)",
        )
        assert performance.placeholder_1 == "500.0"

    def test_reevaluates_on_update_when_enabled(self):
        """Field with reevaluate_on_update=True recomputes on every save."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1_formula="(sold * total_per_sale) - (sold * cost_per_sale)",
        )
        assert performance.placeholder_1 == "500.0"

        performance.sold = 40
        performance.save()
        assert performance.placeholder_1 == "1000.0"

    def test_no_reevaluation_when_disabled(self):
        """Field with reevaluate_on_update=False keeps value from create."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1_formula="(sold * total_per_sale) - (sold * cost_per_sale)",
        )
        assert performance.placeholder_1_no_update == "500.0"

        performance.sold = 40
        performance.save()
        assert performance.placeholder_1_no_update == "500.0"

    def test_empty_formula_returns_none(self):
        """Empty formula field results in None rather than an error."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
        )
        assert performance.placeholder_1 is None

    def test_result_persisted_to_db(self):
        """Evaluated result is persisted and retrievable from the database."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1_formula="(sold * total_per_sale) - (sold * cost_per_sale)",
        )
        refreshed = SalesPerformance.objects.get(pk=performance.pk)
        assert refreshed.placeholder_1 == "500.0"


@pytest.mark.django_db
class TestIfFormula:
    """Tests for Excel-style IF formula support."""

    def test_if_returns_bad_when_condition_not_met(self):
        """IF formula returns false branch when condition is not met."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1_formula='IF(sold > 100, "good", "bad")',
        )
        assert performance.placeholder_1 == "bad"

    def test_if_returns_good_when_condition_met(self):
        """IF formula returns true branch when condition is met."""
        performance = SalesPerformance.objects.create(
            sold=200,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1_formula='IF(sold > 100, "good", "bad")',
        )
        assert performance.placeholder_1 == "good"

    def test_if_reevaluates_when_condition_changes(self):
        """IF formula result flips when data crosses the threshold on update."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1_formula='IF(sold > 100, "good", "bad")',
        )
        assert performance.placeholder_1 == "bad"

        performance.sold = 200
        performance.save()
        assert performance.placeholder_1 == "good"

    def test_if_with_numeric_branches(self):
        """IF formula works with numeric true/false branches."""
        performance = SalesPerformance.objects.create(
            sold=200,
            cost_per_sale=5.0,
            total_per_sale=30,
            placeholder_1_formula="IF(sold > 100, 1, 0)",
        )
        assert performance.placeholder_1 == "1"


@pytest.mark.django_db
class TestMethodFormula:
    """Tests for formula_field pointing to a model method."""

    def test_formula_from_method_evaluates_on_create(self):
        """formula_field pointing to a method uses the method's return value."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
        )
        assert performance.placeholder_2 == "20"

    def test_formula_from_method_not_reevaluated_on_update(self):
        """placeholder_2 has reevaluate_on_update=False — value locked after create."""
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
        )
        assert performance.placeholder_2 == "20"

        performance.sold = 99
        performance.save()
        assert performance.placeholder_2 == "20"


@pytest.mark.django_db
class TestFormulaRegistry:
    """Tests for FormulaRegistryMixin bulk re-evaluation via FormulaRegistry."""

    def _get_content_type(self):
        return ContentType.objects.get_for_model(SalesPerformance)

    def test_registry_formula_evaluates_on_instance_save(self):
        """Mixin evaluates registry formula into placeholder_3 on save."""
        FormulaRegistry.objects.create(
            content_type=self._get_content_type(),
            att_name="placeholder_3",
            formula="sold * total_per_sale",
            reevaluate_on_update=True,
        )
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
        )
        assert performance.placeholder_3 == "600.0"

    def test_registry_formula_bulk_reevaluates_on_registry_update(self):
        """Updating a FormulaRegistry entry re-evaluates all existing instances."""
        entry = FormulaRegistry.objects.create(
            content_type=self._get_content_type(),
            att_name="placeholder_3",
            formula="sold",
            reevaluate_on_update=True,
        )
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
        )
        assert performance.placeholder_3 == "20"

        entry.formula = "sold * 2"
        entry.save()

        performance.refresh_from_db()
        assert performance.placeholder_3 == "40.0"

    def test_multiple_registry_entries_evaluate_independently(self):
        """Two registry entries evaluate into placeholder_3 and placeholder_4 independently."""
        FormulaRegistry.objects.create(
            content_type=self._get_content_type(),
            att_name="placeholder_3",
            formula="sold",
            reevaluate_on_update=True,
        )
        FormulaRegistry.objects.create(
            content_type=self._get_content_type(),
            att_name="placeholder_4",
            formula="sold * total_per_sale",
            reevaluate_on_update=True,
        )
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
        )
        assert performance.placeholder_3 == "20"
        assert performance.placeholder_4 == "600.0"

    def test_registry_evaluates_on_create_regardless_of_reevaluate_flag(self):
        """Registry formula always evaluates on create even if reevaluate_on_update=False."""
        FormulaRegistry.objects.create(
            content_type=self._get_content_type(),
            att_name="placeholder_4",
            formula="sold",
            reevaluate_on_update=False,
        )
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
        )
        assert performance.placeholder_4 == "20"

    def test_registry_no_reevaluation_on_instance_update_when_disabled(self):
        """Registry entry with reevaluate_on_update=False keeps value after instance update."""
        FormulaRegistry.objects.create(
            content_type=self._get_content_type(),
            att_name="placeholder_4",
            formula="sold",
            reevaluate_on_update=False,
        )
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
        )
        assert performance.placeholder_4 == "20"

        performance.sold = 99
        performance.save()

        performance.refresh_from_db()
        assert performance.placeholder_4 == "20"  # unchanged

    def test_registry_no_bulk_reevaluation_when_disabled(self):
        """Updating a registry entry with reevaluate_on_update=False does not bulk re-evaluate."""
        entry = FormulaRegistry.objects.create(
            content_type=self._get_content_type(),
            att_name="placeholder_4",
            formula="sold",
            reevaluate_on_update=False,
        )
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
        )
        assert performance.placeholder_4 == "20"

        entry.formula = "sold * 2"
        entry.save()

        performance.refresh_from_db()
        assert performance.placeholder_4 == "20"

    def test_placeholder_3_reevaluates_on_instance_update(self):
        """placeholder_3 registry entry with reevaluate_on_update=True updates on instance save."""
        FormulaRegistry.objects.create(
            content_type=self._get_content_type(),
            att_name="placeholder_3",
            formula="sold",
            reevaluate_on_update=True,
        )
        performance = SalesPerformance.objects.create(
            sold=20,
            cost_per_sale=5.0,
            total_per_sale=30,
        )
        assert performance.placeholder_3 == "20"

        performance.sold = 99
        performance.save()

        performance.refresh_from_db()
        assert performance.placeholder_3 == "99"