from django_filters import rest_framework as filters
from cfapp.models import (
    Tag
)


class TagFilter(filters.FilterSet):
    class Meta:
        model = Tag
        fields = {'name': ['exact', 'contains'], 'created_by': [
            'exact'], 'created_on': ['exact', 'gte', 'lte', 'date__exact', 'date__lte', 'date__gte']}
        # http://127.0.0.1:8000/api/tag/?created_on__date=2019-6-25
        # http://127.0.0.1:8000/api/tag/?name__contains=tag
        # http://127.0.0.1:8000/api/tag/?created_on__date__lte=2019-6-26
        # http://127.0.0.1:8000/api/tag/?ordering=-name
