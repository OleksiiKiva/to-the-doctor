from datetime import date, timedelta

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from users.models import Doctor, Specialization, Patient


class UserSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=10,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by last name"
            }
        ),
    )


class DoctorForm(UserCreationForm):
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserCreationForm.Meta):
        model = Doctor
        fields = (
            "first_name",
            "last_name",
            "email",
            "specializations",
            "recertification_with",
            "username",
            "password1",
            "password2",
        )

    def clean_recertification_with(self):
        return validate_recertification_with(
            self.cleaned_data["recertification_with"]
        )


def validate_recertification_with(recertification_with):
    """The function checks the validity period of the doctor's certificate.
    The date on the certificate must be greater than the current date."""
    if recertification_with <= date.today():
        raise ValidationError(
            "The date has expired. "
            "Please enter correct data in YYYY-MM-DD format"
        )

    return recertification_with
