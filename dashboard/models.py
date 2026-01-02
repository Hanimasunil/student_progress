from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"

class Progress(models.Model):
    EXAM_CHOICES = [
        ('Quarterly', 'Quarterly'),
        ('Midterm', 'Midterm'),
        ('Model', 'Model'),
        ('End-Term', 'End-Term'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)


    mathematics = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    science = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    english = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    @property
    def total_marks(self):
        return self.mathematics + self.science + self.english

    @property
    def average(self):
        return self.total_marks / 3

    def __str__(self):
        return f"{self.student.full_name} - {self.exam_type}"
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
