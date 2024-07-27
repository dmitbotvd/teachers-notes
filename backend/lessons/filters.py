import django_filters
from .models import LessonPlan


class LessonPlanFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="date_assigned", lookup_expr="gte"
    )
    end_date = django_filters.DateFilter(field_name="date_assigned", lookup_expr="lte")
    completed = django_filters.BooleanFilter(field_name="completed")

    class Meta:
        model = LessonPlan
        fields = ["date_assigned", "due_date", "completed", "start_date", "end_date"]
