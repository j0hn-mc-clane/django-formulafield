from django.contrib.contenttypes.models import ContentType
from django_formulafield.formulas import evaluate_formula_with_context


class FormulaRegistryMixin:
    def _evaluate_registry_formulas(self):
        from django_formulafield.models import FormulaRegistry, build_context

        content_type = ContentType.objects.get_for_model(self.__class__)
        entries = FormulaRegistry.objects.filter(content_type=content_type)
        if not self._state.adding:
            entries = entries.filter(reevaluate_on_update=True)

        for entry in entries:
            if not hasattr(self, entry.att_name):
                raise AttributeError(
                    f"{self.__class__.__name__} has no attribute '{entry.att_name}'. "
                    f"Check FormulaRegistry entry for {entry}."
                )
            setattr(
                self,
                entry.att_name,
                evaluate_formula_with_context(entry.formula, build_context(self)),
            )

    def save(self, *args, **kwargs):
        self._evaluate_registry_formulas()
        super().save(*args, **kwargs)
