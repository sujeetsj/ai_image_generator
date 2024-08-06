# Chaotix AI Image Generator

## Overview

Chaotix AI Image Generator is a Django-based web application that allows users to generate images based on text prompts using Stability AI’s API. The application utilizes Celery for asynchronous task processing and Redis as the message broker.

## Features

- Accepts multiple text prompts from the user.
- Generates images based on the provided prompts using Stability AI’s API.
- Displays the generated images on the web page.

## Requirements

- Python 3.x
- Django 3.x or higher
- Celery 5.x or higher
- Redis 5.x or higher
- requests library

## Setup Instructions

### Step 1: Clone the Repository

```sh
git clone <repository-url>
cd chaotixai
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate


pip install -r requirements.txt


CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Change port if needed
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Change port if needed



port 6380
redis-server /path/to/redis.conf


python manage.py makemigrations
python manage.py migrate



redis-server


celery -A chaotix_ai worker --loglevel=info




python manage.py runserver
