# Blog.Lite v1.0

Create and activate virtual directory before serving program on local host. Ensure you have python and pip installed on your computer before executing the below steps.

* Steps:
- Open Command Prompt
- Navigate to the MAD1 folder
- Create the virtual environment folder: python -m venv .env
- Install the required dependencies: pip install -r requirements.txt
- Activate the virtual environment: .env\Scripts\activate.bat
- Serve the application by running the following command in the shell: python main.py
- Use a web browser of your choice to navigate to the following url: localhost:8080/

You can press Ctrl+C in the command line to stop serving the application and can deactivate the virtual environment using .env\Scripts\deactivate.bat

## Note: It is imperative for the ./database and ./static/images subdirectories to exist for the application to work properly. Please verify these exist before serving the application.
