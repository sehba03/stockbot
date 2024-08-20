# Stockbot

## Getting Started

Follow these instructions to set up and run the Stockbot project locally.

### Prerequisites

- Python 3.x installed. Check by running:
  ```bash
  python --version


### Clone the Repository
- Clone the repository to your local system:
    ```bash
    git clone <repository_url>
    cd stockbot

### Set Up the Project
- Open the Project in Visual Studio Code

- Open the project folder in Visual Studio Code.

- Open Terminal in Visual Studio Code

- Open the terminal within Visual Studio Code (you can usually find it in the menu or use the shortcut Ctrl+ `).

- Navigate to Your Project Folder

- Navigate to the project directory (if not already there):

    ```bash 
    cd stockbot

### Create a Virtual Environment
- Create a virtual environment to isolate your project's dependencies:
    ```bash
    python -m venv venv

### Activate the Virtual Environment

- Activate the virtual environment:

- On macOS/Linux:

    ```bash
    source venv/bin/activate


-  On Windows:

    ```bash
    venv\Scripts\activate

### Install Dependencies

- Install the necessary Python packages:

    ```bash
    pip install Flask flask_sqlalchemy requests beautifulsoup4 transformers torch flask-cors

### Run the Website
- Run the Flask application:

    ```bash
    python app.py


### Access the Website

- Click on the URL shown in the terminal, typically http://127.0.0.1:5000 or http://localhost:5000, to view the website.

