from django.urls import path

from .views import (
    PatientListView,
    PatientDetailView,
    PatientCreateView,
    PatientUpdateView,
    PatientDeleteView,
    DoctorListView,
    DoctorDetailView,
    DoctorCreateView,
    DoctorUpdateView,
    DoctorDeleteView,
)

app_name = "user"

urlpatterns = [
    path("patients/", PatientListView.as_view(), name="patient-list"),
    path(
        "patients/<int:pk>/",
        PatientDetailView.as_view(),
        name="patient-detail",
    ),
    path(
        "patients/create/", PatientCreateView.as_view(), name="patient-create"
    ),
    path(
        "patients/<int:pk>/update/",
        PatientUpdateView.as_view(),
        name="patient-update",
    ),
    path(
        "patients/<int:pk>/delete/",
        PatientDeleteView.as_view(),
        name="patient-delete",
    ),
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
    path(
        "doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"
    ),
    path("doctors/create/", DoctorCreateView.as_view(), name="doctor-create"),
    path(
        "doctors/<int:pk>/update/",
        DoctorUpdateView.as_view(),
        name="doctor-update",
    ),
    path(
        "doctors/<int:pk>/delete/",
        DoctorDeleteView.as_view(),
        name="doctor-delete",
    ),
]
