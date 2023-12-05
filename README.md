# social-network

[![Build Status](https://travis-ci.org/anejakartik/social-network.svg?branch=master)](https://travis-ci.org/anejakartik/social-network)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Description of your Django project.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Pip
- Docker (optional, for containerization)

### Installing

1. Clone the repository:

   ```bash
   git clone https://github.com/anejakartik/social-network.git
   cd social-network

2. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

3. Install dependencies:

    ```bash
    pip install -r requirements.txt

4. Running Migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate

5. Running the Development Server

    ```bash
    python manage.py runserver

### Running with Docker (optional):

    ```bash
    docker-compose build
    docker-compose up

### Postman Collections:

