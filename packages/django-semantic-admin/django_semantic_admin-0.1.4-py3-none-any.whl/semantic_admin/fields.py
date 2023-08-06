from django import forms

from .widgets import SemanticSelect, SemanticSelectMultiple


# Single
class SemanticChoiceField(forms.ChoiceField):
    widget = SemanticSelect


class SemanticTypedChoiceField(forms.TypedChoiceField):
    widget = SemanticSelect


class SemanticModelChoiceField(forms.ModelChoiceField):
    widget = SemanticSelect


# Multiple
class SemanticMultipleChoiceField(forms.MultipleChoiceField):
    widget = SemanticSelectMultiple


class SemanticTypedMultipleChoiceField(forms.TypedMultipleChoiceField):
    widget = SemanticSelectMultiple


class SemanticModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    widget = SemanticSelectMultiple
