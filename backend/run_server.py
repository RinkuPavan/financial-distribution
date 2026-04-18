import uvicorn
from main import app

if __name__ == "__main__":
    try:
        print("Starting Financial Distribution Server...")
        uvicorn.run(app, host="0.0.0.0", port=48765)
    except Exception as e:
        print("ERROR OCCURRED:")
        print(str(e))
        input("Press Enter to exit...")
