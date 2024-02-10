import enum
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class GENDER_CHOICES(models.TextChoices):
    MALE = "male"
    FEMALE = "female"
    NOT_SPECIFIED = "not_specified"

class ChangeLoggingMixin(models.Model):
    """
    Provides change logging support for a model. Adds the `created` and `last_updated` fields.
    """
    created = models.DateTimeField(
        verbose_name=_('created'),
        auto_now_add=True,
        blank=True,
        null=True
    )

    last_updated = models.DateTimeField(
        verbose_name=_('last updated'),
        auto_now=True,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

class AbstractCustomer(ChangeLoggingMixin):

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)

    class Meta:
        abstract = True

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self) -> str:
        return self.get_full_name()
    
class Parent(AbstractCustomer):
    address = models.CharField(max_length=150)

    @property
    def children_count(self):
        return self.students.all().count()

class Student(AbstractCustomer):
    parent = models.ForeignKey(Parent, related_name="students", on_delete=models.CASCADE)

    @property
    def total_fee(self):
        return self.fee.total_amount

class StudentFee(ChangeLoggingMixin):
    student = models.OneToOneField(Student, related_name="fee", on_delete=models.CASCADE)
    monthly_fee = models.PositiveIntegerField()
    exam_fee = models.PositiveIntegerField()
    transportation_fee = models.PositiveIntegerField()

    @property
    def total_amount(self):
        """
        Return the total amount of the fee
        """
        total_amount = self.monthly_fee + self.exam_fee + self.transportation_fee
        return total_amount
    
    def __str__(self) -> str:
        return str(self.student)