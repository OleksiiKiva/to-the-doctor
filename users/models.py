from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from utils.models import SoftDeleteModel


class Specialization(SoftDeleteModel):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Doctor(AbstractUser, SoftDeleteModel):
    recertification_with = models.DateField(default=date.today)
    specializations = models.ManyToManyField(
        Specialization,
        related_name="doctors"
    )

    class Meta:
        ordering = ("last_name",)
        verbose_name = "doctor"
        verbose_name_plural = "doctors"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse("users:doctor-detail", kwargs={"pk": self.pk})


class Patient(SoftDeleteModel):
    phone_number = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(default=date.today)

    class Meta:
        ordering = ("last_name",)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse("users:patient-detail", kwargs={"pk": self.pk})
