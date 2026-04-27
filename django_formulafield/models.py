from django.contrib.contenttypes.models import ContentType
from django.db import models


class FormulaRegistry(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    att_name = models.CharField(max_length=255)
    formula = models.CharField(max_length=500)
    reevaluate_on_update = models.BooleanField(default=True)

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