from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.utils.dates import MONTHS
from django.utils.translation import gettext_lazy as _


class GENDER_CHOICES(models.TextChoices):
    MALE = 'male'
    FEMALE = 'female'
    NOT_SPECIFIED = 'not_specified'


class CLASS_LEVEL(models.TextChoices):
    FIRST = 'I'
    SECOND = 'II'
    THIRD = 'III'
    FOURTH = 'IV'
    FIFTH = 'V'
    SIXTH = 'VI'
    SEVENTH = 'VII'
    EIGHTH = 'VIII'
    NINTH = 'IX'
    TENTH = 'X'
    ELEVENTH = 'XI'
    TWELFTH = 'XII'


class CLASS_SECTION(models.TextChoices):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class MONTH(models.TextChoices):
    JANUARY = 'jan'
    FEBRUARY = 'feb'
    MARCH = 'mar'
    APRIL = 'apr'
    MAY = 'may'
    JUNE = 'jun'
    JULY = 'jul'
    AUGUST = 'aug'
    SEPTEMBER = 'sept'
    OCTOBER = 'oct'
    NOVEMBER = 'nov'
    DECEMBER = 'dec'


class ChangeLoggingMixin(models.Model):
    """
    Provides change logging support for a model. Adds the `created` and `last_updated` fields.
    """

    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True, blank=True, null=True)

    last_updated = models.DateTimeField(verbose_name=_('last updated'), auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class AbstractCustomer(ChangeLoggingMixin):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def __str__(self) -> str:
        return self.full_name()


class Parent(AbstractCustomer):
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=10)

    @property
    def children_count(self):
        return self.students.all().count()


class Student(AbstractCustomer):
    parent = models.ForeignKey(Parent, related_name='students', on_delete=models.CASCADE)
    level = models.CharField(choices=CLASS_LEVEL, max_length=10, null=True, blank=True)
    section = models.CharField(choices=CLASS_SECTION, max_length=1, null=True, blank=True)
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    last_paid = models.DateField(null=True, blank=True)


class StudentFee(ChangeLoggingMixin):
    student = models.ForeignKey(Student, related_name='fee', on_delete=models.CASCADE)
    monthly_fee = models.PositiveIntegerField(default=0)
    exam_fee = models.PositiveIntegerField(default=0)
    transportation_fee = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    recieved_amount = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=200, null=True, blank=True)
    month = models.CharField(choices=MONTH, max_length=20, null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)

    @property
    def total_amount(self):
        """
        Return the total amount of the fee
        """
        total_amount = self.monthly_fee + self.exam_fee + self.transportation_fee
        return total_amount

    def __str__(self) -> str:
        return str(self.student)

    def save(self, *args, **kwargs):
        if self.recieved_amount == self.total_amount:
            self.is_paid = True
        return super().save(args, kwargs)


class FeeStructure(ChangeLoggingMixin):
    monthly_fee = models.PositiveIntegerField(default=0)
    exam_fee = models.PositiveIntegerField(default=0)
    transportation_fee = models.PositiveIntegerField(default=0)
    level = models.CharField(choices=CLASS_LEVEL, max_length=10, null=True, blank=True)
    annual_session = models.CharField(
        blank=True,
        null=True,
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'[0-9]{4}-[0-9]{4}',
                message='Enter a valid session in the format 2023-2024',
                code='invalid_registration',
            )
        ],
    )

    def __str__(self) -> str:
        return self.annual_session
