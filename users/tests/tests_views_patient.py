from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from users.models import Patient

PATIENT_LIST_URL = reverse("user:patient-list")
PATIENT_CREATE_URL = reverse("user:patient-create")


class PublicPatientListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(PATIENT_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(PATIENT_LIST_URL)
        self.assertRedirects(
            response, "/accounts/login/?next=/users/patients/"
        )


class PrivatePatientListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="DocUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="DocPassword123",
        )
        self.client.force_login(self.user)

        number_of_patients = 6
        for patient_num in range(number_of_patients):
            Patient.objects.create(
                phone_number=f"012345678{patient_num}",
                first_name=f"Firstname{patient_num}",
                last_name=f"Lastname{patient_num}",
                date_of_birth="2000-01-02",
            )

    def test_patient_list_view_url_exists_at_desired_location(self):
        response = self.client.get("/users/patients/")
        self.assertEqual(response.status_code, 200)

    def test_patient_list_view_url_accessible_by_name(self):
        response = self.client.get(PATIENT_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_patient_list_view_uses_correct_template(self):
        response = self.client.get(PATIENT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/patient_list.html")

    def test_patient_list_pagination_is_five(self):
        response = self.client.get(PATIENT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["patient_list"]) == 5)

    def test_patient_list_all_manufacturers(self):
        response = self.client.get(PATIENT_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["patient_list"]) == 1)

    def test_patient_search_line(self):
        response = self.client.get(PATIENT_LIST_URL + "?last_name=Last&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(len(response.context["patient_list"]), 1)
        self.assertEqual(
            str(response.context["patient_list"][0]), "Lastname5 Firstname5"
        )
        self.assertTrue(
            "Lastname5 Firstname5" in str(response.context["patient_list"][0])
        )


class PrivatePatientCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="DocUsername",
            first_name="testFirst",
            last_name="testLast",
            password="TestPassword123",
        )
        self.client.force_login(self.user)

        self.form_data = {
            "phone_number": "0123456789",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "date_of_birth": "1965-08-08",
        }

    def test_success_create_new_patient(self):
        response = self.client.post(PATIENT_CREATE_URL, data=self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Patient.objects.count(), 1)

        new_patient = Patient.objects.get(
            phone_number=self.form_data["phone_number"]
        )

        self.assertEqual(
            new_patient.phone_number, self.form_data["phone_number"]
        )
        self.assertEqual(new_patient.first_name, self.form_data["first_name"])
        self.assertEqual(new_patient.last_name, self.form_data["last_name"])
        self.assertEqual(
            str(new_patient.date_of_birth), self.form_data["date_of_birth"]
        )

    def test_create_new_patient_and_redirect_success_url(self):
        response = self.client.post(PATIENT_CREATE_URL, data=self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/users/patients/", status_code=302)
        self.assertRedirects(
            response, reverse_lazy("user:patient-list"), status_code=302
        )


class PrivatePatientUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="DocUsername",
            first_name="testFirst",
            last_name="testLast",
            password="TestPassword123",
        )
        self.client.force_login(self.user)

        self.patient = Patient.objects.create(
            phone_number="0123456789",
            first_name="Firstname",
            last_name="Lastname",
            date_of_birth="2000-01-02",
        )

        self.data = {
            "phone_number": "0123456789",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "date_of_birth": "1965-08-08",
        }

    def test_update_patient(self):
        response = self.client.post(
            reverse("user:patient-update", kwargs={"pk": self.patient.id}),
            self.data,
        )
        self.assertEqual(response.status_code, 302)
        self.patient.refresh_from_db()
        self.assertEqual(str(self.patient.date_of_birth), "1965-08-08")

    def test_view_patient_update_success_url(self):
        response = self.client.post(
            reverse("user:patient-update", kwargs={"pk": self.patient.id}),
            self.data,
        )
        self.assertEqual(response.status_code, 302)
        self.patient.refresh_from_db()
        self.assertRedirects(response, "/users/patients/")
        self.assertRedirects(response, reverse_lazy("user:patient-list"))


class PrivatePatientDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            username="DocUsername",
            first_name="testFirst",
            last_name="testLast",
            password="TestPassword123",
        )
        self.client.force_login(self.user)

        self.patient = Patient.objects.create(
            phone_number="0123456789",
            first_name="Firstname",
            last_name="Lastname",
            date_of_birth="2000-01-02",
        )

    def test_patient_delete_get_request(self):
        response = self.client.get(
            reverse("user:patient-delete", kwargs={"pk": self.patient.id})
        )
        self.assertContains(
            response,
            "Do you want to delete all information about",
        )

    def test_patient_delete_post_request(self):
        post_response = self.client.post(
            reverse("user:patient-delete", kwargs={"pk": self.patient.id})
        )
        self.assertRedirects(
            post_response, reverse("user:patient-list"), status_code=302
        )
