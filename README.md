# cal-sync
A Python script using PyObjC to synchronize macOS Calendar events between two accounts.

## Overview
**cal-sync** is designed for a specific scenario where you need to sync a calendar from one account to another within the macOS Calendar app. This is particularly useful when you can access one account on your laptop but not on your phone, and you want to have the events available on both devices.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Logging](#logging)
- [Uninstall](#uninstall)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)
- [Additional Information](#additional-information)

## Features

- Synchronize events from a source calendar to a destination calendar.
- Automate synchronization at specified intervals.
- Simple configuration using a YAML file.
- Detailed logging of synchronization activities and any issues.

## Installation
- Python 3.x is required to run the script.

Clone the repository:

```bash
git clone https://github.com/loopsmark/cal-sync.git
cd cal-sync
```
The setup_cal_sync.sh script handles the installation of required Python packages and sets up the synchronization schedule.

## Configuration
Before running the script, update the config.yaml file with your calendar preferences.

## Usage
Run the setup_cal_sync.sh script with the desired synchronization frequency per day:
```bash
./setup_cal_sync.sh <frequency_per_day>
```
For example, to run the sync each minute:
```bash
./setup_cal_sync.sh 1440
```

This script will:
- Create a python virtual environment in this repo
- Install necessary Python packages in a virtual environment from requirements.txt using pip.
- Add an entry to your crontab to automate synchronization.

**Note**: You can run the script again to just change the frequency

**Important**: The frequency parameter specifies how many times per day the synchronization will occur.

## Logging
All synchronization activities are logged in cal_sync.log, including:
- Details of events that have been copied or updated.
- Any errors or issues encountered during synchronization.

## Uninstall
Remove the entry from contrab with `crontab -e` and delete this folder.

## License
This project is licensed under the GNU General Public License v3.0.

## Contributing
Contributions are welcome! Please:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Submit a pull request with a detailed description of your changes.

## Contact
For support or to report issues, please use the GitHub Issues page.

## Additional information
- Dependencies: The script requires Python packages specified in requirements.txt, namely pyobjc and pyyaml.
- Platform Compatibility: This script is designed for macOS, leveraging PyObjC to interact with the Calendar app.
- Limitations: Currently, the script does not support manual synchronization without setting up the cron job.
- Future Plans: Open to ideas for additional features or improvements.