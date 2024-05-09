import os
import zipfile
import io
import chardet
import re
import json
from urllib.request import urlopen
from flask import Flask, request, send_file, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process_zip_file', methods=['POST'])
def process_zip_file():
    if 'zipFile' not in request.files:
        return 'No ZIP file found in the request.', 400

    zip_file = request.files['zipFile']
    zip_data = zip_file.read()

    # Create a ZipFile object
    input_zip = zipfile.ZipFile(io.BytesIO(zip_data))

    # List of directories and files to skip
    skip_list = [".gitignore", "node_modules", ".git", "__pycache__"]

    # List of image file extensions to exclude
    image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".ico"]

    # Extract the file structure and create a dictionary to store file paths for each folder
    file_structure = {}
    for file_path in input_zip.namelist():
        base_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_path)[1].lower()

        # Skip directories, files in the skip list, and image files
        if base_name in skip_list or any(skip_dir in file_path for skip_dir in skip_list) or file_extension in image_extensions:
            continue

        folder_path = os.path.dirname(file_path)
        if folder_path not in file_structure:
            file_structure[folder_path] = []
        file_structure[folder_path].append(file_path)

    # Create a BytesIO object to store the zip file contents
    output_zip = io.BytesIO()

    # Create a ZipFile object to write the output files
    with zipfile.ZipFile(output_zip, 'w') as output_zip_file:
        # Create separate text files for each folder path
        for folder_path, file_paths in file_structure.items():
            # Create an output file name based on the folder path
            output_file_name = f"{folder_path.replace('/', '_')}.txt"

            # Create a BytesIO object to store the file contents
            output_file_content = io.BytesIO()

            # Write the file structure for the current folder
            output_file_content.write(f"File Structure for folder '{folder_path}':\n".encode())
            for file_path in file_paths:
                output_file_content.write(f"- {file_path}\n".encode())
            output_file_content.write(b"\n")

            # Write the contents of each file in the current folder
            for file_path in file_paths:
                with input_zip.open(file_path) as file:
                    file_content = file.read()
                    encoding = chardet.detect(file_content)['encoding']
                    if encoding:
                        try:
                            decoded_content = file_content.decode(encoding)
                            output_file_content.write(f"# {file_path}\n".encode())
                            output_file_content.write(decoded_content.encode())
                            output_file_content.write(b"\n\n")
                        except UnicodeDecodeError:
                            pass
                    else:
                        pass

            output_file_content.seek(0)
            output_zip_file.writestr(output_file_name, output_file_content.read())

    output_zip.seek(0)

    # Send the zip file as a response
    return send_file(output_zip, mimetype='application/zip', as_attachment=True, download_name='processed_zip_as_text.zip')

@app.route('/api/download_github_repo', methods=['POST'])
def download_github_repo():
    # Get the GitHub URL from the request data
    data = request.get_json()
    github_url = data['url']

    # Extract the reponame from the URL
    reponame = github_url.split("/")[-1]

    try:
        # Fetch the HTML response from the URL
        response = urlopen(github_url).read().decode('utf-8')

        # Extract all JSON data from the HTML response
        json_data_matches = re.findall(r'<script type="application/json" data-target="react-partial.embeddedData">(.*?)</script>', response, re.DOTALL)

        # Find the JSON data with the 'initialPayload' key
        json_data = None
        for match in json_data_matches:
            try:
                data = json.loads(match)
                if 'initialPayload' in data['props']:
                    json_data = data['props']['initialPayload']
                    break
            except (ValueError, KeyError):
                pass

        if json_data is None:
            return jsonify({"error": "JSON data with 'initialPayload' key not found in the HTML response."}), 404

        # Extract the zipballUrl from the JSON data
        zipball_url = json_data["overview"]["codeButton"]["local"]["platformInfo"]["zipballUrl"]
        full_zipball_url = f"https://github.com{zipball_url}"

        # Download the ZIP file
        zip_data = urlopen(full_zipball_url).read()

        # Create a ZipFile object
        zip_file = zipfile.ZipFile(io.BytesIO(zip_data))

        # List of directories and files to skip
        skip_list = [".gitignore", "node_modules", ".git", "__pycache__"]

        # List of image file extensions to exclude
        image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".ico"]

        # Extract the file structure and create a dictionary to store file paths for each folder
        file_structure = {}
        for file_path in zip_file.namelist():
            base_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_path)[1].lower()

            # Skip directories, files in the skip list, and image files
            if base_name in skip_list or any(skip_dir in file_path for skip_dir in skip_list) or file_extension in image_extensions:
                continue

            folder_path = os.path.dirname(file_path)
            if folder_path not in file_structure:
                file_structure[folder_path] = []
            file_structure[folder_path].append(file_path)

        # Create a BytesIO object to store the zip file contents
        output_zip = io.BytesIO()

        # Create a ZipFile object to write the output files
        with zipfile.ZipFile(output_zip, 'w') as output_zip_file:
            # Create a file to store the entire folder structure
            structure_file_name = f"{reponame}_structure.txt"
            structure_file_content = io.BytesIO()
            structure_file_content.write(b"Folder Structure:\n")
            for folder_path in file_structure:
                structure_file_content.write(f"- {folder_path}\n".encode())
                for file_path in file_structure[folder_path]:
                    structure_file_content.write(f"  - {file_path}\n".encode())
                structure_file_content.write(b"\n")
            structure_file_content.seek(0)
            output_zip_file.writestr(structure_file_name, structure_file_content.read())

            # Create separate text files for each folder path
            for folder_path, file_paths in file_structure.items():
                # Create an output file name based on the folder path
                output_file_name = f"{folder_path.replace('/', '_')}.txt"

                # Create a BytesIO object to store the file contents
                output_file_content = io.BytesIO()

                # Write the file structure for the current folder
                output_file_content.write(f"File Structure for folder '{folder_path}':\n".encode())
                for file_path in file_paths:
                    output_file_content.write(f"- {file_path}\n".encode())
                output_file_content.write(b"\n")

                # Write the contents of each file in the current folder
                for file_path in file_paths:
                    with zip_file.open(file_path) as file:
                        file_content = file.read()
                        encoding = chardet.detect(file_content)['encoding']
                        if encoding:
                            try:
                                decoded_content = file_content.decode(encoding)
                                output_file_content.write(f"# {file_path}\n".encode())
                                output_file_content.write(decoded_content.encode())
                                output_file_content.write(b"\n\n")
                            except UnicodeDecodeError:
                                pass
                        else:
                            pass

                output_file_content.seek(0)
                output_zip_file.writestr(output_file_name, output_file_content.read())

        output_zip.seek(0)

        # Send the zip file as a response
        return send_file(output_zip, mimetype='application/zip', as_attachment=True, download_name=f"{reponame}.zip")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()