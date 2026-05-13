# Vehicle Management System

A full-stack Vehicle Management System built with Django, React, and PostgreSQL.

This project simulates a digital platform for vehicle registration, citizen vehicle management, institutional approval workflows, obligations, payments, notifications, and document tracking.

The system is designed as a modern GovTech-style platform focused on vehicle lifecycle management.

# Features

## Authentication & Users
- JWT Authentication
- Citizen registration and login
- Institution/Admin login
- Role-based access

## Citizen Portal
- Register vehicles
- Track vehicle approval status
- View registered vehicles
- Vehicle dashboard
- Vehicle-related obligations
- Payment tracking
- Notifications
- PDF payment receipts

## Institution Portal
- Institution dashboard
- Pending vehicle approvals
- Approve/reject vehicles
- Vehicle monitoring
- Obligation monitoring
- Payment monitoring

## Vehicle Management
- Plate number
- VIN / chassis number
- Vehicle make/model/year
- Vehicle status tracking
- Insurance expiry
- Inspection expiry
- Circulation permit expiry
- Road tax expiry

## Obligations & Payments
- Automatic obligation creation
- Payment processing simulation
- Payment history
- Receipt generation
- Obligation status management

## Notifications
- Vehicle approval notifications
- Payment notifications
- Due-date reminders
- Read/unread tracking

# Tech Stack

## Backend
- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication

## Frontend
- React
- React Router
- Axios
- JavaScript

## Database
- PostgreSQL

# Project Structure

vehicle-management-system/
│
├── backend/
│   ├── apps/
│   ├── core/
│   ├── vehicle_system/
│   └── manage.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── screenshots/
│
├── README.md
└── .gitignore