import sys
import os

if getattr(sys, 'frozen', False):
    # Running as compiled .exe — executable sits in dist/run_server/
    project_root = os.path.dirname(sys.executable)
else:
    # Running as plain .py — go up one level from backend/
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

backend_dir = os.path.join(project_root, 'backend')

sys.path.insert(0, project_root)   # financial-distribution/
sys.path.insert(0, backend_dir)    # financial-distribution/backend/

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