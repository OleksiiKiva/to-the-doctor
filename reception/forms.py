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
    """The function checks the visit date field.
    The visit date must be greater than the current date. Timezone-aware!"""
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
            attrs={
                "placeholder": "Search by date or time"
            }
        ),
    )
