from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import Specialization, Patient


class SpecializationModelTests(TestCase):
    @classmethod
    def setUp(cls):
        Specialization.objects.create(name="Surgery")

    def test_name_label(self):
        specialization = Specialization.objects.get(id=1)
        field_label = specialization._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        specialization = Specialization.objects.get(id=1)
        max_length = specialization._meta.get_field("name").max_length
        self.assertEqual(max_length, 30)

    def test_specialization_str(self):
        specialization = Specialization.objects.get(id=1)
        self.assertEqual(str(specialization), specialization.name)


class DoctorModelTests(TestCase):
    def setUp(self):
        self.username = "testUser"
        self.first_name = "testFirst"
        self.last_name = "testLast"
        self.password = "TestPassword123"
        get_user_model().objects.create_user(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
        )

    def test_recertification_with_label(self):
        doctor = get_user_model().objects.get(id=1)
        field_label = doctor._meta.get_field(
            "recertification_with"
        ).verbose_name
        self.assertEqual(field_label, "recertification with")

    def test_create_doctor_with_recertification_with_line(self):
        doctor = get_user_model().objects.get(id=1)
        self.assertEqual(str(doctor.username), self.username)
        self.assertEqual(doctor.recertification_with, date.today())
        self.assertTrue(doctor.check_password(self.password))

    def test_doctor_has_a_specialization(self):
        doctor = get_user_model().objects.get(id=1)
        specialization = Specialization.objects.create(name="Surgery")
        doctor.specializations.add(specialization)
        self.assertEqual(specialization.doctors.count(), 1)

    def test_doctor_has_a_some_specializations(self):
        doctor = get_user_model().objects.get(id=1)
        for item in (
            "Surgery",
            "Therapy",
        ):
            specialization = Specialization.objects.create(name=item)
            doctor.specializations.add(specialization)
        self.assertEqual(doctor.specializations.count(), 2)

    def test_doctor_str(self):
        doctor = get_user_model().objects.get(id=1)
        self.assertEqual(str(doctor), f"{self.last_name} {self.first_name}")

    def test_get_absolute_url_doctor(self):
        doctor = get_user_model().objects.get(id=1)
        self.assertEqual(doctor.get_absolute_url(), "/users/doctors/1/")


class PatientModelTests(TestCase):
    def setUp(self):
        self.phone_number = "0672220909"
        self.first_name = "testPatientFirst"
        self.last_name = "testPatientLast"
        Patient.objects.create(
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
        )

    def test_phone_number_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field("phone_number").verbose_name
        self.assertEqual(field_label, "phone number")

    def test_phone_number_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field("phone_number").max_length
        self.assertEqual(max_length, 10)

    def test_phone_number_has_unique(self):
        patient = Patient.objects.get(id=1)
        unique = patient._meta.get_field("phone_number").unique
        self.assertEqual(unique, True)

    def test_first_name_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_first_name_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 30)

    def test_last_name_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_last_name_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 30)

    def test_date_of_birth_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field("date_of_birth").verbose_name
        self.assertEqual(field_label, "date of birth")

    def test_create_patient_with_date_of_birth_line(self):
        patient = Patient.objects.get(id=1)
        self.assertEqual(patient.date_of_birth, date.today())

    def test_patient_str(self):
        patient = Patient.objects.get(id=1)
        self.assertEqual(str(patient), f"{self.last_name} {self.first_name}")

    def test_get_absolute_url_patient(self):
        patient = Patient.objects.get(id=1)
        self.assertEqual(patient.get_absolute_url(), "/users/patients/1/")
