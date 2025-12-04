#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

TARGET_DIR="$1"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: '$TARGET_DIR' is not a valid directory."
    exit 1
fi

FOLDERS=$(find "$TARGET_DIR" -type d -name "*-student*" 2>/dev/null)
COUNT=0

if [ -z "$FOLDERS" ]; then
    echo "No folders found containing '-student'."
    exit 0
fi

while IFS= read -r folder; do
    rm -rf "$folder"
    COUNT=$((COUNT + 1))
done <<< "$FOLDERS"

echo "Deleted $COUNT folder(s) containing '-student'."
