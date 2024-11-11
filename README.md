# XML-to-CSV Parser

## Overview

This project is a simple XML-to-CSV parser built using Python. It reads an XML file containing parts data, extracts relevant information, and saves it into a CSV file. The application uses a graphical user interface (GUI) built with Tkinter to allow users to select input XML files and specify output CSV files.

## Features

- Parse XML files to extract parts data.
- Save extracted data into a CSV file.
- Simple and intuitive GUI for file selection and parsing.

## Requirements

- Python 3.x
- Tkinter
- Pandas
- Numpy
- lxml
- pyinstaller (only for building)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/xml-to-csv.git
    cd xml-to-csv
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```bash
    python src/main.py
    ```

2. Use the GUI to:
    - Select the input XML file.
    - Select the output CSV file.
    - Click the "Parse and Validate" button to parse the XML and save the data to the CSV file.

## Building the .exe

To build the application into an executable file, you can use PyInstaller. Follow these steps:

1. Install PyInstaller:

    ```bash
    pip install pyinstaller
    ```

2. Build the executable:

    ```bash
    pyinstaller --onefile src/main.py --icon logo.ico
    ```

3. The executable will be created in the `dist` directory.

## Contributing

If you want to fork and work on your own version of this project, follow these steps:

1. Fork the repository on GitHub.

2. Clone your forked repository:

    ```bash
    git clone https://github.com/yourusername/xml-to-csv.git
    cd xml-to-csv
    ```

3. Create a new branch for your feature or bugfix:

    ```bash
    git checkout -b my-feature-branch
    ```

4. Make your changes and commit them:

    ```bash
    git add .
    git commit -m "Description of your changes"
    ```

5. Push your changes to your forked repository:

    ```bash
    git push origin my-feature-branch
    ```

6. Create a pull request on the original repository to merge your changes.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

### Icon

The icon used in this project `logo.png` was generated using DALL-E. Please ensure to comply with OpenAI's usage policies when using or distributing this image.
