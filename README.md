# DS Pergola - Sudoku with Handwritten Digit Recognition (Trained with MNIST data)

### 1. Project Scope

Developing a Sudoku app, which allows users to enter numbers by drawing on screen. 
Drawed canvas will be classified as digits (1 to 9) by a Machine Learning algorithm(?).

### 2. Components
#### 2.1 Application Layer
Application runs on a Flask Server (python) and UI is developed with HTML, CSS and JavaScript.
Sudoku logic is built in the JS layer.

Each sudoku cell can be entered by drawing a digit, then will be recognized by a model which was trained by MNIST dataset.
#### 2.2 Model
**Option 1:** Exporting model in a file (.h5 or similar) and will be consumed in Flask app directly.

**Option 2:** Prediction will be deployed as a service and will be consumed via an API by the application.

#### 2.3 Training
//Model training details

#### 2.4 Data Storage
Drawed images are currently stored under digits/ directory with a timestamp name in png format.
In future, each prediction will be stored into a database with prediction result, and if possible with a feedback from the user.

### 3. Architecture
![ScreenShot](architecture.png)

Diagram is drawed in [Draw.io](https://github.com/jgraph/drawio-desktop/releases/tag/v13.5.1)

### 4. How to Setup

1. Create a new virtual environment
```
conda create --name mnist
conda activate mnist 
```
2. Install packages in [requirements.txt](requirements.txt) into the new environment
```
conda install -c conda-forge packages.txt
```
2. Download the project folder with:  
```
git clone https://github.com/ds-pergola/handwritten-sudoku.git
```
3. Run application
```
python app.py
```
4. Visit the URL:

http://0.0.0.0:5000/

http://localhost:5000/
