import io

from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import path
from django.urls.resolvers import URLPattern
from student.filtersets import StudentFeeFilter
from student.models import Parent, Student, StudentFee


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

    def has_change_permission(self, request, obj=None) -> bool:
        return False


class StudentFeeInline(admin.TabularInline):
    extra = 0
    model = StudentFee

    def has_module_permission(self, request: HttpRequest) -> bool:
        return super().has_module_permission(request)

    def has_change_permission(self, request, obj=None) -> bool:
        return False


class ParentAdmin(admin.ModelAdmin):
    inlines = [
        StudentInline,
    ]
    list_display = ['full_name', 'email', 'children_count']
    search_fields = ['first_name', 'last_name']


class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentFeeInline]
    # search_fields = ['first_name', 'last_name']
    list_display = ['full_name', 'email']
    list_filter = ['first_name', 'last_name']


class StudentFeeAdmin(admin.ModelAdmin):
    change_list_template = 'admin/import_unpaid_student_list.html'
    search_fields = ['student__first_name', 'student__last_name']
    list_display = ['id', 'student', 'total_amount', 'recieved_amount', 'is_paid']
    list_filter = ['is_paid']

    def get_urls(self) -> list[URLPattern]:
        urls = super().get_urls()
        custon_urls = [path('import/', self.import_excel, name='excel_import')]
        urls = custon_urls + urls
        return urls

    def import_excel(self, request, *args, **kwargs):
        if request.method == 'POST':
            print(dict(request.GET))
            pass
        print(request.GET)
        query_param = {}
        for key, value in request.GET.items():
            query_param[key] = value
        queryset = self.get_queryset(request=request)
        new_query = StudentFeeFilter(query_param=query_param, queryset=queryset).qs
        import pandas as pd

        df = pd.DataFrame(new_query.values())
        df['last_updated'] = df['last_updated'].dt.tz_localize(None)
        df['created'] = df['created'].dt.tz_localize(None)
        output = io.BytesIO()

        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')

        writer.close()
        xlsx_data = output.getvalue()
        response = HttpResponse(
            xlsx_data,
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=myfile.xlsx'
        return response


# Register your models here.
admin.site.register(Parent, ParentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(
    StudentFee,
    StudentFeeAdmin,
)

# # UnRegister your models here.
# admin.site.unregister(Group)
