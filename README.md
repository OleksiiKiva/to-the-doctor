<h1 align="center">🩺 ToTheDoctor 🩺</h1>
<h3 align="center">Service for managing visits, doctors and patients for a medical clinic</h3>
<h3 align="center">Based on Django</h3>

## 📝 Description

A simple service that allows the clinic administrator to make an appointment with a doctor for a patient

* The administrator has all permissions: can create, update, delete visits, doctors and patients
* The doctors do not have permissions to creating, updating, or deleting doctors

### 🌀 Logic of use

* 1️⃣ The clinic administrator creates a patient if he is not in the clinic database
* 2️⃣ Creates a visit, indicating the direction of treatment (for example surgery, therapy, rehabilitation, etc.),
  time and date of the visit, type of visit (initial or repeat)

### Implemented checks:

* date of birth of the patient (an appointment with a doctor is possible from 6 months of age)
* expiration date of the medical certificate
* date of registration for the visit (cannot be less than the current date)

### Implemented a Soft-Delete method

* the process of removing records so that they are still present in the database but are
  not accessible to the user

### The models are implemented according to the following diagram:

![models-diagram](static/picture/models-diagram.png)

## 🛢️Technology stack

* Backend: Python 3.12.1, Django 4.2.7, SQLite
* Frontend: HTML/CSS, Bootstrap 4.2.6
* Virtual Environment: venv
* Environment Variables: .env
* Database Migrations: Django Migrations
* Dependency Management: pip
* Authorization: takes place using a token
* Collaboration and Version Control: Git, GitHub
* Testing: Unittest

## 🔀 Structure description

* the app is available at: [http://localhost:8000](http://localhost:8000)
* `/admin/` -- login to Django admin panel
* `POST /accounts/login/` -- login
* `POST /accounts/logout/` -- logout
* `GET /visits/` -- list of visits (available for authorized users)
* `POST /visits/create/` -- creating a visit
* `GET /users/doctors/` -- current list of doctors of the medical institution
* `GET /users/doctors/1/` -- doctor with id 1
* `GET /users/patients/` -- current list of patients of the medical institution

## 🚀 Install using GitHub

1. Install Python
1. Clone the repo
   ```commandline
   git clone https://github.com/OleksiiKiva/to-the-doctor.git   
   ```
1. Open the project folder in your IDE
1. Open the project terminal folder. Create & activate venv
   ```commandline
   python -m venv venv
   venv\Scripts\activate (on Windows)
   source venv/bin/activate (on Linux/MacOS)
   ```
1. Install all requirements
   ```commandline
   pip install -r requirements.txt
   ```
1. Rename `.env.sample` file as `.env`. Add the environment variables to `.env` file as `KEY=VALUE` pair
   ```
   SECRET_KEY=<your secret key>
   ```
    - generate `SECRET_KEY`
    - copy paste `SECRET_KEY` value to `.env` file
1. Apply migrations & update the database schema
   ```commandline
   python manage.py migrate
   ```
1. Start development server
   ```commandline
   python manage.py runserver
   ```

## 🔑 Credentials

1. Use the following command to load prepared data from fixture for a quick test
    ```
    python manage.py loaddata to_the_doctor_db_data.json
    ```
    - credentials for this fixture: Admin login: `admin@site.com`. Admin password: `Admin-12345`. Doctors
      password: `Doctor12345`
1. Or create a superuser and populate the db yourself

## 📧 Contacts

Please send bug reports and suggestions by email:
[oleksii.kiva@gmail.com](mailto:oleksii.kiva@gmail.com)
