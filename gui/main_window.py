from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox
from PyQt5.QtCore import QTimer, Qt
import sys
import json
from monitoring.cpu import get_cpu_info
from monitoring.ram import get_ram_info
from monitoring.gpu import get_gpu_info


class MonitoringApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SysMonitorX')
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.cpu_usage_label = QLabel()
        layout.addWidget(self.cpu_usage_label)

        self.show_cpu_temp_checkbox = QCheckBox("Show CPU Temperature")
        self.show_cpu_temp_checkbox.setChecked(True)
        self.show_cpu_temp_checkbox.stateChanged.connect(self.toggle_cpu_temp_display)
        layout.addWidget(self.show_cpu_temp_checkbox)

        self.cpu_temp_label = QLabel()
        layout.addWidget(self.cpu_temp_label)

        self.ram_usage_label = QLabel()
        layout.addWidget(self.ram_usage_label)

        self.gpu_info_label = QLabel()
        layout.addWidget(self.gpu_info_label)

        self.setLayout(layout)
    
    def toggle_cpu_temp_display(self, state):
        if state == Qt.Checked:
            self.cpu_temp_label.show()
        else:
            self.cpu_temp_label.hide()
    
    def update_monitoring_data(self, cpu_usage, cpu_temps, ram_info, gpu_info):
        self.cpu_usage_label.setText(f"CPU Usage: {cpu_usage}%")
        if cpu_temps:
            temps_str = "\n".json([f"CPU Temperature {i+1}: {temp['temperature']}°C" for i, temp in enumerate(cpu_temps)])
            self.cpu_temp_label.setText(temps_str)
        else:
            self.cpu_temp_label.setText("CPU Temperature: Not available")
        
        self.ram_usage_label.setText(f"RAM Usage: {ram_info.percent}%")

        gpu_str = "\n\n".join([f"GPU {i+1}:\nName: {gpu['name']}\nLoad: {gpu['load']:.2f}%\nTemperature: {gpu['temperature']}°C" for i, gpu in enumerate(gpu_info)])
        self.gpu_info_label.setText(gpu_str)


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
    cpu_usage, cpu_temps = get_cpu_info()
    ram_info = get_ram_info()
    gpu_info = get_gpu_info()
    monitor.update_monitoring_data(cpu_usage, cpu_temps, ram_info, gpu_info)

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
    