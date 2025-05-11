from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from predict import solve_sudoku_image  # You will write this

app = FastAPI()

@app.post("/solve")
async def solve_sudoku(file: UploadFile = File(...)):
    print("hello")
    try:
        contents = await file.read()
        board = solve_sudoku_image(contents)
        # board = placeholder(contents)
        board = [[int(cell) for cell in row] for row in board]
        return {"board": board}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
def placeholder(img):
    return [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]
