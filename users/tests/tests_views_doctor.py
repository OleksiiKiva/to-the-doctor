from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from users.models import Specialization

DOCTOR_LIST_URL = reverse("user:doctor-list")
DOCTOR_CREATE_URL = reverse("user:doctor-create")


class PublicPatientListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DOCTOR_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(DOCTOR_LIST_URL)
        self.assertRedirects(response, "/accounts/login/?next=/users/doctors/")


class PrivateDoctorListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="DocUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="DocPassword123",
        )
        self.client.force_login(self.user)

        number_of_doctors = 3
        for doctor_num in range(number_of_doctors):
            get_user_model().objects.create_user(
                username=f"DocUsername{doctor_num}",
                first_name=f"Firstname{doctor_num}",
                last_name=f"Lastname{doctor_num}",
                password="DocPassword123",
                recertification_with="2030-01-02",
            )

    def test_doctor_list_view_url_exists_at_desired_location(self):
        response = self.client.get("/users/doctors/")
        self.assertEqual(response.status_code, 200)

    def test_doctor_list_view_url_accessible_by_name(self):
        response = self.client.get(DOCTOR_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_doctor_list_view_uses_correct_template(self):
        response = self.client.get(DOCTOR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/doctor_list.html")

    def test_doctor_list_pagination_is_three(self):
        response = self.client.get(DOCTOR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["doctor_list"]) == 3)

    def test_doctor_list_all_doctors(self):
        response = self.client.get(DOCTOR_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["doctor_list"]) == 1)

    def test_doctor_search_line(self):
        response = self.client.get(
            DOCTOR_LIST_URL + "?last_name=Lastname&page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(len(response.context["doctor_list"]), 1)
        self.assertEqual(
            str(response.context["doctor_list"][0]), "Lastname2 Firstname2"
        )
        self.assertTrue(
            "Lastname2 Firstname2" in str(response.context["doctor_list"][0])
        )


class PrivateDoctorCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="AdminUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="AdminPassword123",
        )
        self.client.force_login(self.admin)

        specialization = Specialization.objects.create(name="Surgery")

        self.data = {
            "username": "DocUsername",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password1": "DocPassword123",
            "password2": "DocPassword123",
            "recertification_with": "2030-01-02",
            "specializations": specialization.id,
        }

    def test_success_create_new_doctor(self):
        response = self.client.post(DOCTOR_CREATE_URL, data=self.data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 2)

        new_doctor = get_user_model().objects.get(
            username=self.data["username"]
        )

        self.assertEqual(new_doctor.username, self.data["username"])
        self.assertEqual(new_doctor.first_name, self.data["first_name"])
        self.assertEqual(new_doctor.last_name, self.data["last_name"])
        self.assertEqual(
            str(new_doctor.recertification_with),
            self.data["recertification_with"],
        )

    def test_create_new_doctor_and_redirect_success_url(self):
        response = self.client.post(DOCTOR_CREATE_URL, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/users/doctors/", status_code=302)
        self.assertRedirects(
            response, reverse_lazy("user:doctor-list"), status_code=302
        )


class PrivatePatientUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="AdminUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="AdminPassword123",
        )
        self.client.force_login(self.admin)

        specialization = Specialization.objects.create(name="Surgery")

        self.doctor = get_user_model().objects.create_user(
            username="DocUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="DocPassword123",
            recertification_with="2030-01-02",
        )
        self.doctor.specializations.add(specialization)

        self.data = {
            "username": "Doc_Username",
            "password1": "DocPassword123",
            "password2": "DocPassword123",
            "recertification_with": "2040-10-10",
            "specializations": specialization.id,
        }

    def test_update_doctors_recertification_with_field(self):
        response = self.client.post(
            reverse("user:doctor-update", kwargs={"pk": self.doctor.id}),
            self.data,
        )
        self.assertEqual(response.status_code, 302)
        self.doctor.refresh_from_db()
        self.assertEqual(str(self.doctor.recertification_with), "2040-10-10")

    def test_view_doctors_recertification_with_field_update_success_url(self):
        response = self.client.post(
            reverse("user:doctor-update", kwargs={"pk": self.doctor.id}),
            self.data,
        )
        self.assertEqual(response.status_code, 302)
        self.doctor.refresh_from_db()
        self.assertRedirects(response, "/users/doctors/")
        self.assertRedirects(response, reverse_lazy("user:doctor-list"))


class PrivateDoctorDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="AdminUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="AdminPassword123",
        )
        self.client.force_login(self.admin)

        specialization = Specialization.objects.create(name="Surgery")

        self.doctor = get_user_model().objects.create_user(
            username="DocUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="DocPassword123",
            recertification_with="2030-01-02",
        )
        self.doctor.specializations.add(specialization)

    def test_doctor_delete_get_request(self):
        response = self.client.get(
            reverse("user:doctor-delete", kwargs={"pk": self.doctor.id})
        )
        self.assertContains(
            response,
            "Do you want to delete all information about",
        )

    def test_doctor_delete_post_request(self):
        post_response = self.client.post(
            reverse("user:doctor-delete", kwargs={"pk": self.doctor.id})
        )
        self.assertRedirects(
            post_response, reverse("user:doctor-list"), status_code=302
        )
