# Casa Shop
Casa Shop is an e-commerce platform built on a microservices architecture, leveraging cutting-edge Deep Learning models for Natural Language Processing (NLP) to enhance product filtration and recommendation functionalities.

## Components

The project consists of several components, each responsible for a specific functionality:

- **EcommerceAI**: Main Django application for managing overall platform operations.
- **Product**: Django application for managing products and related functionalities.
- **Django-auth**: Django application for user authentication and authorization.
- **Policy**: Django application for enforcing platform policies.
- **Search Category**: Flask application for category-based product searching.
- **Search Products**: Flask application for product searching.
- **Similarity Model**: Flask application for product similarity analysis.
- **Product Classification Policy**: FastAPI application for product classification based on policy compliance.

## Running the Servers

To run the servers for different components, follow these steps:

1. Start Django servers:

    ```bash
    venv\Scripts\python EcommerceAI\manage.py runserver
    venv\Scripts\python product\manage.py runserver 5555
    venv\Scripts\python django-auth\manage.py runserver 7777
    venv\Scripts\python policy\manage.py runserver 9999
    ```
    These commands start Django servers for different components of your application (EcommerceAI, product, django-auth, and policy) on different ports. Make sure each of these servers starts successfully without any errors.


2. Start Flask servers:

    ```bash
    venv\Scripts\python search-category\server.py
    venv\Scripts\python search-products\server.py
    venv\Scripts\python similarity model\server.py
    ```
    These commands start Flask servers for search category, search products, and similarity model.
   

4. Start FastAPI server:

    ```bash
    cd Product-classification-policy && venv\Scripts\uvicorn app:app --host 0.0.0.0 --port 1111
    ```
    This command navigates to the Product-classification-policy directory and starts a FastAPI server using uvicorn on port 1111.
   

Make sure all servers are running and accessible.

## Usage

- Access the EcommerceAI platform through the provided endpoints.
- Utilize various functionalities such as product management, user authentication, policy enforcement, product searching, and similarity analysis.
- Interact with different components as required by your application workflow.

## Contribution

Special thanks to [Metkoul](https://github.com/Metkoul) for their contributions to this project.

## License

This project is licensed under the [MIT License](LICENSE).
