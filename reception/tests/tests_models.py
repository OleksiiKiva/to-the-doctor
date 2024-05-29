from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from reception.models import Visit
from users.models import Specialization, Patient


def sample_specialization():
    return Specialization.objects.create(name="Surgery")


def sample_doctor(**params):
    defaults = {
        "username": "SampleUsername",
        "first_name": "testFirst",
        "last_name": "testLast",
        "password": "TestPassword123",
    }
    defaults.update(params)

    return get_user_model().objects.create_user(**defaults)


def sample_patient(**params):
    defaults = {
        "phone_number": "0661234567",
        "first_name": "testPatientFirst",
        "last_name": "testPatientLast",
    }
    defaults.update(params)

    return Patient.objects.create(**defaults)


class VisitModelTests(TestCase):
    def setUp(self):
        Visit.objects.create(
            treatment_direction=sample_specialization(),
            doctor=sample_doctor(),
            patient=sample_patient(),
        )

    def test_treatment_direction_label(self):
        visit = Visit.objects.get(id=1)
        field_label = visit._meta.get_field("treatment_direction").verbose_name
        self.assertEqual(field_label, "treatment direction")

    def test_doctor_label(self):
        visit = Visit.objects.get(id=1)
        field_label = visit._meta.get_field("doctor").verbose_name
        self.assertEqual(field_label, "doctor")

    def test_create_visit_with_date_time_line(self):
        visit = Visit.objects.get(id=1)
        self.assertEqual(str(visit.date_time)[0:10], str(date.today()))

    def test_type_of_visit_label(self):
        visit = Visit.objects.get(id=1)
        field_label = visit._meta.get_field("type_of_visit").verbose_name
        self.assertEqual(field_label, "type of visit")

    def test_visit_has_a_type_of_visit(self):
        visit = Visit.objects.get(id=1)
        self.assertEqual(visit.type_of_visit, "REPT")

    def test_patient_label(self):
        visit = Visit.objects.get(id=1)
        field_label = visit._meta.get_field("patient").verbose_name
        self.assertEqual(field_label, "patient")
