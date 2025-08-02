import os

def add_file(file_path,file_variable_name):
    # Determine file name and extension
    file_name = os.path.basename(file_path)

    file_extension = os.path.splitext(file_name)[1].lower()
    # Determine mimeType based on file extension
    if file_extension in ['.png', '.jpg', '.jpeg']:
        mime_type = f"image/{file_extension[1:]}"
    elif file_extension == '.pdf':
        mime_type = 'application/pdf'
    elif file_extension == '.pptx':
        mime_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    # Read the file content
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Create the file dictionary
    file_info = {

        file_variable_name: {
            "name": file_name,
            "mimeType": mime_type,
            "buffer": file_content,
        }


    }

    return file_info

