#!/bin/bash
source /home/p7/miniconda3/bin/activate base  # Adjust path to Conda and environment name
exec python /home/p7/timeserver/sntp_server/serverntp.py
