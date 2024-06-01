# PDF_Insight_App
A full-stack application that allows users to upload PDF documents and ask questions regarding the content of these documents. The backend processes these documents and utilizes natural language processing to provide answers to the questions posed by the users.

# First Setup your React.js App

Step 1: Open git bash and Clone the repository and open the directory

git clone https://github.com/Maanit491/PDF_Insight_App.git

cd PDF_Insight_App

Step2: Open your terminal in the project directory and do

`cd frontend`

Step 3: `npm install`

Step 4: `npm start` 

(Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.)

for more information about react setup, you can refer to the "README.md" File present in the "frontend" folder of this repository.

# FastAPI Application Setup Guide

This guide will help you set up a virtual environment and run a FastAPI application. Follow these steps to get your application up and running.

## Prerequisites

Make sure you have the following installed on your system:
- Python 3.7+
- pip (Python package installer)
- virtualenv (optional but recommended for creating isolated environments)

## Steps

### 1. Clone the Repository

First, clone the repository containing your FastAPI application. Open your terminal and run:

```sh
git clone https://github.com/Maanit491/PDF_Insight_App.git
cd PDF_Insight_App
```

### 2. Create a Virtual Environment

Creating a virtual environment ensures that dependencies are managed separately from other projects. You can create a virtual environment using the `venv` module (included with Python) or `virtualenv`.

#### Using `venv`

```sh
python -m venv env
```

#### Using `virtualenv`

```sh
virtualenv env
```

### 3. Activate the Virtual Environment

Activate the virtual environment you created.

#### On macOS and Linux

```sh
source env/bin/activate
```

#### On Windows

```sh
.\env\Scripts\activate
```

### 4. Install Dependencies

Install the required dependencies using `pip`. Make sure you are in the project directory where the `requirements.txt` file is located.

```sh
pip install -r requirements.txt
```

### 5. Run the Application

Run the FastAPI application using `uvicorn`, which is an ASGI server for Python.

```sh
uvicorn app.main:app --reload
```

- `main` is the name of your Python file (without the `.py` extension) containing the FastAPI app.
- `app` is the name of the FastAPI instance in your `main` file.
- The `--reload` flag is useful for development, as it reloads the server when you make changes to your code.

Your application should now be running at `http://127.0.0.1:8000`.

### 6. Access the Application

Open your web browser and go to:

```
http://127.0.0.1:8000
```

You can also access the automatic interactive API documentation provided by FastAPI:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 7. Deactivate the Virtual Environment

Once you are done working on your application, you can deactivate the virtual environment by running:

```sh
deactivate
```

## Additional Tips

- To add new dependencies, install them using `pip` and update `requirements.txt`:

  ```sh
  pip install <package_name>
  pip freeze > requirements.txt
  ```

- Make sure to commit the updated `requirements.txt` file to your version control system.

## Troubleshooting

If you encounter any issues, consider the following steps:
- Ensure all dependencies are correctly listed in `requirements.txt`.
- Check for typos in file names and paths.
- Review the FastAPI documentation: https://fastapi.tiangolo.com/
