# File Organizer

Browser File Organizer is a Python script designed to monitor the default browser on your system and organize downloaded files into folders based on their types. It works seamlessly in the background, ensuring your downloads are neatly categorized without any manual effort.

## Features

### Automatic File Organization
- Automatically organizes files in the Downloads folder and Desktop into categorized folders based on their file types.
- Supports various file types including PDFs, images, HTML files, text files, spreadsheets, presentations, audio files, video files, fonts, archives, executables, scripts, Word documents, and more.
- Handles duplicates by appending a suffix to the filename to ensure no files are overwritten.
- Provides user-friendly messages to indicate the start and stop of the file organizer, as well as error messages for missing folders and permission issues.

### Browser Detection and Auto-Start
- Detects when a browser process is running.
- Starts to organize when a browser is detected, allowing seamless organization of downloaded files while browsing.


## Requirements

- Python 3.x
- watchdog
- psutil
- errno

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
