# Instagram Clone

This project is a full-stack web application that replicates some of the core features of Instagram. It is built with **FastAPI** for the backend, **SQLAlchemy** for the database, and **Jinja2** for templating. The application is deployed on Render and you can view the live version [here](https://instagram-client-6kow.onrender.com/).

-----

## Features

  * **User Authentication**: Users can sign up and log in to their accounts. Authentication is handled using JWT (JSON Web Tokens).
  * **Create and Manage Posts**: Authenticated users can create, update, and delete their own posts, which include an image and a caption.
  * **Like and Comment on Posts**: Users can like and unlike posts, as well as add and delete comments on posts.
  * **User Profiles**: Each user has a profile page that displays their bio, profile picture, and all of their posts.
  * **Search for Users**: Users can search for other users by their username.
  * **News Feed**: The main page displays a feed of all posts from all users.

-----

## Technologies Used

  * **Backend**: FastAPI, Python 3
  * **Database**: SQLAlchemy, SQLite
  * **Authentication**: JWT (JSON Web Tokens), OAuth2PasswordBearer
  * **Frontend**: HTML5, CSS3, JavaScript, Jinja2
  * **Deployment**: Render

-----

## Getting Started

### Prerequisites

  * Python 3.8+
  * pip

### Installation and Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/RishavDaredevil/instagram-client.git
    cd instagram-client
    ```

2.  **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    The application can be started using `uvicorn`. The `render.yaml` file specifies the start command as:

    ```bash
    uvicorn instagram_client.main:app --host 0.0.0.0 --port 8000
    ```

    The application will be accessible at `http://localhost:8000`.

-----

## Project Structure

```
instagram_client/
├── db/
│   ├── database.py
│   ├── db_comment.py
│   ├── db_like.py
│   ├── db_post.py
│   ├── db_user.py
│   ├── hashing_fn.py
│   └── models.py
├── pydantic_class_for_validation/
│   └── ListOfStrLists.py
├── routers/
│   ├── creating_comment.py
│   ├── creating_like.py
│   ├── insta_post.py
│   ├── instagram_post_page.py
│   ├── login_page.py
│   ├── template_response.py
│   ├── user.py
│   └── user_page.py
├── security/
│   ├── auth_router.py
│   └── oauth.py
├── template/
│   ├── instagram_post_page.html
│   ├── login_page.html
│   └── user_page.html
├── main.py
└── schema.py
```

-----

## API Endpoints

The main API endpoints are defined in the `routers` directory. Here's a summary of the most important ones:

  * **Authentication** (`/login`): Handles user login and returns a JWT access token.
  * **Users** (`/user`):
      * `POST /user`: Create a new user.
      * `GET /users`: Get a list of all users.
      * `GET /user/{username}`: Get a user by their username.
      * `PUT /user/{username}`: Update a user's information.
      * `DELETE /user/{username}`: Delete a user.
      * `GET /users/search`: Search for users by username.
  * **Posts** (`/post`):
      * `POST /post`: Create a new post.
      * `GET /posts`: Get all posts.
      * `PUT /post/{post_id}`: Update a post.
      * `DELETE /post/{post_id}`: Delete a post.
  * **Comments** (`/post/{post_id}/comment`):
      * `POST /post/{post_id}/comment`: Add a comment to a post.
      * `PUT /post/{post_id}/comment/{comment_id}`: Update a comment.
      * `DELETE /post/{post_id}/comment/{comment_id}`: Delete a comment.
  * **Likes** (`/post/{post_id}/like`):
      * `POST /post/{post_id}/like`: Like a post.
      * `DELETE /post/{post_id}/like`: Unlike a post.
