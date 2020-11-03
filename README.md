# django-rest
Restful-API development by Django rest framework

## Environment

### Ubuntu 20.04.1

```
sudo apt install python3-pip
sudo apt install python3-venv
```

### Local development

- Create venv
    ```
    python3 -m venv venv
    ```

- Install project dependencies
    ```
    pip install -r requirements.txt
    ```

- Create a new django project
    ```
    docker-compose run --rm app sh -c "django-admin.py startproject app ."
    ```

-- Create apps in a django project
    ```
    docker-compose run --rm app sh -c "python manage.py startapp core"
    docker-compose run --rm app sh -c "python manage.py startapp user"
    ```

- Build app docker image
    ```
    docker build .
    ```

- Run test cases
    ```
    docker-compose run --rm app sh -c "python manage.py test"
    docker-compose run --rm app sh -c "python manage.py test && flake8 --ignore=W293,E501"
    ```

- Make migrations for `core` app
    ```
    docker-compose run --rm app sh -c "python manage.py makemigrations core"
    ```

- Create a superuser
    ```
    docker-compose run --rm app sh -c "python manage.py createsuperuser"
    ```
