from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from users.forms import UserSearchForm, DoctorForm, PatientForm
from users.models import Doctor, Patient


class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        last_name = self.request.GET.get("last_name", "")
        context["search_form"] = UserSearchForm(
            initial={"last_name": last_name}
        )
        return context

    def get_queryset(self):
        queryset = Patient.objects.filter(
            deleted_at__isnull=True
        )
        form = UserSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                last_name__icontains=form.cleaned_data["last_name"]
            )

        return queryset


class PatientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Patient
    queryset = Patient.objects.filter(
        deleted_at__isnull=True
    )


class PatientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy("user:patient-list")


class PatientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy("user:patient-list")


class PatientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Patient
    success_url = reverse_lazy("user:patient-list")


class DoctorListView(LoginRequiredMixin, generic.ListView):
    model = Doctor
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DoctorListView, self).get_context_data(**kwargs)
        last_name = self.request.GET.get("last_name", "")
        context["search_form"] = UserSearchForm(
            initial={"last_name": last_name}
        )
        return context

    def get_queryset(self):
        queryset = Doctor.objects.prefetch_related(
            "specializations"
        ).filter(
            is_staff=False
        ).filter(
            deleted_at__isnull=True
        )
        form = UserSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                last_name__icontains=form.cleaned_data["last_name"]
            )

        return queryset


class DoctorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Doctor
    queryset = Doctor.objects.prefetch_related("specializations")


class DoctorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Doctor
    form_class = DoctorForm
    success_url = reverse_lazy("user:doctor-list")


class DoctorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Doctor
    form_class = DoctorForm
    success_url = reverse_lazy("user:doctor-list")


class DoctorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Doctor
    success_url = reverse_lazy("user:doctor-list")
