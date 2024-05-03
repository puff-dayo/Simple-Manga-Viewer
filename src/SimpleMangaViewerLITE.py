import os
import sys
import tempfile

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QKeyEvent, QWheelEvent, QPalette, QColor, QIcon, QImage
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QColorDialog, QWidget, \
    QRadioButton, QVBoxLayout, QDialog
from pypdf import PdfReader


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Manga Viewer LITE")
        self.setWindowIcon(QIcon("icon-512.png"))
        self.devicePixelRatio = self.devicePixelRatioF()
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        self.temp_dir_path = temp_dir.name

        self.reading_direction_left_to_right = True
        # True: left-to-right, False: right-to-left
        self.scaling_method = Qt.SmoothTransformation
        self.is_denoise_on = None
        self.is_sharpen_on = None
        self.last_image = ""

        # ---------- MAIN LAYOUT ---------- #

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # BUTTON to open folder
        self.button_open = QPushButton("Open Folder", self)
        self.button_open.clicked.connect(self.open_folder)
        self.button_open.setGeometry(10, 10, 120, 40)

        # BUTTON to open PDF file
        self.button_open_pdf = QPushButton("Open PDF", self)
        self.button_open_pdf.clicked.connect(self.open_pdf)
        self.button_open_pdf.setGeometry(10, 60, 100, 40)

        # BUTTON to change background color
        self.button_color = QPushButton("Change Background Color", self)
        self.button_color.clicked.connect(self.change_background_color)
        self.button_color.setGeometry(140, 10, 200, 40)

        # BUTTON to toggle reading direction button
        self.button_toggle = QPushButton("Toggle Reading Direction", self)
        self.button_toggle.clicked.connect(self.toggle_reading_direction)
        self.button_toggle.setGeometry(350, 10, 200, 40)

        # BUTTON to open settings panel
        self.button_settings = QPushButton("Settings", self)
        self.button_settings.clicked.connect(self.open_settings)
        self.button_settings.setGeometry(560, 10, 100, 40)

        # LABEL to display images
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        # LABEL to display notification
        self.notification_label = QLabel("Long press 2 seconds to hide/show buttons.", self)
        self.notification_label.setAlignment(Qt.AlignCenter)
        self.notification_label.setStyleSheet("background-color: rgba(0, 0, 0, 128); color: white;")
        self.notification_label.setGeometry(10, 60, 380, 20)
        self.notification_label.hide()

        # ---------- MAIN LAYOUT ---------- #

        # List of image paths
        self.images = []
        self.current_image_index = 0

        # Timer for detecting long press
        self.long_press_timer = QTimer()
        self.long_press_timer.setSingleShot(True)
        self.long_press_timer.setInterval(2000)  # ms
        self.long_press_timer.timeout.connect(self.toggle_button_visibility)

        self.raise_all_button()

    def done_opening(self):
        self.button_open.hide()
        self.button_open_pdf.hide()
        self.button_color.hide()
        self.button_toggle.hide()
        self.button_settings.hide()

        self.show_notification()

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            import os
            valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
            self.images = [os.path.join(folder, f) for f in sorted(os.listdir(folder)) if
                           f.lower().endswith(valid_extensions)]
            self.current_image_index = 0
            self.display_image()

            self.done_opening()

    def open_pdf(self):
        pdf_file, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if pdf_file:
            self.images = []
            self.extract_images_from_pdf(pdf_file)
            self.current_image_index = 0
            self.display_image()

            self.done_opening()

    def extract_images_from_pdf(self, pdf_file=None):
        cleanup_temp_dir()

        if pdf_file:
            pdf_files = [pdf_file]
        else:
            pdf_files = [f for f in self.images if f.lower().endswith('.pdf')]

        for pdf_file in pdf_files:
            with open(pdf_file, 'rb') as f:
                pdf_reader = PdfReader(f)
                for page_num, page in enumerate(pdf_reader.pages):
                    count = 0
                    for image_file_object in page.images:
                        image_path = os.path.join(self.temp_dir_path, os.path.basename(pdf_file),
                                                  f"page_{page_num}_{count}_{image_file_object.name}")
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)
                        with open(image_path, 'wb') as fp:
                            fp.write(image_file_object.data)
                            self.images.append(image_path)
                            count += 1

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.centralWidget().setStyleSheet(f"background-color: {color.name()};")

    def display_image(self):
        if self.images:
            image_path = self.images[self.current_image_index]
            pixmap = QPixmap(self.images[self.current_image_index])

            scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, self.scaling_method)
            self.label.setPixmap(scaled_pixmap)
            self.label.setGeometry((self.width() - scaled_pixmap.width()) // 2,
                                   (self.height() - scaled_pixmap.height()) // 2,
                                   scaled_pixmap.width(),
                                   scaled_pixmap.height())

    def toggle_reading_direction(self):
        self.reading_direction_left_to_right = not self.reading_direction_left_to_right
        self.show_notification(notif="Reading direction changed.")

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            selected_method = dialog.get_selected_method()
            print(selected_method)
            if selected_method == 1:
                self.scaling_method = Qt.SmoothTransformation
                self.is_denoise_on = True
                self.is_sharpen_on = False
            elif selected_method == 2:
                self.scaling_method = Qt.SmoothTransformation
                self.is_sharpen_on = True
                self.is_denoise_on = False
            elif selected_method == 3:
                self.scaling_method = Qt.SmoothTransformation
                self.is_denoise_on = True
                self.is_sharpen_on = True
            else:
                self.scaling_method = selected_method
                self.is_sharpen_on = False
                self.is_sharpen_on = False
            self.display_image()

    def wheelEvent(self, event: QWheelEvent):
        if self.images:
            numDegrees = event.angleDelta().y() / 8
            numSteps = numDegrees / 15
            if numSteps > 0:
                increment = -1 if self.reading_direction_left_to_right else 1
            else:
                increment = 1 if self.reading_direction_left_to_right else -1
            self.current_image_index = max(0, min(self.current_image_index + increment, len(self.images) - 1))
            self.display_image()

    def keyPressEvent(self, event: QKeyEvent):
        if self.images:
            increment = -1 if self.reading_direction_left_to_right else 1
            if event.key() in (Qt.Key_Left, Qt.Key_Up):
                self.current_image_index = max(self.current_image_index + increment, 0)
            elif event.key() in (Qt.Key_Right, Qt.Key_Down):
                self.current_image_index = min(self.current_image_index - increment, len(self.images) - 1)
            self.display_image()

    def resizeEvent(self, event):
        self.display_image()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        self.long_press_timer.start()
        if self.images:
            x = event.position().x()
            if self.reading_direction_left_to_right:
                if x < self.width() / 2:
                    self.current_image_index = max(self.current_image_index - 1, 0)
                else:
                    self.current_image_index = min(self.current_image_index + 1, len(self.images) - 1)
            else:
                if x < self.width() / 2:
                    self.current_image_index = min(self.current_image_index + 1, len(self.images) - 1)
                else:
                    self.current_image_index = max(self.current_image_index - 1, 0)
            self.display_image()

    def mouseReleaseEvent(self, event):
        self.long_press_timer.stop()

    def toggle_button_visibility(self):
        visibility = not self.button_open.isVisible()
        self.button_open.setVisible(visibility)
        self.button_open_pdf.setVisible(visibility)
        self.button_color.setVisible(visibility)
        self.button_toggle.setVisible(visibility)
        self.button_settings.setVisible(visibility)

        if visibility:
            self.raise_all_button()

        self.show_notification()

    def raise_all_button(self):
        self.button_open.raise_()
        self.button_open_pdf.raise_()
        self.button_color.raise_()
        self.button_toggle.raise_()
        self.button_settings.raise_()

    def show_notification(self, notif="Long press 2 seconds to hide/show buttons."):
        self.notification_label.setText(notif)
        self.notification_label.show()
        QTimer.singleShot(3000, self.notification_label.hide)



