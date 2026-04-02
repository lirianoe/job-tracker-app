# Job Tracker App

## Overview

This is a web application that allows users to track job applications.
It is built using Flask (Python), MySQL, and HTML/CSS.

## Features

* Manage companies, jobs, applications, and contacts
* Full CRUD operations (Create, Read, Update, Delete)
* Job Match feature that calculates skill match percentages
* Clean and modern user interface

## Setup Instructions

1. Install MySQL and create database:

   * Run schema.sql in MySQL Workbench

2. Install Python dependencies:
   pip install -r requirements.txt

3. Before running the application, set your MySQL password as an environment variable:

export DB_PASSWORD=your_password_here

4. Start the application:
   python3 app.py

5. Open in browser:
   http://127.0.0.1:5000

## Project Structure

* app.py → Flask application
* database.py → Database connection
* templates/ → HTML files
* schema.sql → Database structure
* AI_USAGE.md → AI documentation
* requirements.txt → Dependencies

## Notes

Make sure MySQL is running before starting the app.
