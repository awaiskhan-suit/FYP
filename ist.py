import sys
import serial
import time
import cv2

from cvzone.HandTrackingModule import HandDetector

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import *


# ================= VIDEO THREAD =================
class VideoThread(QThread):
    frame_ready = pyqtSignal(object)
    distance_ready = pyqtSignal(int)

    def __init__(self, get_serial_callback):
        super().__init__()
        self.running = True
        self.get_serial = get_serial_callback
        self.prev_length = 0

    def run(self):
        # ✅ SAFE CAMERA INIT (inside thread)
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not cap.isOpened():
            print("Camera failed")
            return

        # ✅ IMPORT + CREATE INSIDE THREAD (CRITICAL FIX)
        from cvzone.HandTrackingModule import HandDetector
        detector = HandDetector(detectionCon=0.7, maxHands=1)

        while self.running:
            ret, frame = cap.read()

            if not ret:
                print("Frame failed")
                break

            # ✅ flip for natural interaction
            frame = cv2.flip(frame, 1)

            try:
                hands, frame = detector.findHands(frame)

                if hands:
                    lmList = hands[0]['lmList']

                    # 👉 STABLE DISTANCE (index ↔ middle)
                    length, _, frame = detector.findDistance(
                        lmList[8], lmList[12], frame

                    )

                    # ===== NORMALIZE =====
                    length = int((length // 10) * 10 - 30)
                    length = max(0, min(200, length))

                    # ===== SMOOTH =====
                    alpha = 0.7
                    length = int(alpha * self.prev_length + (1 - alpha) * length)
                    self.prev_length = length

                    # ===== SEND SERIAL SAFELY =====
                    ser = self.get_serial()
                    if ser and ser.is_open:
                        try:
                            ser.write(f"DIST:{length}\n".encode())
                        except:
                            pass

                    self.distance_ready.emit(length)

            except Exception as e:
                print("Detection error:", e)

            # ✅ SEND FRAME
            self.frame_ready.emit(frame)

            # ✅ FPS LIMIT (VERY IMPORTANT)
            self.msleep(30)

        cap.release()

    def stop(self):
        self.running = False
        self.wait()


# ================= GAUGE =================
class SimpleCircularGauge(QWidget):
    def __init__(self, max_value=200):
        super().__init__()
        self.value = 0
        self.max_value = max_value
        self.setMinimumSize(170, 170)

    def setValue(self, value):
        self.value = max(0, min(self.max_value, value))
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        r = min(w, h) // 2 - 10

        p.setPen(QPen(QColor(60, 60, 60), 10))
        p.drawArc(cx - r, cy - r, r * 2, r * 2, 315 * 16, 270 * 16)

        angle = int((self.value / self.max_value) * 270)

        if self.value < 60:
            color = QColor(0, 255, 140)
        elif self.value < 140:
            color = QColor(0, 200, 255)
        else:
            color = QColor(255, 60, 60)

        for i in range(6, 0, -1):
            glow = QColor(color)
            glow.setAlpha(25)
            p.setPen(QPen(glow, 2 + i))
            p.drawArc(cx - r, cy - r, r * 2, r * 2, 225 * 16, -angle * 16)

        p.setPen(QPen(color, 10, Qt.SolidLine, Qt.RoundCap))
        p.drawArc(cx - r, cy - r, r * 2, r * 2, 225 * 16, -angle * 16)

        inner_r = int(r * 0.55)

        p.setPen(Qt.NoPen)
        p.setBrush(QColor(55, 55, 55))
        p.drawEllipse(cx - inner_r, cy - inner_r, inner_r * 2, inner_r * 2)

        p.setPen(QPen(QColor(90, 90, 90), 2))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(cx - inner_r, cy - inner_r, inner_r * 2, inner_r * 2)

        p.setPen(Qt.white)
        p.setFont(QFont("Segoe UI", 18, QFont.Bold))
        p.drawText(cx - inner_r, cy - inner_r, inner_r * 2, inner_r * 2,
                   Qt.AlignCenter, str(self.value))


class GaugeWithLabel(QWidget):
    def __init__(self, title):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            color:#87CEFA;
            font-weight:bold;
            font-size:16px;
        """)

        self.gauge = SimpleCircularGauge()

        layout.addWidget(label)
        layout.addWidget(self.gauge)
        self.setLayout(layout)

    def setValue(self, v):
        self.gauge.setValue(v)


# ================= SERIAL THREAD =================
class ArduinoThread(QThread):
    sensors_data = pyqtSignal(list)
    connected = pyqtSignal(bool)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.serial = None
        self.running = True

    def run(self):
        try:
            self.serial = serial.Serial(self.port, 9600, timeout=1)
            time.sleep(2)
            self.connected.emit(True)

            while self.running:
                if self.serial.in_waiting:
                    line = self.serial.readline().decode().strip()

                    if line.startswith("SENSORS:"):
                        vals = [float(x) for x in line.split(":")[1].split(",")]
                        self.sensors_data.emit(vals)

        except:
            self.connected.emit(False)

    def stop(self):
        self.running = False
        if self.serial:
            self.serial.close()
        self.wait()


# ================= MAIN UI =================
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.arduino_thread = None
        self.video_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Smart Arduino Dashboard")
        self.setStyleSheet("background-color:#121212;")

        main = QVBoxLayout()

        # VIDEO
        self.video = QLabel("Camera Offline")
        self.video.setFixedSize(340, 250)
        self.video.setAlignment(Qt.AlignCenter)
        self.video.setStyleSheet("""
            background-color: #444;
            color: #aaa;
            border-radius:10px;
        """)
        main.addWidget(self.video, alignment=Qt.AlignCenter)

        # GAUGES
        g = QHBoxLayout()
        self.g1 = GaugeWithLabel("Voltage")
        self.g2 = GaugeWithLabel("Current")
        self.g3 = GaugeWithLabel("Power")
        self.g4 = GaugeWithLabel("Hand Distance")

        for x in [self.g1, self.g2, self.g3, self.g4]:
            g.addWidget(x)

        main.addLayout(g)

        # ===== LED CONTROL PANEL (RESTORED) =====
        box = QGroupBox("LED Control")
        box.setStyleSheet("color:white;")
        grid = QGridLayout()

        for i in range(3):
            on = QPushButton(f"LED{i + 1} ON")
            off = QPushButton(f"LED{i + 1} OFF")

            on.setFixedHeight(45)
            off.setFixedHeight(45)

            on.setStyleSheet("""
                background:#27ae60;
                color:white;
                border-radius:8px;
                font-size:14px;
                font-weight:bold;
            """)

            off.setStyleSheet("""
                background:#c0392b;
                color:white;
                border-radius:8px;
                font-size:14px;
                font-weight:bold;
            """)

            on.clicked.connect(lambda _, n=i + 1: self.send_led(n, True))
            off.clicked.connect(lambda _, n=i + 1: self.send_led(n, False))

            grid.addWidget(on, i, 0)
            grid.addWidget(off, i, 1)

        box.setLayout(grid)
        main.addWidget(box)

        # CONNECT BUTTON
        self.btn = QPushButton("CONNECT ARDUINO")
        self.btn.setStyleSheet("""
            background-color: #f1c40f;
            color: black;
            font-weight: bold;
            padding: 10px;
            border-radius: 8px;
        """)
        self.btn.clicked.connect(self.connect_arduino)
        main.addWidget(self.btn)

        self.setLayout(main)

    def connect_arduino(self):
        port = "COM4"
        self.arduino_thread = ArduinoThread(port)
        self.arduino_thread.connected.connect(self.on_connection)
        self.arduino_thread.sensors_data.connect(self.update_sensors)
        self.arduino_thread.start()

    def on_connection(self, status):
        if status:
            self.btn.setText("CONNECTED")
            self.btn.setStyleSheet("background:#2ecc71; color:white;")

            self.video_thread = VideoThread(lambda: self.arduino_thread.serial)
            self.video_thread.frame_ready.connect(self.update_video)
            self.video_thread.distance_ready.connect(self.update_distance)
            self.video_thread.start()
        else:
            self.video.setText("Connection Failed")

    def send_led(self, num, state):
        if self.arduino_thread and self.arduino_thread.serial:
            cmd = f"LED{num}_{'ON' if state else 'OFF'}\n"
            self.arduino_thread.serial.write(cmd.encode())

    def update_video(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.video.setPixmap(QPixmap.fromImage(qt))

    def update_distance(self, val):
        self.g4.setValue(val)

    def update_sensors(self, vals):
        if len(vals) >= 3:
            self.g1.setValue(vals[0])
            self.g2.setValue(vals[1])
            self.g3.setValue(vals[2])

    def closeEvent(self, e):
        if self.video_thread:
            self.video_thread.stop()
        if self.arduino_thread:
            self.arduino_thread.stop()
        e.accept()


# ================= RUN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Dashboard()
    w.show()
    sys.exit(app.exec_())

