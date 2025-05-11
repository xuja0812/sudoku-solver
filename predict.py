import cv2
import numpy as np
from tensorflow.keras.models import load_model
from solver import SSolver
from utils.image_utils import warp_perspective_four_point
import matplotlib.pyplot as plt

def solve_sudoku_image(image_bytes: bytes, model_path="models/model.keras"):
    print("Received image input")
    image_np = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_GRAYSCALE)

    # gaussian blur and adaptive thresholding
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    
    # find contours and sort by area
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if not contours:
        print("countours")
        raise ValueError("No board found")

    # assuming the largest contour is the sudoku board
    board_cnt = contours[0]
    peri = cv2.arcLength(board_cnt, True)
    approx = cv2.approxPolyDP(board_cnt, 0.02 * peri, True)

    if len(approx) != 4:
        print("quad")
        raise ValueError("Board is not quadrilateral")

    # warp the perspective of the board to get a top-down view
    warped = warp_perspective_four_point(img, approx.reshape(4, 2))

    # load the trained model
    model = load_model(model_path)
    side = warped.shape[0] // 9
    board = []

    # iterate through each cell 
    for y in range(9):
        row = []
        for x in range(9):
            # get the cell from the warped image
            cell = warped[y*side:(y+1)*side, x*side:(x+1)*side]
            
            # Show the cell image before resizing and normalizing
            # plt.imshow(cell, cmap='gray')
            # plt.title(f"Cell ({y}, {x}) before resize")
            # plt.show()

            # resize the cell to 28x28 pixels (input size for the model)
            cell = cv2.resize(cell, (28, 28))
            
            # normalize the image (similar to training preprocessing)
            cell = cell.astype("float32") / 255.0
            cell = np.expand_dims(cell, axis=(0, -1))  # Add batch dimension and channel
            
            # Display the resized cell (input to model)
            # plt.imshow(cell[0, :, :, 0], cmap='gray')  # cell[0] is the batch dimension
            # plt.title(f"Cell ({y}, {x}) after resize")
            # plt.show()

            # predict the digit using the model
            pred = model.predict(cell, verbose=0)
            
            # print the model's prediction and its confidence scores
            print(f"Prediction for cell ({y}, {x}): {pred}")
            
            # get the predicted digit from the output (softmax probabilities)
            digit = np.argmax(pred) + 1  # Adjust based on model labels (0 should be ignored)
            print("digit", digit)
            
            # handling case where the model predicts nothing or zero
            if digit == 0:
                digit = 0  # or set to a placeholder like -1 if you want to ignore it

            # add the predicted digit to the row
            row.append(digit)
        
        # add the row to the board
        board.append(row)

    # print the final extracted board
    print("The extracted board is:", board)

    # pass the extracted board to the solver
    solver = SSolver(board)
    if not solver.solve():
        raise ValueError("Unsolvable board")
    
    return solver.board
