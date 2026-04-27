# Django Formula Field
When you want to provide placeholder columns for user to fill in based on values of the rows, you oftentimes want to have an Excel-like formula parser. This is the aim of this package, you provide a formula field and an evaluated result field.

## Installation

Installation through pip: `pip install django-formula-field`
## Getting Started

Defining an EvaluatedFormulaField is quite simple, you define a model:

```python
from django.db import models
from django_formulafield.fields import EvaluatedFormulaField

class SampleModel(models.Model):
    formula = models.CharField(max_length=255)
    result = EvaluatedFormulaField(formula_field="formula")  
```

Optional parameters are:
- max_length: behind the scenes, the evaluation is stored in a CharField
- reevaluate_on_update: if it should update the evaluation when you update the record

Formula field can be a callable function defined on the model.

## Evaluation
Evaluation is completely offloaded to the [formulas](https://pypi.org/project/formulas/) and any FormulaErrors are raised