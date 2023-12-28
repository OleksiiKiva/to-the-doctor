from django.urls import path

from .views import (
    index,
    VisitListView,
    VisitDetailView,
    VisitCreateView,
    VisitUpdateView,
    VisitDeleteView
)

app_name = "reception"

urlpatterns = [
    path("", index, name="index"),
    path("visits/", VisitListView.as_view(), name="visit-list"),
    path("visits/<int:pk>/", VisitDetailView.as_view(), name="visit-detail"),
    path("visits/create/", VisitCreateView.as_view(), name="visit-create"),
    path(
        "visits/<int:pk>/update/",
        VisitUpdateView.as_view(),
        name="visit-update"
    ),
    path(
        "visits/<int:pk>/delete/",
        VisitDeleteView.as_view(),
        name="visit-delete"
    ),
]
