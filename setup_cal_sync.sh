#!/bin/bash

# Usage: ./setup_calendar_sync.sh [frequency_per_day]
# Example: ./setup_calendar_sync.sh 4 (runs every 6 hours)

# Check if the parameter is passed
if [ -z "$1" ]; then
  echo "Error: Frequency per day is required. Example: ./setup_calendar_sync.sh 4"
  exit 1
fi

# Set variables
FREQUENCY_PER_DAY=$1
PROJECT_DIR=$(pwd)  # Assumes the script is run from the project directory
VENV_DIR="$PROJECT_DIR/.venv"
RUN_SCRIPT="$PROJECT_DIR/run_cal_sync.sh"
LOG_FILE="$PROJECT_DIR/cal_sync.log"

# Step 1: Check if the Python virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv "$VENV_DIR"
  echo "Virtual environment created at $VENV_DIR"
else
  echo "Virtual environment already exists. Skipping creation."
fi

# Step 2: Activate the virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
deactivate
echo "Dependencies installed."

# Step 3: Calculate the frequency in minutes
FREQUENCY_MINUTES=$((1440 / FREQUENCY_PER_DAY))


# Step 4: Remove any existing cron job for this script
CRONTAB=$(crontab -l 2>/dev/null)
NEW_CRONTAB=$(echo "$CRONTAB" | grep -v "$RUN_SCRIPT")

# Step 5: Add the new cron job to the crontab
NEW_CRONTAB="$NEW_CRONTAB"$'\n'"*/$FREQUENCY_MINUTES * * * * $RUN_SCRIPT >> $LOG_FILE 2>&1"

# Step 6: Update the crontab
echo "$NEW_CRONTAB" | crontab -

echo "Crontab entry updated to run every $FREQUENCY_MINUTES minutes."
echo "Setup complete."