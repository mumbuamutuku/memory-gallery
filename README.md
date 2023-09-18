# Memory Gallery App

Memory Gallery is a web application built with Django that allows users to create albums and upload memories to those albums.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed on your system.
- pip package manager installed.
- Virtual environment (optional but recommended).

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/memory-gallery.git

    Navigate to the project directory:
   ```
   ```
   cd memory-gallery
   ```

# Install, Create and activate a virtual environment (optional but recommended):
```
pip install virtualenv
```
```
python -m venv venv
```
- Command Prompt:
```
venv\Scripts\activate
```
- PowerShell:
```
 .\venv_name\Scripts\Activate.ps1
```
- On macOS and Linux:
```
source venv_name/bin/activate
```

- Install the project dependencies:
```
pip install -r requirements.txt
```

- Configure Environment Variables:

- Create a .env file in the root directory of the project and set your environment variables:
```
# Django settings
SECRET_KEY=your key
DEBUG=True
ALLOWED_HOSTS=*

# Email settings
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='host email'
EMAIL_HOST_PASSWORD='host password'
```
 Replace all place holders with your credentials.

# Run Migrations:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
# Create a superuser for admin access:
```
python manage.py createsuperuser
```
# Start the development server:
```
python manage.py runserver
```
The app should now be running at http://127.0.0.1:8000/.

# Usage

 - Access the admin panel by visiting http://127.0.0.1:8000/admin/ and logging in with the superuser credentials you created.

 - Create albums and manage user profiles using the Django admin interface.

    - Access the API endpoints:
       ```
        User Registration: http://127.0.0.1:8000/register/
        User Login: http://127.0.0.1:8000/login/
        User Profile: http://127.0.0.1:8000/profile/
        Album List and Create: http://127.0.0.1:8000/albums/
        Memory List and Create: http://127.0.0.1:8000/memory/
       ```
  - To integrate with a React frontend, make API requests to the above endpoints.

# API Documentation
For detailed API documentation, refer to the provided API documentation file.
Contributing
    
- Fork the project.
   ```
    Create your feature branch (git checkout -b feature/your-feature-name).
    Commit your changes (git commit -m 'Add some feature').
    Push to the branch (git push origin feature/your-feature-name).
    Open a pull request.
   ```
This project is licensed under the MIT License - see the LICENSE file for details.
