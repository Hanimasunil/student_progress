# Student Progress Management System

A Django-based web application to manage students and track their progress efficiently.  
This project is designed as an academic mini project / internship task using Django.

---

## Features

- User authentication (Login / Logout)
- Student management (Add, View, Edit, Delete)
- Progress tracking for each student
- User-specific data access
- Pagination for better data handling
- Secure access using Django authentication
- Clean and simple UI

---

## Technologies Used

- Python 3
- Django
- SQLite (default database)
- HTML, CSS

---

## Project Structure

student_progress/
│
├── student_progress/ # Project settings
├── app/ # Main application
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ ├── urls.py
│ └── templates/
│
├── manage.py
└── README.md


---

## Installation & Setup

1. Clone the repository
```bash
git clone <repository-url>
cd student_progress
2. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install django

4. Run migrations
python manage.py makemigrations
python manage.py migrate

5. Create superuser
python manage.py createsuperuser

6. Run the server
python manage.py runserver


Open browser and visit:

http://127.0.0.1:8000/

Usage

Admin can manage users and student data

Users can log in and manage their assigned students

Track student progress with status updates

View progress history

Future Enhancements

License

This project is for educational purposes.




