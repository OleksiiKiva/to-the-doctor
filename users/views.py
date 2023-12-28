from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class PatientListView(LoginRequiredMixin, generic.ListView):
    pass


class PatientDetailView(LoginRequiredMixin, generic.DetailView):
    pass


class PatientCreateView(LoginRequiredMixin, generic.CreateView):
    pass


class PatientUpdateView(LoginRequiredMixin, generic.UpdateView):
    pass


class PatientDeleteView(LoginRequiredMixin, generic.DeleteView):
    pass


class DoctorListView(LoginRequiredMixin, generic.ListView):
    pass


class DoctorDetailView(LoginRequiredMixin, generic.DetailView):
    pass


class DoctorCreateView(LoginRequiredMixin, generic.CreateView):
    pass


class DoctorUpdateView(LoginRequiredMixin, generic.UpdateView):
    pass


class DoctorDeleteView(LoginRequiredMixin, generic.DeleteView):
    pass
