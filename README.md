# Job Compass: Career Guidance for Job Seekers

A comprehensive job search platform that connects job seekers with employers.

## Features

- **User Management**: Registration, authentication, and profile management
- **Resume Building**: Create and manage professional resumes
- **Job Listings**: Browse and apply to job opportunities
- **Company Profiles**: View company information and available positions
- **Industry Categories**: Filter jobs by industry
- **Skill Matching**: Match skills with job requirements
- **Dashboard**: Personalized dashboard for job tracking

## Tech Stack

- **Backend**: Django 5.1
- **Database**: PostgreSQL
- **File Storage**: Cloudinary
- **Authentication**: Custom email-based authentication with OTP verification
- **Styling**: Widget Tweaks, Bootstrap 5, Vanilla CSS
- **Deployment**: Whitenoise for static files, configured for Render

## Setup

### Prerequisites

- Python 3.x
- PostgreSQL database
- Cloudinary account

### Local Development

1. Clone the repository
```
git clone <repository-url>
cd jobcompass_env
```

2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Set up environment variables
```
# Django
export SECRET_KEY='your-secret-key'
export DEBUG=True

# Database
export DATABASE_URL='sqlite:///db.sqlite3'  # For local development

# Email (for OTP)
export EMAIL_HOST_USER='your-email@example.com'
export EMAIL_HOST_PASSWORD='your-app-password'

# Cloudinary
export CLOUDINARY_CLOUD_NAME='your-cloud-name'
export CLOUDINARY_API_KEY='your-api-key'
export CLOUDINARY_API_SECRET='your-api-secret'
```

5. Run migrations
```
python manage.py migrate
```

6. Create a superuser
```
python manage.py createsuperuser
```

7. Start the development server
```
python manage.py runserver
```

### Production Deployment

The application is configured for deployment on Render. Set the following environment variables:

- `DATABASE_URL`: Your PostgreSQL connection string
- `SECRET_KEY`: A secure secret key
- `RENDER_EXTERNAL_HOSTNAME`: Will be set automatically by Render

## Usage

1. Access the admin panel at `/admin/` to manage site content
2. Users can register and create profiles
3. Job seekers can create resumes and apply for jobs
4. Employers can post job listings and review applications

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For support or inquiries, contact jobcompassco@gmail.com 
