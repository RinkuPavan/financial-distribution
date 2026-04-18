@echo off
echo.
echo ========================================
echo Financial Distribution System Setup
echo ========================================
echo.

echo This script will start the backend server.
echo.
echo Make sure you have Python installed and added to PATH.
echo.
echo Backend will start in a new terminal window.
echo.
echo After starting the backend:
echo 1. Ensure the server is running at http://localhost:8000
echo 2. Load the TDL file into Tally
echo.

pause

start "" cmd /k "cd backend && start_backend.bat"

echo.
echo Setup complete. Backend server should be running in a new window.
echo.
echo To test the system:
echo 1. Open Tally and load the financial_distribution.tdl file
echo 2. Go to the Financial Distribution menu in Tally
echo 3. Click "Generate Plan" with sample values
echo 4. Verify XML response is received and processed correctly
echo.

pause