class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.layout = QVBoxLayout(self)

        self.radio_smooth = QRadioButton("Smooth Transformation (Default)")
        self.radio_linear = QRadioButton("Fast Transformation (Linear)")

        self.layout.addWidget(self.radio_linear)
        self.layout.addWidget(self.radio_smooth)

        self.radio_smooth.setChecked(True)

        self.button_ok = QPushButton("OK", self)
        self.button_ok.clicked.connect(self.accept)
        self.layout.addWidget(self.button_ok)

    def get_selected_method(self):
        if self.radio_smooth.isChecked():
            return Qt.SmoothTransformation
        if self.radio_linear.isChecked():
            return Qt.FastTransformation


temp_dir = tempfile.TemporaryDirectory()


def cleanup_temp_dir():
    try:
        print("Attempting to clean up the temporary directory.")
        temp_dir.cleanup()
        print("Temporary directory cleaned up.")
    except Exception as e:
        print(f"Failed to clean up temporary directory: {e}")


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        app.setPalette(QPalette(QColor('#444444')))
        app.setAttribute(Qt.AA_EnableHighDpiScaling)
        app.aboutToQuit.connect(cleanup_temp_dir)
        viewer = ImageViewer()
        viewer.showMaximized()
        sys.exit(app.exec())
    except Exception as e:
        cleanup_temp_dir()
        print(f"An error occurred: {e}")
        sys.exit(1)
