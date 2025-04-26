#!/bin/bash

while true; do
    /home/ubuntu/venv/bin/python3.12 /home/ubuntu/RelocateJobs/scraper/check_job.py
    echo "Script crashed with exit code $?. Restarting in 5 seconds..."
    sleep 5
done