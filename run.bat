@echo off
setlocal

:: Check if venv directory exists
IF EXIST venv (
    echo Virtual environment found.
    call venv\Scripts\activate.bat
) ELSE (
    echo Creating virtual environment...
    python -m venv venv
    IF ERRORLEVEL 1 (
        echo Failed to create virtual environment. Please make sure Python is installed.
        pause
        exit /b 1
    )
    call venv\Scripts\activate.bat
    
    :: Update pip without --user flag
    echo Updating pip...
    python -m pip install --upgrade pip
    IF ERRORLEVEL 1 (
        echo Failed to update pip.
        pause
        exit /b 1
    )

    :: Install requirements if requirements.txt exists
    IF EXIST requirements.txt (
        echo Installing requirements...
        pip install -r requirements.txt
        IF ERRORLEVEL 1 (
            echo Failed to install requirements.
            pause
            exit /b 1
        )
    )
)

echo.
echo Virtual environment is ready!
echo Type 'deactivate' to exit the virtual environment.
echo.

:: Keep the window open
cmd /k