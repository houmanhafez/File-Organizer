# File Organizer

Browser File Organizer is a Python script designed to monitor the default browser on your system and organize downloaded files into folders based on their types. It works seamlessly in the background, ensuring your downloads are neatly categorized without any manual effort.

## Features

- Automatically detects the default browser on your system.
- Monitors the Desktop and Downloads folders.
- Detects if a browser is running and starts to organize files in the background.
- Organizes downloaded files into folders based on their types (e.g., PDF, images, HTML, etc.).
- Works on Windows, macOS, and Linux platforms.
- Minimal setup required.
- Lightweight and efficient.

## Requirements

- Python 3.x
- watchdog
- psutil

## Installation

1. Clone or download the repository to your local machine.

2. Install the required dependencies using pip:
  ```
  pip install -r requirements.txt
  ```

3. Run the script:

- For Windows:
  - Double-click the `windows.bat` file.

- For macOS and Linux:
  - Execute the following command in your terminal:

    ```
    sh unix.sh
    ```

## Usage

- Once the script is running, it will continuously monitor the Downloads and Desktop directory in the background.
- You can customize the file organization logic by modifying the main Python script (`script.py`).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## Acknowledgements

- [psutil](https://github.com/giampaolo/psutil) - Cross-platform library for retrieving information on running processes and system utilization in Python.

## Support

If you encounter any issues or have questions, please feel free to [open an issue](https://github.com/SpecialSpicy/Downloaded-File-Organizer/issues/new).
