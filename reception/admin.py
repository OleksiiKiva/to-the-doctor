from django.contrib import admin

from reception.models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        "date_time",
        "patient",
        "type_of_visit",
        "doctor",
        "treatment_direction",
        "deleted_at",
    )
    list_filter = (
        "treatment_direction",
        "type_of_visit",
        "deleted_at",
    )
    search_fields = ("doctor",)
