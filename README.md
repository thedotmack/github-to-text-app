# GitHub Repository Downloader

This is a simple web app that allows users to download the contents of a GitHub repository as a zip file. The app is built using Flask for the backend and Tailwind CSS for styling the frontend.

## Features

- Enter a GitHub repository URL and download its contents as a zip file
- The downloaded zip file contains separate text files for each folder in the repository
- The text files include the file structure and contents of each file in the respective folder

## Prerequisites

- Python 3.x
- Flask
- chardet

## Getting Started

1. Clone the repository or download the project files.

2. Open a terminal or command prompt and navigate to the project directory.

3. Create a virtual environment by running the following command:

   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - For Windows:

     ```
     venv\Scripts\activate
     ```

   - For macOS and Linux:

     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

6. Run the Flask server:

   ```
   python app.py
   ```

7. Open a web browser and visit `http://localhost:5000` or `http://127.0.0.1:5000` to access the web app.

## Usage

1. Enter a valid GitHub repository URL in the input field, e.g., `https://github.com/username/repo`.

2. Click the "Download" button.

3. The server will process the request, generate the zip file, and initiate the download.

4. The downloaded zip file will be saved in your browser's default downloads directory.

## Project Structure

```
github-repo-downloader/
├── app.py
├── index.html
├── requirements.txt
└── venv/
```

- `app.py`: The Flask server code.
- `index.html`: The HTML code for the web app.
- `requirements.txt`: The file containing the project dependencies.
- `venv/`: The virtual environment directory.

## Stopping the Server

To stop the Flask development server, press `CTRL+C` in the terminal where the server is running.

## Deactivating the Virtual Environment

To deactivate the virtual environment, run the following command in the terminal:

```
deactivate
```

## Updating Dependencies

If you need to update the project dependencies or add new ones, follow these steps:

1. Activate the virtual environment (if not already activated).

2. Install or update the desired packages using pip. For example:

   ```
   pip install package_name
   ```

3. Update the `requirements.txt` file with the current dependencies:

   ```
   pip freeze > requirements.txt
   ```

   This command will overwrite the existing `requirements.txt` file with the updated dependencies.

4. Commit the updated `requirements.txt` file to your version control system.

## Troubleshooting

If you encounter any issues or have questions, please feel free to reach out or open an issue in the GitHub repository.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
