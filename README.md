# FAQ translation API

This project is a FAQ System API with auto-translation to hindi, bengali built using Django, Django REST Framework (DRF), and redis for caching.

## Project Setup

### Prerequisites

Make sure you have the following installed on your local machine:

- Python 3.11+
- pip (Python package installer)
- Redis(up and running)

### Installation Steps (Using Docker)
 Ensure Docker Desktop latest version is installed on your machine, then do the following,

 1. **Clone the Repository**

   Clone this repository to your local machine.

     git clone https://github.com/rahulmakhijasg8/bharatfd_assignment.git
     cd todo
 
 2. ** Run the following command**

    ```
     docker-compose build
     docker-compose up

### Installation Steps (Manual Setup) (Change the redis url in cache in the settings file)

1. **Clone the Repository**

   Clone this repository to your local machine.

   ```bash
   git clone https://github.com/rahulmakhijasg8/bharatfd_assignment.git
   cd todo

2. **Create and Activate a Virtual Environment**

   It's recommended to create a virtual environment to isolate your project dependencies.

   On Linux/macOS:

   ```
   python3 -m venv venv
   source venv/bin/activate

3. **Install requirements.txt**

    ```bash
   pip install -r requirements.txt

4. **Make Migrations and Migrate**

    ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate

  if the api app tables are not created please run:
         
     python3 manage.py makemigrations api
     python3 manage.py migrate api


5. **Create a superuser (Optional)**

    ```bash
   python3 manage.py createsuperuser

6. **Run the server**

    ```bash
   python3 manage.py runserver

7. **For Testing Run**

    ```bash
   # run all tests
   pytest

 Endpoints

GET /api/faqs/: List all faqs in english
GET /api/faqs/?lang=(hi or bn): List all faqs in Hindi or Bengali as per selection
GET /api/faqs/{id}/: Retrieve specific faq in english
GET /api/faqs/{id}/?lang=(hi or bn): Retrieve specific faq in Hindi or Bengali as per selection
POST /api/faqs/: Create a new faq
PUT /api/faqs/{id}/: Update an faq
DELETE /api/faqs/{id}/: Delete an faq
