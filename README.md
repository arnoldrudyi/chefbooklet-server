# ChefBooklet Server

ChefBooklet is a web application designed to help users discover recipes based on the ingredients they have on hand. It also provides functionality to suggest random dishes and filter recipes by nationality. This repository contains the backend server built with Django.

## Key Features

- **User Authentication**
    - Implements JWT-based authentication.
    - Certain endpoints are restricted to authorized users.
- **Recipe Management**
    - Superusers can add new recipes to the database.
    - Users can search for recipes by entering available ingredients.
    - Users can get random recipe suggestions.
    - Users can filter recipes by selected national cuisines.
    - Users can add recipes to their favorites.

## Development Requirements

The application is deployed at **[ChefBooklet API](https://chefbooklet-api.fly.dev/)**. For local development, follow the steps below.

### Technical Requirements

- Python 3.9+
- Django 4.2+
- Django REST Framework
- Docker 24.0+

### Prerequisites

Before running the server, ensure that you have the following prerequisites installed:

1. **Python and pip**: If you don't have Python and pip installed, you can download and install them from the official Python website: **[Python Downloads](https://www.python.org/downloads/)**.

2. **Docker**: Make sure you have Docker installed. You can download and install Docker from the official Docker website: **[Docker Installation](https://docs.docker.com/get-docker/)**.

### Configuration

1. Clone the repository:
    ```sh
    git clone https://github.com/arnoldrudyi/chefbooklet-server.git
    cd chefbooklet-server
    ```

2. Create and configure your `.env` file:

    **Database Configuration**
    - `POSTGRES_USER`: Your PostgreSQL username.
    - `POSTGRES_PASSWORD`: Your PostgreSQL password.
    - `POSTGRES_DB`: Your desired database name.
    - `POSTGRES_HOST`: Set to `chefbooklet_postgresql` by default if running through Docker.

    **Django Secret Key**
    - Generate a secret key from the [Secret Key Generator](https://djecrety.ir/) and set it in your `.env` file as `SECRET_KEY`.

    **S3 Data Storage Configuration (Optional)** 
    
    By default, all media files will be stored on the local machine storage. But if you want, you can configure the AWS S3 Bucket to store those data:
    - `USE_S3`: Set to `true` if using AWS S3 for media storage.
    - `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
    - `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
    - `AWS_STORAGE_BUCKET_NAME`: Your AWS bucket name.

    Example `.env` file:
    ```plaintext
    POSTGRES_USER='admin'
    POSTGRES_PASSWORD='v6xPoIu9Ot2V'
    POSTGRES_DB='database'
    POSTGRES_HOST='chefbooklet_postgresql'
    SECRET_KEY='hc$zk9#5t_s^c#*#a^kxneqj7f6ht^x^pa$&hnz$b2($rkay+_'
    USE_S3="true"
    AWS_ACCESS_KEY_ID='5FO8130LQS898MFBEP7P'
    AWS_SECRET_ACCESS_KEY='1pwVCEwclicZVy6xzxMR0nzVB4uHxvm6dyNn8L6e+sI='
    AWS_STORAGE_BUCKET_NAME='chefbooklet-media'
    ```

### Running the Application

1. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Load the environment variables and run the Docker container:
    ```sh
    set -a && source .env && set +a
    docker-compose up
    ```
4. Apply the database migrations:
    ```sh
    python3 manage.py migrate
    ```
5. Run the development server:
    ```sh
    python3 manage.py runserver
    ```

    Once the server is running, it will be accessible at `http://localhost:8000/`. You can interact with the API using an API client like Postman or through the **[frontend application](https://github.com/arnoldrudyi/chefbooklet-client)**.

## License
This project is licensed under the MIT License - see the **[LICENSE](LICENSE)** file for details. Contributions are welcome!
