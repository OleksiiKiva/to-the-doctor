from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from reception.forms import VisitSearchForm, VisitForm
from reception.models import Visit
from users.models import Patient, Doctor


@login_required
def index(request):
    """
    View function for the home page of the site.
    """
    num_visits = (
        Visit.objects.filter(deleted_at__isnull=True)
        .filter(date_time__gte=datetime.now())
        .count()
    )
    num_patients = Patient.objects.filter(deleted_at__isnull=True).count()
    num_doctors = (
        Doctor.objects.filter(is_staff=False)
        .filter(deleted_at__isnull=True)
        .count()
    )

    num_visit_page = request.session.get("num_visit_page", 0) + 1
    request.session["num_visit_page"] = num_visit_page

    context = {
        "num_patients": num_patients,
        "num_visits": num_visits,
        "num_doctors": num_doctors,
        "num_visit_page": num_visit_page,
        "is_show_counter": True,
    }

    return render(request, "reception/index.html", context=context)


class VisitListView(LoginRequiredMixin, generic.ListView):
    model = Visit
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VisitListView, self).get_context_data(**kwargs)
        date_time = self.request.GET.get("date_time", "")
        context["search_form"] = VisitSearchForm(
            initial={"date_time": date_time}
        )
        return context

    def get_queryset(self):
        queryset = (
            Visit.objects.select_related(
                "treatment_direction", "doctor", "patient"
            )
            .filter(patient__deleted_at__isnull=True)
            .filter(doctor__deleted_at__isnull=True)
            .filter(date_time__gte=datetime.now())
        )
        form = VisitSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                date_time__icontains=form.cleaned_data["date_time"]
            )

        return queryset


class VisitDetailView(LoginRequiredMixin, generic.DetailView):
    model = Visit
    queryset = (
        Visit.objects.select_related(
            "treatment_direction",
            "doctor",
            "patient",
        )
        .filter(patient__deleted_at__isnull=True)
        .filter(doctor__deleted_at__isnull=True)
    )


class VisitCreateView(LoginRequiredMixin, generic.CreateView):
    model = Visit
    form_class = VisitForm
    success_url = reverse_lazy("reception:visit-list")


class VisitUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Visit
    form_class = VisitForm
    success_url = reverse_lazy("reception:visit-list")


class VisitDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Visit
    success_url = reverse_lazy("reception:visit-list")
