# Face Swapper

## Project Overview
Face Swapper is an interactive application designed to manipulate images by swapping faces between them. Using the open-source library `inswapper_128.onnx`, the application can detect multiple faces in a picture. Users can select which faces to swap, creating fun and intriguing results. Registered users gain additional features, including the ability to detect biometric data from images. All passwords are securely hashed to ensure privacy and security.

## Installation

### Prerequisites
- Python 3.8 or higher
- Flask
- SQLite

### Set up Python Environment
First, ensure you have Python installed. If not, download and install it from [python.org](https://www.python.org/).

### Clone the Repository
To get started, clone the project repository to your local machine:
```
git clone https://github.com/yourusername/faceswapper.git
```
Being in the project directory 
```
cd faceswapper
```
continue with the instruction
### Install Required Libraries
The project dependencies are listed in requirements.txt. Install them using pip:
```
python -m pip install -r requirements.txt
```
### Set up the Database
The application uses SQLite to manage user data. 
Open sqlite3 in termnal:


Run the following script to create the necessary users table in the database:
```
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);
```
To create the faceswapper.db file and initialize the database, you can use a SQLite client or a Python script. For simplicity, here's how you can do it in Python:
```
import sqlite3

conn = sqlite3.connect('faceswapper.db')
c = conn.cursor()
c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);''')
conn.commit()
conn.close()
```
## Running the Application

### Activate the Virtual Environment
To isolate our package dependencies locally, create a virtual environment:
```
python -m venv venv
source venv/bin/activate  
# On Windows use `venv\Scripts\activate`
```
### Start the Flask Application
With the virtual environment activated and dependencies installed, you can start the Flask application:

```
flask run
```
The application will be accessible at http://127.0.0.1:5000 in your web browser.