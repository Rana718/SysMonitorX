from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDial
from PyQt5.QtCore import QTimer, Qt
import sys
import json
from info.cpu import get_cpu_info
from info.ram import get_ram_info
from info.gpu import get_gpu_info

class AnalogMeter(QWidget):
    def __init__(self, label_text, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.dial = QDial()
        self.dial.setMinimum(0)
        self.dial.setMaximum(100)
        self.dial.setNotchesVisible(True)
        layout.addWidget(self.dial)
        
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.value_label = QLabel("0%")
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
        
        self.setLayout(layout)

    def setValue(self, value):
        self.dial.setValue(int(value))
        self.value_label.setText(f"{int(value)}%")

class MonitoringApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SysMonitorX')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.cpu_name_label = QLabel()
        layout.addWidget(self.cpu_name_label)

        self.cpu_usage_meter = AnalogMeter("CPU Usage")
        layout.addWidget(self.cpu_usage_meter)

        self.cpu_temp_label = QLabel()
        layout.addWidget(self.cpu_temp_label)

        self.ram_usage_label = QLabel()
        layout.addWidget(self.ram_usage_label)

        self.gpu_usage_meter = AnalogMeter("GPU Usage")
        layout.addWidget(self.gpu_usage_meter)

        self.gpu_info_label = QLabel()
        layout.addWidget(self.gpu_info_label)

        self.setLayout(layout)

    def update_monitoring_data(self, cpu_name, cpu_usage, cpu_temps, ram_info, gpu_info):
        self.cpu_name_label.setText(f"CPU Name: {cpu_name}")
        self.cpu_usage_meter.setValue(cpu_usage)
        if cpu_temps:
            if isinstance(cpu_temps, list):
                temps_str = "\n".join([f"CPU Temperature {i+1}: {temp:.2f}°C" for i, temp in enumerate(cpu_temps)])
            elif isinstance(cpu_temps, dict):
                temps_str = "\n".join([f"{key}: {value:.2f}°C" for key, value in cpu_temps.items()])
            else:
                temps_str = "CPU Temperature: Not available"
            self.cpu_temp_label.setText(temps_str)
        else:
            self.cpu_temp_label.setText("CPU Temperature: Not available")

        self.ram_usage_label.setText(f"RAM Usage: {ram_info.percent}%")

        if gpu_info:
            self.gpu_usage_meter.setValue(gpu_info[0]['load'])
            gpu_str = "\n\n".join([f"GPU {i+1}:\nName: {gpu['name']}\nLoad: {gpu['load']:.2f}%\nTemperature: {gpu['temperature']:.2f}°C" for i, gpu in enumerate(gpu_info)])
            self.gpu_info_label.setText(gpu_str)
        else:
            self.gpu_info_label.setText("GPU Info: Not available")

def save_settings(settings_dict):
    with open('settings.json', 'w') as f:
        json.dump(settings_dict, f)

def load_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def update_gui(monitor):
    cpu_name, cpu_usage, cpu_temps = get_cpu_info()
    ram_info = get_ram_info()
    gpu_info = get_gpu_info()
    monitor.update_monitoring_data(cpu_name, cpu_usage, cpu_temps, ram_info, gpu_info)

def main():
    app = QApplication(sys.argv)
    monitor = MonitoringApp()
    monitor.show()
    settings = load_settings()
    update_interval = settings.get('update_interval', 5)
    timer = QTimer()
    timer.timeout.connect(lambda: update_gui(monitor))
    timer.start(update_interval * 1000)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
