from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from reception.models import Visit


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = (
            "patient",
            "date_time",
            "treatment_direction",
            "doctor",
            "type_of_visit",
        )

    def clean_date_time(self):
        return validate_date_time(self.cleaned_data["date_time"])


def validate_date_time(date_time):
    """
    Check the visit date field.
    The visit date must be greater than the current date. Timezone-aware!
    """
    queryset = (
        Visit.objects.select_related(
            "treatment_direction", "doctor", "patient"
        )
        .filter(patient__deleted_at__isnull=True)
        .filter(doctor__deleted_at__isnull=True)
        .filter(date_time__gte=datetime.now(date_time.tzinfo))
    )
    for visit in queryset:
        if date_time == visit.date_time:
            raise ValidationError(
                f"{visit.doctor} already has an entry for this date and time. "
                "Please select another date/time or doctor."
            )

    if date_time <= datetime.now(date_time.tzinfo):
        raise ValidationError(
            "The visit date is overdue. Enter a visit date "
            "greater than the current one in YYYY-MM-DD format."
        )

    return date_time


class VisitSearchForm(forms.Form):
    date_time = forms.CharField(
        max_length=10,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by date or time"}
        ),
    )
