from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Specialization, Patient, Doctor


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "deleted_at",)
    list_filter = ("deleted_at",)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "phone_number",
        "date_of_birth",
        "deleted_at",
    )
    list_filter = ("first_name",)
    search_fields = ("last_name",)


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "recertification_with",
        "deleted_at",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            (
                "Additional info",
                {"fields": ("specializations", "recertification_with",)}
            ),
        )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "specializations",
                        "recertification_with",
                    )
                },
            ),
        )
    )
