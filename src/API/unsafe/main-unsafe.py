from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def first_example():
  '''
     FG Example First Fast API Example 
  '''
    return {"GFG Example": "FastAPI"}