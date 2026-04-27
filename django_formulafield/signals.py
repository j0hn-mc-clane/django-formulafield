
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_formulafield.formulas import evaluate_formula_with_context
from django_formulafield.models import FormulaRegistry, build_context
from django_formulafield.mixins import FormulaRegistryMixin


@receiver(post_save, sender=FormulaRegistry)
def reevaluate_on_registry_change(sender, instance, **kwargs):
    if not instance.reevaluate_on_update:
        return

    model_class = instance.content_type.model_class()
    if not issubclass(model_class, FormulaRegistryMixin):
        return

    if not hasattr(model_class, instance.att_name):
        raise AttributeError(
            f"{model_class.__name__} has no attribute '{instance.att_name}'. "
            f"Check FormulaRegistry entry for {instance}."
        )

    for obj in model_class.objects.all():
        context = build_context(obj)
        result = evaluate_formula_with_context(instance.formula, context)
        model_class.objects.filter(pk=obj.pk).update(**{instance.att_name: result})