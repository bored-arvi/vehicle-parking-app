# e-Vehicle Parking App - V1

A web-based 4-wheeler parking management system with admin and user roles. Built using Flask, Jinja2, Bootstrap, and SQLite.

## Features

### Admin
- Superuser (no registration)
- Create, edit, delete parking lots
- Add/remove parking spots
- Set price per parking lot
- View all parking lot statuses

### User
- Register and login
- View available lots
- Book a parking spot (auto-assigned)
- Vacate a spot

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Jinja2, HTML, CSS, Bootstrap
- **Database**: SQLite (created via code only)

## Database Schema

- **admin**: predefined superuser
- **users**: id, username, password
- **parking_lots**: id, location_name, price, address, pin_code, max_spots
- **parking_spots**: id, lot_id, status (A/O)
- **reservations**: id, spot_id, user_id, start_time, end_time, cost

## Setup

1. Clone the repo
2. Run `app.py` (Flask main file)
3. Database and tables are created programmatically
4. Access locally via browser (e.g., `http://127.0.0.1:5000/`)

## Notes

- No manual DB creation (e.g., DB Browser) allowed
- All functionality works offline on local machine
