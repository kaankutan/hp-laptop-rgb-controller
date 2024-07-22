from PyQt5.QtCore import QThread, pyqtSignal
from effects import breathing, spectrum
import time

class KeyboardThread(QThread):
    # Signal to notify about color changes
    changedColor = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Initialize color, effect, and state
        self._current_color = self.getInitialColor()
        self._previous_color = self._current_color
        self._effect = 'static'
        self.speed = 50
        self._running = True
        self._stop_requested = False
    
    @property
    def current_color(self):
        return self._current_color
    
    @current_color.setter
    def current_color(self, value):
        # Request to stop if color changes
        self._stop_requested = value != self._previous_color
        self._previous_color = self._current_color
        self._current_color = value

    @property
    def effect(self):
        return self._effect
    
    @effect.setter
    def effect(self, value):
        # Request to stop if effect changes
        self._stop_requested = value != self._effect
        self._effect = value

    def setKeyboardColor(self, color):
        # Emit signal to update the color and write to device file
        self.changedColor.emit(color)
        try:
            with open("/sys/devices/platform/hp-wmi/rgb_zones/zone00", "w") as f:
                f.write(color[1:])  # Remove '#' from color string
        except Exception as e:
            print(f"Error setting keyboard color: {e}")

    def run(self):
        # Main loop for thread execution
        while self._running:
            if self.effect == 'breathing':
                self.runEffect(self.getBreathingColors)
            elif self.effect == 'spectrum':
                self.runEffect(self.getSpectrumColors)
            elif self.effect == 'static' and self._current_color != self._previous_color:
                self.setKeyboardColor(self._current_color)
            else:
                time.sleep(0.1)
        self.setKeyboardColor(self.current_color)  # Set final color when stopping

    def runEffect(self, get_colors_func):
        # Run the specified effect
        colors = get_colors_func()
        for color in colors:
            if self._stop_requested:
                self._stop_requested = False
                break
            self.setKeyboardColor(color)
            sleep_time = max(0.01, 1.0 / self.speed)  # Ensure sleep time is not too short
            time.sleep(sleep_time)

    def getBreathingColors(self):
        # Generate breathing effect colors
        return breathing(self.current_color, 0.01)

    def getSpectrumColors(self):
        # Generate spectrum effect colors
        return spectrum(200)

    def stop(self):
        # Stop the thread and request to stop effects
        self._running = False
        self._stop_requested = True
    
    def getInitialColor(self):
        # Read the initial color from the device file
        with open("/sys/devices/platform/hp-wmi/rgb_zones/zone00", "r") as f:
            # Format is red: 255, green: 0, blue: 255
            colors = str(f.read()).split(", ")
            red = int(colors[0].split(": ")[1])
            green = int(colors[1].split(": ")[1])
            blue = int(colors[2].split(": ")[1])
            return f"#{red:02x}{green:02x}{blue:02x}"  # Convert to hex color format
