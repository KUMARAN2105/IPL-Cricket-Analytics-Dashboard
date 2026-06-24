# Create a virtual environment and install Python dependencies for this project.
# Run this from the repository root in PowerShell.

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
