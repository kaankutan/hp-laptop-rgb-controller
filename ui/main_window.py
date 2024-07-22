from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QSlider,
    QSystemTrayIcon,
    QMenu,
    QApplication
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from threads import KeyboardThread
from pyqt_color_picker import ColorPickerWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the keyboard thread and start it
        self.keyboard_thread = KeyboardThread()
        self.keyboard_thread.changedColor.connect(self.updateKeyboard)
        self.keyboard_thread.start()
        
        # Initialize the color picker widget
        self.color_picker = ColorPickerWidget(orientation='horizontal')
        self.color_picker.colorChanged.connect(self.colorPickerHandler)

        # Variables to keep track of selected buttons
        self.selected_color_button = None
        self.selected_effect_button = None

        # Set up the system tray icon
        self.initTrayIcon()

        # Set up the UI
        self.initUI()

    def initTrayIcon(self):
        # Create a system tray icon for the application
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("assets/hp_logo.png"))
        self.tray_icon.setToolTip("HP Laptop RGB Control")
        # Right-clicking will show the tray icon menu
        self.tray_icon.setContextMenu(self.createTrayMenu())

        self.tray_icon.activated.connect(lambda reason: self.show() if reason == QSystemTrayIcon.ActivationReason.DoubleClick else None)
        self.tray_icon.show()

    def createTrayMenu(self):
        # Create a context menu for the system tray icon
        tray_menu = QMenu()
        # Add an option to show the main window
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        # Add an option to exit the application
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(self.quit)
        return tray_menu
    
    def initUI(self):
        self.setWindowTitle("HP Laptop RGB Control")
        self.setWindowIcon(QIcon("assets/hp_logo.png"))

        # Create and configure the keyboard image label
        self.keyboard_image = QLabel(self)
        self.keyboard_image.setPixmap(QPixmap("assets/keyboard.png"))
        self.keyboard_image.setStyleSheet(f"background-color: {self.keyboard_thread.current_color}; border-radius: 10px;")
        self.keyboard_image.setScaledContents(True)
        self.keyboard_image.setFixedSize(580, 248)

        # Create the layout for color buttons
        self.colors_layout = QHBoxLayout()
        self.color_buttons = []

        # List of color options
        colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffffff', '#000000']

        # Create and add color buttons to the layout
        for color in colors:
            color_button = QLabel(self)
            color_button.setFixedSize(48, 48)
            color_button.setStyleSheet(f"background-color: {color}; border-radius: 24px; border: 2px solid transparent;")
            color_button.setCursor(Qt.CursorShape.PointingHandCursor)
            color_button.mousePressEvent = lambda event, color=color, button=color_button: self.onColorButtonClick(color, button)
            self.colors_layout.addWidget(color_button)
            self.color_buttons.append(color_button)
        
        # Create and add the color picker button to the layout
        self.color_selector_button = QLabel(self)
        self.color_selector_button.setFixedSize(48, 48)
        self.color_selector_button.setScaledContents(True)
        self.color_selector_button.setPixmap(QPixmap("assets/color_button.png"))
        self.color_selector_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.color_selector_button.mousePressEvent = lambda event: self.color_picker.show()
        self.colors_layout.addWidget(self.color_selector_button)
        self.color_buttons.append(self.color_selector_button)

        # Create the layout for effect buttons
        self.effect_layout = QHBoxLayout()
        self.effect_buttons = []

        # List of effect options
        effects = ['static', 'breathing', 'spectrum']

        # Create and add effect buttons to the layout
        for effect in effects:
            effect_button = QLabel(self)
            effect_button.setText(effect.capitalize())
            effect_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
            effect_button.setFixedSize(80, 32)
            effect_button.setStyleSheet(f"background-color: #101010; color: #ffffff; border: 2px solid transparent; border-radius: 8px; font-size: 14px;")
            effect_button.setCursor(Qt.CursorShape.PointingHandCursor)
            effect_button.mousePressEvent = lambda event, effect=effect, button=effect_button: self.onEffectButtonClick(effect, button)
            self.effect_layout.addWidget(effect_button)
            self.effect_buttons.append(effect_button)

        # Highlight the first effect button by default
        self.effect_buttons[0].setStyleSheet(self.effect_buttons[0].styleSheet().replace('border: 2px solid transparent;', 'border: 2px solid #ffffff;'))
        self.selected_effect_button = self.effect_buttons[0]

        # Create and configure the speed slider
        self.speed_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.setTickInterval(10)
        self.speed_slider.valueChanged.connect(self.onSpeedChange)
        self.speed_slider.hide()  # Hide by default

        # Create and configure the speed label
        self.speed_label = QLabel("Speed", self)
        self.speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.speed_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        self.speed_label.hide()  # Hide by default

        # Layout for speed slider and label
        self.speed_layout = QHBoxLayout()
        self.speed_layout.addWidget(self.speed_label)
        self.speed_layout.addWidget(self.speed_slider)

        # Main layout to hold everything
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.keyboard_image)
        self.main_layout.addLayout(self.colors_layout)
        self.main_layout.addLayout(self.effect_layout)
        self.main_layout.addLayout(self.speed_layout)

        # Create and configure the central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #282828;")
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.setFixedSize(600, 450)
        self.show()

    def onColorButtonClick(self, color, button):
        # Update the color on the keyboard thread and highlight the selected color button
        self.keyboard_thread.current_color = color
        if self.selected_color_button:
            self.selected_color_button.setStyleSheet(self.selected_color_button.styleSheet().replace('border: 2px solid #ffffff;', 'border: 2px solid transparent;'))
        button.setStyleSheet(button.styleSheet().replace('border: 2px solid transparent;', 'border: 2px solid #ffffff;'))
        self.selected_color_button = button

    def onEffectButtonClick(self, effect, button):
        # Update the effect on the keyboard thread and adjust the visibility of UI elements
        self.keyboard_thread.effect = effect
        if effect == 'spectrum':
            for color_button in self.color_buttons:
                color_button.hide()
        else:
            for color_button in self.color_buttons:
                color_button.show()
        if effect == 'static':
            self.speed_slider.hide()
            self.speed_label.hide()
        else:
            self.speed_slider.show()
            self.speed_label.show()
        if self.selected_effect_button:
            self.selected_effect_button.setStyleSheet(self.selected_effect_button.styleSheet().replace('border: 2px solid #ffffff;', 'border: 2px solid transparent;'))
        button.setStyleSheet(button.styleSheet().replace('border: 2px solid transparent;', 'border: 2px solid #ffffff;'))
        self.selected_effect_button = button
    
    def colorPickerHandler(self, color):
        # Update the color on the keyboard thread from the color picker
        self.keyboard_thread.current_color = color.name()
        if self.selected_color_button:
            self.selected_color_button.setStyleSheet(self.selected_color_button.styleSheet().replace('border: 2px solid #ffffff;', 'border: 2px solid transparent;'))

    def onSpeedChange(self):
        # Update the speed on the keyboard thread from the slider value
        self.keyboard_thread.speed = self.speed_slider.value()

    def updateKeyboard(self, color):
        # Update the keyboard image's background color
        self.keyboard_image.setStyleSheet(f"background-color: {color}; border-radius: 10px;")

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def quit(self):
        self.keyboard_thread.stop()
        self.keyboard_thread.wait()
        self.tray_icon.hide()
        QApplication.quit()
