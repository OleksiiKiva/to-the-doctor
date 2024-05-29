from datetime import datetime

from django.db import models
from django.conf import settings

from users.models import Patient, Specialization
from utils.models import SoftDeleteModel


class Visit(SoftDeleteModel):
    VISIT_CHOICES = (
        ("INIT", "Initial"),
        ("REPT", "Repeat"),
    )

    treatment_direction = models.ForeignKey(
        Specialization,
        null=True,
        on_delete=models.SET_NULL,
    )
    date_time = models.DateTimeField(default=datetime.now)
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="visits",
    )
    type_of_visit = models.CharField(
        max_length=4,
        choices=VISIT_CHOICES,
        default="REPT",
    )
    patient = models.ForeignKey(
        Patient, null=True, on_delete=models.SET_NULL, related_name="visits"
    )

    class Meta:
        ordering = ("date_time",)
