#!/bin/bash

cd ..
sudo chmod +rwx *.py
pip install -r requirements.txt
python3 gui.py
echo "Setup script finished! Press Enter to continue..."
read -p ""