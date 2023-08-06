from django_filters.filters import (
    AllValuesMultipleFilter,
    ChoiceFilter,
    Filter,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
    MultipleChoiceFilter,
    TypedMultipleChoiceFilter,
)
from semantic_admin.fields import (
    SemanticChoiceField,
    SemanticModelChoiceField,
    SemanticModelMultipleChoiceField,
    SemanticMultipleChoiceField,
    SemanticTypedChoiceField,
    SemanticTypedMultipleChoiceField,
)


class FilterOrExcludeMixin(Filter):
    def get_method(self, qs):
        """Return filter method based on whether we're excluding or simply filtering"""
        return qs.exclude if self.exclude else qs.filter


class SemanticChoiceFilter(FilterOrExcludeMixin, ChoiceFilter):
    field_class = SemanticChoiceField


class SemanticMultipleChoiceFilter(FilterOrExcludeMixin, MultipleChoiceFilter):
    field_class = SemanticMultipleChoiceField


class SemanticTypedChoiceFilter(FilterOrExcludeMixin, TypedMultipleChoiceFilter):
    field_class = SemanticTypedChoiceField


class SemanticTypedMultipleChoiceFilter(
    FilterOrExcludeMixin, TypedMultipleChoiceFilter
):
    field_class = SemanticTypedMultipleChoiceField


class SemanticMultipleAllValuesFilter(FilterOrExcludeMixin, AllValuesMultipleFilter):
    # TODO
    pass


class SemanticModelChoiceFilter(FilterOrExcludeMixin, ModelChoiceFilter):
    field_class = SemanticModelChoiceField


class SemanticModelMultipleChoiceFilter(
    FilterOrExcludeMixin, ModelMultipleChoiceFilter
):
    field_class = SemanticModelMultipleChoiceField
