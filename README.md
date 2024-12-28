# Face Swapper

## Project Overview
Face Swapper is an interactive application designed to manipulate images by swapping faces between them. Using the open-source library `inswapper_128.onnx`, the application can detect multiple faces in a picture. 
Users can upload a target image (the destination picture) and another one containing the source face. They can then choose whose face will be replaced by whose, resulting in fun, creative, and often intriguing transformations. Both real photos and AI-generated images can be used seamlessly. Even if there are multiple people in the target image, the application handles it with ease by listing all recognized faces, allowing users to select their preferred one for swapping.

Additionally, the application offers a feature to estimate the age of a person from a photo. Curious to see how old you look? Try it out—but don't take the results too seriously, as it's all just for fun!

The face-swapping and age-estimation features are available exclusively to registered users. For privacy and security, all user passwords are securely hashed, ensuring your personal data remains safe.
### Prerequisites
- Python 3.8 or higher
- Flask
- SQLite

### Set up Python Environment
If Python is not already installed on your system, you can download it from the official Python website: [python.org](https://www.python.org/). Follow the installation instructions for your operating system to ensure everything is set up correctly. 

### Clone the Repository
To get started, clone the project repository to your local machine:
```
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
```
You should see following
```
sqlite> .schema
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
```

### Dowloading inswapper_128.onnx
The inswapper_128.onnx library is an essential component of the application. Since this file is approximately 500 MB in size, it is not included in the project repository. You can download it from the official source here: https://github.com/deepinsight/insightface/issues/2335.

Once downloaded, place the file in the project folder to ensure the application can access it.

## Running the Application

### Activate the Virtual Environment
It is recommended to use a virtual environment to isolate the package dependencies for this project. To create and activate a virtual environment, run the following commands:
```
python -m venv venv
source venv/bin/activate  
# On Windows use
```venv\Scripts\activate
```
If you wish to exit the virtual environment, simply type the following command:
```
deactivate
```

### Start the Flask Application
With the virtual environment activated and all dependencies installed, you’re ready to start the Flask application. Run the following command in your terminal:

```
flask run
```
The application will launch, and you can access it in your web browser at http://127.0.0.1:5000.

### Summary
Face Swapper is a tool designed for creativity and fun, allowing users to experiment with face-swapping and age-estimation features. 
