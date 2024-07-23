#!/bin/bash

# Define paths
BASE_DIR="/home/$USER/.hp-rgb"
REPO_URL="https://github.com/kaankutan/hp-laptop-rgb-controller.git"
VENV_PATH="$BASE_DIR/venv"
RUN_SCRIPT_PATH="$BASE_DIR/run.sh"
DESKTOP_ENTRY_PATH="/home/$USER/.local/share/applications/hp_rgb_controller.desktop"

# Create necessary directories
mkdir -p "$(dirname "$DESKTOP_ENTRY_PATH")"

# Clone the repository
if [ -d "$BASE_DIR" ]; then
    echo "Directory $BASE_DIR already exists. Pulling latest changes."
    cd "$BASE_DIR" && git pull
else
    git clone "$REPO_URL" "$BASE_DIR"
fi

# Setup virtual environment
python3 -m venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"
pip install --upgrade pip

# Install dependencies from requirements.txt if it exists
if [ -f "$BASE_DIR/requirements.txt" ]; then
    pip install -r "$BASE_DIR/requirements.txt"
fi

# Create the shell script
echo '#!/bin/bash

VENV_PATH="/home/$USER/.hp-rgb/venv"
SCRIPT_PATH="/home/$USER/.hp-rgb/main.py"
source "$VENV_PATH/bin/activate"
python  "$SCRIPT_PATH"' > "$RUN_SCRIPT_PATH"
chmod +x "$RUN_SCRIPT_PATH"

# Create the .desktop entry
echo "[Desktop Entry]
Name=HP RGB Controller
Comment=RGB Controller for HP Laptops
Exec=pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY $RUN_SCRIPT_PATH
Icon=$BASE_DIR/assets/hp_logo.png
Terminal=false
Type=Application" > "$DESKTOP_ENTRY_PATH"

echo "Installation complete! You can now find the HP RGB Controller in your application menu."
