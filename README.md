# Fintech Project Setup Guide

This guide provides step-by-step instructions to set up the fintech_project repository on both Ubuntu and Windows systems. Ensure you follow the instructions specific to your operating system.

## Prerequisites
- Git installed
- Python 3 installed
- A terminal or command prompt

## Step 1: Clone the Repository
Clone the project repository to your local machine using the following command:
```
git clone https://github.com/KalminX/fintech_project.git
```

Navigate into the project directory:
```
cd fintech_project
```

## Step 2: Set Up Virtual Environment

### For Ubuntu
#### Create a Virtual Environment
Create a virtual environment named `venv`:
```
python3 -m venv venv
```

#### Activate the Virtual Environment
Activate the virtual environment:
```
source venv/bin/activate
```

### For Windows
#### Create a Virtual Environment
Create a virtual environment named `venv`:
```
python -m venv venv
```

#### Activate the Virtual Environment
Activate the virtual environment:
```
venv\Scripts\activate
```

## Step 3: Configure Environment Variables
A template file named `.env.example` is provided in the repository. Complete the details for your `.env` file:
1. Copy `.env.example` to a new file named `.env`.
2. Fill in the required environment variables (e.g., database credentials, API keys) as per your setup.

## Step 4: Install Dependencies
Install the project dependencies listed in `requirements.txt`:
```
pip install -r requirements.txt
```

## Step 5: Database Setup
Set up the database by creating and applying migrations.

### Make Migrations
Generate migration files based on your models:
```
python3 manage.py makemigrations
```

### Apply Migrations
Apply the migrations to set up the database:
```
python3 manage.py migrate
```

## Step 6: Create a Superuser
Create an admin user to access the Django admin interface:
```
python3 manage.py createsuperuser
```

Follow the prompts to set up your superuser credentials.

## Step 7: Run the Application
Start the development server:
```
python3 manage.py runserver
```

Visit `http://localhost:8000` in your browser to access the application.

## Notes
- Ensure your virtual environment is activated before running any `python3 manage.py` commands.
- For Windows, replace `python3` with `python` in all commands if `python3` is not recognized.
