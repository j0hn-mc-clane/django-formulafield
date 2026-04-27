
from django.contrib.contenttypes.models import ContentType
from django_formulafield.formulas import evaluate_formula_with_context
from django_formulafield.models import FormulaRegistry, build_context


class FormulaRegistryMixin:
    def _get_objects(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return FormulaRegistry.objects.filter(content_type=content_type)

    def _evaluate_registry_formulas(self, update=False):
        context = build_context(self)
        for entry in self._get_objects():
            if update and not entry.reevaluate_on_update:
                continue

            if not hasattr(self, entry.att_name):
                raise AttributeError(
                    f"{self.__class__.__name__} has no attribute '{entry.att_name}'. "
                    f"Check FormulaRegistry entry for {entry}."
                )

            result = evaluate_formula_with_context(entry.formula, context)
            setattr(self, entry.att_name, result)

    def save(self, *args, **kwargs):
        is_update = self.pk is not None and self.__class__.objects.filter(pk=self.pk).exists()
        self._evaluate_registry_formulas(update=is_update)
        super().save(*args, **kwargs)