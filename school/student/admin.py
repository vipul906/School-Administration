from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import HttpRequest
from student.models import Parent, Student, StudentFee


class StudentInline(admin.TabularInline):
    model = Student


class StudentFeeInline(admin.TabularInline):
    model = StudentFee


class ParentAdmin(admin.ModelAdmin):
    inlines = [
        StudentInline,
    ]
    list_display = ['id', 'first_name', 'last_name', 'email', 'children_count']
    search_fields = ['first_name', 'last_name']


class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentFeeInline]
    list_display = ['id', 'first_name', 'last_name', 'email', 'total_fee']


class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'total_amount', 'recieved_amount', 'is_paid']


# Register your models here.
admin.site.register(Parent, ParentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(
    StudentFee,
    StudentFeeAdmin,
)

# # UnRegister your models here.
# admin.site.unregister(Group)
