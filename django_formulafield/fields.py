from django.db import models
import formulas


class EvaluatedFormulaField(models.CharField):
    description = "Stores the evaluated result of a formula stored in another field."

    def __init__(self, formula_field=None, max_length=255, reevaluate_on_update=False, *args, **kwargs):
        if not formula_field:
            raise ValueError(f"Expected a formula_field parameter in the definition")
        
        self.formula_field = formula_field
        self.reevaluate_on_update = reevaluate_on_update
        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("max_length", max_length)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["formula_field"] = self.formula_field
        kwargs["reevaluate_on_update"] = self.reevaluate_on_update
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        if add or self.reevaluate_on_update:
            return self.evaluate_and_store(model_instance)
        return getattr(model_instance, self.attname)

    def evaluate_and_store(self, model_instance):
        formula_source = getattr(model_instance, self.formula_field)
        
        if callable(formula_source):
            formula = formula_source()
        else:
            formula = formula_source

        print(formula)

        context = {
            field.name.upper(): getattr(model_instance, field.name)
            for field in model_instance._meta.get_fields()
            if hasattr(field, "column")
            and not field.is_relation
            and field.name is not None
        }

        if not formula.strip().startswith("="):
            formula = "=" + formula

        _, ast = formulas.Parser().ast(formula)
        compiled = ast.compile()
        needed = set(compiled.inputs.keys())
        result = str(compiled(**{k: v for k, v in context.items() if k in needed}))

        setattr(model_instance, self.attname, result)
        return result
