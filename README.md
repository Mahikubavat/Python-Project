# ShareLocal

A community-driven platform for sharing items locally, promoting sustainability and building stronger neighborhoods through collaborative consumption.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

ShareLocal is a Django-based web application that connects people in local communities to share items they no longer need or want to lend. Whether you're giving away clothes, lending tools, selling gently used items, or renting out equipment, ShareLocal makes it easy to find people nearby who might need what you have to offer.

The platform focuses on building sustainable communities by reducing waste, encouraging reuse, and fostering neighborly connections through location-based sharing.

## Features

### 🏘️ Community Sharing
- **Local Focus**: Connect with people in your neighborhood and nearby areas
- **GPS Integration**: Location-based search and filtering using GPS coordinates
- **Geocoding**: Automatic location conversion for easy address management

### 📦 Item Management
- **Multiple Sharing Types**: Give away, sell, or rent items
- **Categories**: Organize items by type (Electronics, Clothing, Books, Home, etc.)
- **Rich Descriptions**: Detailed item listings with photos and descriptions
- **Availability Control**: Mark items as available or unavailable

### 🤝 Request System
- **Easy Requests**: Simple system to request items from other users
- **Status Tracking**: Track request status (Pending, Accepted, Rejected)
- **Communication**: Built-in messaging through request management

### 👤 User Features
- **User Profiles**: Complete profiles with photos and contact information
- **Dashboard**: Personal dashboard showing your items and requests
- **Request History**: Track all your borrowing and lending activity

### 🔍 Discovery
- **Search & Filter**: Find items by location, category, and keywords
- **Featured Items**: Highlight recently added available items
- **Statistics**: Community stats showing total items, users, and requests

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment support
- SQLite (included with Python) or PostgreSQL

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Mahikubavat/Python-Project.git
cd Python-Project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
cd sharelocal
python manage.py migrate
```

5. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to access ShareLocal.

## Usage

### For New Users
1. **Register**: Create an account with your location information
2. **Complete Profile**: Add a profile photo and contact details
3. **Browse Items**: Explore available items in your area
4. **Make Requests**: Request items you're interested in

### For Item Owners
1. **List Items**: Add items you want to share, sell, or rent
2. **Manage Requests**: Accept or reject incoming requests
3. **Update Availability**: Mark items as available or unavailable
4. **Track Activity**: Monitor who has requested your items

### Basic Workflow
1. User A lists an item (e.g., "Power drill - Give Away")
2. User B searches for "power tools" and finds the listing
3. User B submits a request for the item
4. User A receives notification and can accept/reject the request
5. If accepted, users coordinate pickup/delivery locally

## Project Structure

```
Python-Project/
├── sharelocal/                 # Main Django project
│   ├── accounts/              # User management and profiles
│   │   ├── models.py         # UserProfile model with GPS
│   │   ├── views.py          # Registration, login, profile
│   │   └── templates/        # User-related templates
│   ├── core/                 # Core functionality
│   │   ├── models.py         # Categories and locations
│   │   └── views.py          # Home page with statistics
│   ├── items/                # Item management
│   │   ├── models.py         # Item model with GPS/location
│   │   ├── views.py          # CRUD operations for items
│   │   └── templates/        # Item listing and detail templates
│   ├── request_app/          # Request management system
│   │   ├── models.py         # ItemRequest model
│   │   ├── views.py          # Request creation and management
│   │   └── templates/        # Request-related templates
│   ├── sharelocal/           # Django settings and configuration
│   ├── templates/            # Global templates (base.html)
│   ├── media/                # User-uploaded files
│   └── db.sqlite3            # SQLite database
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Development

### Code Style

This project follows Python best practices and uses:
- Django 4.2 LTS
- SQLite for development (easily configurable for PostgreSQL/MySQL)
- Bootstrap 5 for responsive UI
- GPS/geocoding integration with OpenStreetMap Nominatim API

### Key Technologies
- **Backend**: Django (Python web framework)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Location Services**: GPS coordinates, geocoding
- **Media Handling**: Django's file upload system

### Running Tests

```bash
cd sharelocal
python manage.py test
```

### Development Commands

```bash
# Create new app
python manage.py startapp new_app

# Make migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic
```

## Contributing

We welcome contributions to ShareLocal! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Areas for Contribution
- UI/UX improvements
- Mobile responsiveness
- Additional sharing categories
- Messaging system between users
- Review/rating system
- API development for mobile apps
- Multi-language support

### Development Guidelines
- Follow Django best practices
- Write tests for new features
- Update documentation
- Ensure responsive design
- Test location-based features thoroughly

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**ShareLocal** - Building sustainable communities through sharing. 

##  Testing

Run the test suite:

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=sharelocal tests/
```

##  Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the LICENSE file for details.

**Last Updated:** February 23, 2026
