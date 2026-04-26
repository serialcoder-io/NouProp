# NouProp

NouProp is a Django-based web platform designed for managing recyclable materials, community waste reporting, and user-to-user offers.  
It aims to promote environmental responsibility by connecting citizens, enabling reuse, and improving waste management visibility.

---

## Features

### Authentication System
- Email/password authentication (custom Django user model)
- Google OAuth login via django-allauth
- Role-based access control (citizen, staff, etc.)
- Custom signup with additional fields (WhatsApp, role)

### Listings System
- Create, view, and manage recyclable material listings
- Free or paid listings support
- Categories and area-based classification
- Listings visibility controlled by owner

### Offers System
- Users can send offers on listings
- Offer status management: pending, accepted, rejected
- Automatic rejection of other offers when one is accepted
- Listing automatically closes when an offer is accepted

### Reports System
- Users can report waste or environmental issues
- Tag-based classification system
- Location support (latitude / longitude + area)
- Staff moderation dashboard
- Status workflow: pending → validated → in progress → completed/rejected

### Admin & Dashboard
- Custom Django admin powered by DaisyUI theme
- Role-based sidebar navigation
- Staff dashboard with:
  - Reports statistics
  - Status distribution overview
  - Platform activity overview

### Locations
- District and area management system
- Geographical organization of listings and reports

---

## Tech Stack

- Backend: Django
- Authentication: Django Allauth (Google OAuth included)
- Database: PostgreSQL / SQLite (development)
- Frontend: Django templates with Tailwind / DaisyUI
- Admin UI: Django Daisy Admin Theme
- Maps: Leaflet.js (for reports location)

---

## Project Structure

users/ → Custom user system, roles, account management  
listings/ → Listings management  
offers/ → Offer system  
reports/ → Waste/environment reports  
locations/ → Districts & areas 
legal/ → termes of use, legal notice and privacy policy
templates/ → UI templates and admin overrides  

---

## Authentication Flow

- Login and signup handled via django-allauth
- Social login (Google OAuth supported)
- Custom signup form extends allauth with:
  - WhatsApp number
  - Role selection
- Custom user model based on email authentication

---

## Admin Dashboard

- Customized Django admin interface
- Sidebar organized by application modules
- Staff-only analytics dashboard for:
  - Reports statistics
  - Status tracking
  - System overview

---

## Installation

git clone <repo-url>  
python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
python manage.py migrate  
python manage.py createsuperuser  
python manage.py runserver  

---

## Environment Variables

SECRET_KEY=your_secret_key  
DEBUG=True  
DATABASE_URL=your_database_url  
GOOGLE_CLIENT_ID=your_google_client_id  
GOOGLE_CLIENT_SECRET=your_google_client_secret  

---

## Security & Privacy

- Compliant with Mauritius Data Protection Act 2017
- Secure authentication system
- CSRF protection enabled
- Role-based access control

---

## Project Purpose

This project is developed as an academic final-year project focused on:

- Full-stack Django development
- Authentication and authorization systems
- Real-world data modeling
- Admin system customization
- Environmental impact use case

---

## Author

Email: anliomar@outlook.com  
WhatsApp: +230 5729 7857  

---

## License

Academic project — not intended for commercial use.