from django.db import models


class Employee(models.Model):
    employee_code = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    experience = models.PositiveIntegerField()
