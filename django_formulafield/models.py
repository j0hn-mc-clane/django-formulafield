from django.contrib.contenttypes.models import ContentType
from django.db import models

from django_formulafield.formulas import evaluate_formula_with_context
from django_formulafield.mixins import FormulaRegistryMixin


class FormulaRegistry(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    att_name = models.CharField(max_length=255)
    formula = models.CharField(max_length=500)
    reevaluate_on_update = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.reevaluate_on_update:
            self.reevaluate_all()

    def reevaluate_all(self):
        model_class = self.content_type.model_class()
        if not issubclass(model_class, FormulaRegistryMixin):
            return

        if not hasattr(model_class, self.att_name):
            raise AttributeError(
                f"{model_class.__name__} has no attribute '{self.att_name}'. "
                f"Check FormulaRegistry entry for {self}."
            )

        field_names = [
            f.name
            for f in model_class._meta.get_fields()
            if hasattr(f, "column") and not f.is_relation
        ]
        objects = list(model_class.objects.only(*field_names, "pk"))

        for obj in objects:
            setattr(
                obj,
                self.att_name,
                evaluate_formula_with_context(self.formula, build_context(obj)),
            )

        model_class.objects.bulk_update(objects, [self.att_name], batch_size=500)

    class Meta:
        unique_together = ("content_type", "att_name")
        verbose_name = "Formula Registry"
        verbose_name_plural = "Formula Registries"

    def __str__(self):
        return f"{self.content_type.model}.{self.att_name} = {self.formula}"


def build_context(instance) -> dict:
    return {
        field.name.upper(): getattr(instance, field.name)
        for field in instance._meta.get_fields()
        if hasattr(field, "column")
        and not field.is_relation
        and field.name is not None
        and getattr(instance, field.name) is not None  # exclude None values
    }
