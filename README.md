## This project is part of my masters degree at the Kingston University, module CI7260.

# Job Seeker Platform

### Individual Project

### Description
This project is a CV (Curriculum Vitae) management system built using Flask, a Python web framework. It allows candidates to register, log in, create and download their CV. Employers can also register, log in, and search for candidates based on various criteria.

The project uses SQLAlchemy, a popular Object-Relational Mapping (ORM) library, to interact with a SQLite database for storing user information and CV details. The system supports basic CRUD operations (Create, Read, Update, Delete) for candidates, employers, and CVs.

Infuture I will host it in AWS and containerize using Docker.

### Prerequisites
Python 3.x
Flask
Flask SQLAlchemy
ReportLab

### Installation
Clone the repository or download the source code.<br />
Open a terminal and navigate to the project directory.<br />
Create a virtual environment (optional but recommended):<br />
In the terminal run using<br />

### Docker Setup
This project can be set up using docker as well. Dockerfile is available with the source code.


### Set up the database:
Open the app.py file.<br />
Uncomment the appropriate line based on your database preference (SQLite or MS SQL Server).<br />
Save the file.<br />
Initialize the database:<br />
In the terminal, run python app.py to create the necessary tables.<br />
Start the application:<br />
In the terminal, run python app.py.<br />
Open a web browser and visit http://localhost:5000 to access the CV Management System.<br />


### Usage:
Home Page (/): Displays a simple landing page.<br />
Candidate Registration (/candidate_register): Allows candidates to register by providing a username, password, and email.<br />
Candidate Login (/candidate_login): Enables candidates to log in using their credentials.<br />
Employer Registration (/employer_register): Allows employers to register by providing a username, password, and email.<br />
Employer Login (/employer_login): Enables employers to log in using their credentials.<br />
Candidate Dashboard (/candidate_dashboard): Shows a dashboard for logged-in candidates, allowing them to manage their profile and CV.<br />
Advanced Search (/employer_dashboard): Allows employers to search for candidates based on various filters, such as name, address, experience, skills, etc.<br />
Candidate Profile (/candidate_profile): Allows candidates to view and update their profile information.<br />
Employer Profile (/employer_profile): Allows employers to view and update their profile information.<br />
Candidate CV (/candidate_cv): Allows candidates to create and update their CV, including personal details, skills, experience, etc.<br />
CV Detail (/cv/<int:cv_id>): Displays detailed information about a specific CV.<br />
Download CV (/download_cv): Allows candidates to download their CV as a PDF file.<br />
Logout (/logout): Logs out the currently logged-in user.<br />
