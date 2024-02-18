from django.db.models import Q
from student.models import StudentFee


class StudentFeeFilter:
    def __init__(self, query_param, queryset) -> None:
        self.queryset = queryset
        self.query_param: dict = query_param
        self.q_search()
        self.model_filter_search()

    def q_search(self):
        if self.query_param.get('q'):
            value = self.query_param.pop('q')
            self.queryset = self.queryset.filter(
                Q(student__first_name__icontains=value) | Q(student__last_name__icontains=value)
            )
            print(self.queryset, 'Q')

    def model_filter_search(self):
        try:
            self.queryset = self.queryset.filter(**self.query_param)
        except Exception as ex:
            print(f'Unexcepted query params: {ex}')

    @property
    def qs(self):
        return self.queryset
