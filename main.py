from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys

if __name__ == "__main__":
    # Create the application object
    app = QApplication(sys.argv)
    
    # Create the main window instance
    window = MainWindow()
    
    # Start the application's event loop
    sys.exit(app.exec())
