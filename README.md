# FastAPI with Firebase Backend

This project is a FastAPI application that uses Firebase as its backend.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have the following installed:

-   Python 3.8
-   Docker

### Installing

1. Clone the repository

```
git clone https://github.com/yourusername/yourrepository.git
```

2. Change directory into the project

```
cd yourrepository
```

3. Install the required packages

```
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and fill in your Firebase credentials. It should look like this:

```
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
FIREBASE_DATABASE_URL=your_firebase_database_url
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_STORAGE_BUCKET=your_firebase_storage_bucket
FIREBASE_MESSAGING_SENDER_ID=your_firebase_messaging_sender_id
FIREBASE_APP_ID=your_firebase_app_id
FIREBASE_MEASUREMENT_ID=your_firebase_measurement_id
```

5. Build the Docker image

```
docker build -t your-image-name .
```

6. Run the Docker container

```
docker run -p 80:80 your-image-name
```

## Usage

The application has the following endpoints:

-   `GET /`: Returns a simple greeting.
-   `GET /items/{item_id}`: Returns the item with the given ID.
-   `POST /items/`: Creates a new item.
-   `PUT /items/{item_id}`: Updates the item with the given ID.
-   `DELETE /items/{item_id}`: Deletes the item with the given

## Run locally

`python main.py`

`uvicorn main:app --host 0.0.0.0 --port 8080 --reload`

fastapi==0.63.0
uvicorn==0.13.4
pydantic==1.8.1

# bardapi==0.1.34

# jinaai==0.2.7

firebase-admin==6.2.0

docker build -t bhavan-ai-api .
docker run -p 8080:8080 bhavan-ai-api

docker build -t bhavan-ai-api:0.0.1 .
docker run -p 8080:8080 bhavan-ai-api:0.0.1

docker build -t bhavan24/bhavan-ai-api:0.0.1 .
docker run -p 8080:8080 bhavan24/bhavan-ai-api:0.0.1
docker push bhavan24/bhavan-ai-api:0.0.1

To build, run, and push a Docker image with a custom tag, you can use the following commands:

1. Build the Docker image:

```
docker build -t <image-name>:<tag> .
```

Replace `<image-name>` with the desired name for your image and `<tag>` with the custom tag you want to use. The `.` at the end specifies the current directory as the build context.

2. Run the Docker container:

```
docker run -d <image-name>:<tag>
```

Replace `<image-name>` and `<tag>` with the same values used in the build command. The `-d` flag runs the container in detached mode.

3. Push the Docker image to a registry:

```
docker push <image-name>:<tag>
```

Replace `<image-name>` and `<tag>` with the same values used in the build command. This command pushes the image to a Docker registry, such as Docker Hub or a private registry, if you have the necessary permissions.

Make sure you are logged in to the registry using `docker login` before pushing the image.

pipreqs . --force