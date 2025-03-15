def save_to_file(content, filename):
    
    """ content should be a string """

    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Content saved to {filename}")
    except Exception as e:
        print(f"Error saving content to file: {e}")

