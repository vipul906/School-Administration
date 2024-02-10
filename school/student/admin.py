from django.contrib import admin
from django.contrib.auth.models import Group
from student.models import Student, Parent, StudentFee
from django.contrib import admin


class StudentInline(admin.TabularInline):
    model = Student

class StudentFeeInline(admin.TabularInline):
    model = StudentFee


class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentFeeInline]
    list_display = ['id','first_name', 'last_name', 'email', 'total_fee']

class ParentAdmin(admin.ModelAdmin):
    inlines = [
        StudentInline,
    ]
    list_display = ['id', 'first_name', 'last_name', 'email', 'children_count']

class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'total_amount']

# Register your models here.
admin.site.register(Parent, ParentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentFee, StudentFeeAdmin, )

# # UnRegister your models here.
# admin.site.unregister(Group)