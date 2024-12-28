# Face Swapper

## Project Overview
Face Swapper is an interactive application designed to manipulate images by swapping faces between them. Using the open-source library `inswapper_128.onnx`, the application can detect multiple faces in a picture. Users can select which faces to swap, creating fun and intriguing results. Registered users can have additional features, including the ability to detect biometric data from images. All passwords are securely hashed to ensure privacy and security.

## Installation

### Prerequisites
- Python 3.8 or higher
- Flask
- SQLite

### Set up Python Environment
First, ensure you have Python installed. If not, download and install it from [python.org](https://www.python.org/).

### Clone the Repository
To get started, clone the project repository to your local machine:
```bash
git clone https://github.com/yourusername/faceswapper.git
```
Navigate to the project directory:
```
cd faceswapper
```
and continue with the instruction

### Install Required Libraries
The project dependencies are listed in requirements.txt. Install them using pip:
```
python -m pip install -r requirements.txt
```
### Set up the Database
The application uses SQLite to manage user data. 

To create the faceswapper.db file and initialize the database run following script:  
```
python iniDB.py
```
Afterwards, faceswapper.db should appear in the project folder. To check correctness, use the following commands to see what is in the database:
```
sqlite3 faceswapper.db
```
Once inside, check if the table users is created correctly:
```
.schema
``
You should see following
```
sqlite> .schema
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
```

### Dowloading inswapper_128.onnx
This library weighs around 500 MB, so it could not be attached to this repository. However, this open-source library is available for download here: https://github.com/deepinsight/insightface/issues/2335

Place the downloaded file in the project folder.

## Running the Application

### Activate the Virtual Environment
To isolate our package dependencies locally, create a virtual environment:
```
python -m venv venv
source venv/bin/activate  
# On Windows use `venv\Scripts\activate`
```
f you wish to exit the virtual environment, simply type the following command:
```
deactivate
```

### Start the Flask Application
With the virtual environment activated and dependencies installed, you can start the Flask application:

```
flask run
```
The application will be accessible at http://127.0.0.1:5000 in your web browser.
