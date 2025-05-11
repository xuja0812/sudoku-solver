# Sudoku Solver

## Overview
This iOS app takes in an image of a sudoku board from the user's photo library and outputs the solved version of that sudoku board. The app allows users to take a snapshot of a sudoku puzzle, send it to a Python backend for processing, and then displays the solved board in a user-friendly interface.

## Implementation
The frontend of this app was created in **Swift** using **SwiftUI**. The board-solving algorithm is implemented in **Python** and hosted on a backend using **FastAPI**. When the user uploads an image of a sudoku board, the app communicates with the Python backend to solve the puzzle. Once the puzzle is solved, the solution is returned and displayed on the app’s interface.

### Frontend (Swift):
- **SwiftUI** is used for the user interface.
- The app uses the **UIImagePickerController** to allow users to upload an image from their photo library or capture one using the device’s camera.
- The image is sent to the Python backend for processing through an HTTP request.
- Once the backend solves the board, the app displays the solution in a grid layout with lines separating the squares like a traditional sudoku board.

### Backend (Python with FastAPI):
- The backend uses **FastAPI** to handle requests from the iOS app.
- The solver receives the image, processes it to extract the sudoku grid, and solves the puzzle using a backtracking algorithm.
- The solved board is returned to the app in JSON format.
- The backend also integrates an **OCR (Optical Character Recognition)** method to read the numbers from the uploaded image, allowing the app to work with images of handwritten or printed sudoku boards.

### Features:
- **Capture and Upload**: The user can capture a new image of a sudoku puzzle or choose an existing image from their photo library.
- **Sudoku Solving**: The app communicates with the backend to solve the puzzle using a Python algorithm.
- **Responsive UI**: The solved sudoku board is displayed with a clean and responsive interface.
- **Error Handling**: If an image is invalid or the solver fails, the app provides the user with an error message.

## Technologies Used:
- **Frontend**: Swift, SwiftUI, UIImagePickerController
- **Backend**: Python, FastAPI, OpenCV, OCR for sudoku grid recognition
- **Version Control**: Git, GitHub

