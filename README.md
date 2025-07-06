# Semester Planner

This is a Python-based application for interactive semester scheduling of courses. It provides a user-friendly Streamlit interface to assign timeslots to courses, check instructor availability, and prevent conflicts in the weekly plan.

## Features

- Upload instructor availability from Excel
- Automatic generation of 90-minute slots
- Upload and manage a course list
- Assign slots to courses with dropdown selection
- Conflict prevention (no double-bookings)
- Multi-day course support (e.g. 4 semester hours)

## Technologies

- Python 3.12
- Streamlit
- Pandas
- openpyxl

## Installation
```bash
pip install -r requirements.txt
```

## Running the application
```bash
streamlit run app.py
```
