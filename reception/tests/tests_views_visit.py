from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from reception.models import Visit
from users.models import Specialization, Patient

VISIT_LIST_URL = reverse("reception:visit-list")
VISIT_CREATE_URL = reverse("reception:visit-create")


class PublicVisitListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(VISIT_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(VISIT_LIST_URL)
        self.assertRedirects(response, "/accounts/login/?next=/visits/")


class PrivateVisitListViewTest(TestCase):
    def setUp(self):
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

        self.patient = Patient.objects.create(
            phone_number="0123456789",
            first_name="Firstname",
            last_name="Lastname",
            date_of_birth="2000-01-02",
        )

        number_of_visits = 3
        for visit_num in range(number_of_visits):
            Visit.objects.create(
                treatment_direction=specialization,
                date_time="2030-01-02",
                doctor=self.doctor,
                patient=self.patient,
            )

    def test_visit_list_view_url_exists_at_desired_location(self):
        response = self.client.get("/visits/")
        self.assertEqual(response.status_code, 200)

    def test_visit_list_view_url_accessible_by_name(self):
        response = self.client.get(VISIT_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_visit_list_view_uses_correct_template(self):
        response = self.client.get(VISIT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reception/visit_list.html")

    def test_visit_list_pagination_is_two(self):
        response = self.client.get(VISIT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["visit_list"]) == 2)

    def test_visit_list_all_visits(self):
        response = self.client.get(VISIT_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["visit_list"]) == 1)

    def test_visit_search_line(self):
        response = self.client.get(
            VISIT_LIST_URL + "?date_time=2030-01-02&page=2"
        )
        # print(response.context["visit_list"][0].date_time)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(len(response.context["visit_list"]), 1)
        self.assertEqual(
            str(response.context["visit_list"][0].date_time),
            "2030-01-02 00:00:00",
        )
        self.assertTrue(
            "2030-01-02 00:00:00"
            in str(response.context["visit_list"][0].date_time)
        )


class PrivateVisitCreateViewTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="AdminUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="AdminPassword123",
        )
        self.client.force_login(self.admin)

        specialization = Specialization.objects.create(name="Surgery")

        doctor = get_user_model().objects.create_user(
            username="DocUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="DocPassword123",
            recertification_with="2030-01-02",
        )
        doctor.specializations.add(specialization)
        self.doctor = get_user_model().objects.get(username="DocUsername")

        self.patient = Patient.objects.create(
            phone_number="0123456786",
            first_name="Firstname",
            last_name="Lastname",
            date_of_birth="2000-01-02",
        )

        self.data = {
            "patient": self.patient.id,
            "date_time": "2031-01-01",
            "treatment_direction": specialization.id,
            "doctor": self.doctor.id,
            "type_of_visit": "REPT",
        }

    def test_success_create_new_visit(self):
        response = self.client.post(VISIT_CREATE_URL, data=self.data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Visit.objects.count(), 1)

        new_visit = Visit.objects.get(date_time=self.data["date_time"])

        self.assertEqual(new_visit.patient.id, self.data["patient"])
        self.assertEqual(str(new_visit.date_time)[:10], self.data["date_time"])
        self.assertEqual(
            new_visit.treatment_direction.id, self.data["treatment_direction"]
        )
        self.assertEqual(new_visit.doctor.id, self.data["doctor"])
        self.assertEqual(new_visit.type_of_visit, self.data["type_of_visit"])

    def test_create_new_visit_and_redirect_success_url(self):
        response = self.client.post(VISIT_CREATE_URL, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/visits/", status_code=302)
        self.assertRedirects(
            response, reverse_lazy("reception:visit-list"), status_code=302
        )


class PrivatePatientUpdateViewTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="AdminUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="AdminPassword123",
        )
        self.client.force_login(self.admin)

        specialization = Specialization.objects.create(name="Surgery")

        doctor = get_user_model().objects.create_user(
            username="DocUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="DocPassword123",
            recertification_with="2030-01-02",
        )
        doctor.specializations.add(specialization)
        self.doctor = get_user_model().objects.get(username="DocUsername")

        self.patient = Patient.objects.create(
            phone_number="0123456785",
            first_name="Firstname",
            last_name="Lastname",
            date_of_birth="2000-01-02",
        )

        self.visit = Visit.objects.create(
            patient=self.patient,
            date_time="2031-01-01",
            treatment_direction=specialization,
            doctor=self.doctor,
            type_of_visit="REPT",
        )

        self.data = {
            "patient": self.patient.id,
            "date_time": "2032-02-02",
            "treatment_direction": specialization.id,
            "doctor": self.doctor.id,
            "type_of_visit": "INIT",
        }

    def test_update_visit(self):
        response = self.client.post(
            reverse("reception:visit-update", kwargs={"pk": self.visit.id}),
            self.data,
        )
        self.assertEqual(response.status_code, 302)
        self.visit.refresh_from_db()
        self.assertEqual(str(self.visit.date_time)[:10], "2032-02-02")
        self.assertEqual(str(self.visit.type_of_visit), "INIT")

    def test_view_visit_update_success_url(self):
        response = self.client.post(
            reverse("reception:visit-update", kwargs={"pk": self.visit.id}),
            self.data,
        )
        self.assertEqual(response.status_code, 302)
        self.visit.refresh_from_db()
        self.assertRedirects(response, "/visits/")
        self.assertRedirects(response, reverse_lazy("reception:visit-list"))


class PrivateVisitDeleteViewTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="AdminUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="AdminPassword123",
        )
        self.client.force_login(self.admin)

        specialization = Specialization.objects.create(name="Surgery")

        doctor = get_user_model().objects.create_user(
            username="DocUsername",
            first_name="Firstname",
            last_name="Lastname",
            password="DocPassword123",
            recertification_with="2030-01-02",
        )
        doctor.specializations.add(specialization)
        self.doctor = get_user_model().objects.get(username="DocUsername")

        self.patient = Patient.objects.create(
            phone_number="0123456785",
            first_name="Firstname",
            last_name="Lastname",
            date_of_birth="2000-01-02",
        )

        self.visit = Visit.objects.create(
            patient=self.patient,
            date_time="2031-01-01",
            treatment_direction=specialization,
            doctor=self.doctor,
            type_of_visit="REPT",
        )

    def test_visit_delete_get_request(self):
        response = self.client.get(
            reverse("reception:visit-delete", kwargs={"pk": self.visit.id})
        )
        self.assertContains(
            response,
            "Do you want to delete all visit information?",
        )

    def test_visit_delete_post_request(self):
        post_response = self.client.post(
            reverse("reception:visit-delete", kwargs={"pk": self.visit.id})
        )
        self.assertRedirects(
            post_response, reverse("reception:visit-list"), status_code=302
        )
