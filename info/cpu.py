import psutil
import platform
import wmi


def get_cpu_name():
    if platform.system() == "Windows":
        try:
            w = wmi.WMI()
            for processor in w.Win32_Processor():
                return processor.Name
        except wmi.x_wmi as e:
            print(f"Error querying WMI: {e}")
    elif platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except FileExistsError:
            pass
    return "Unknown CPU"

def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_temps = []
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            cpu_temps = temps['coretemp']
        elif 'cpu-thermal' in temps:
            cpu_temps = temps['cpu-thermal']
    except AttributeError:
        pass
    
    if not cpu_temps and platform.system() == 'Windows':
        try:
            w = wmi.WMI(namespace="root\\wmi")
            temperature_info = w.MSAcpi_ThermalZoneTemperature()
            for sensor in temperature_info:
                cpu_temps.append(sensor.CurrentTemperature / 10 - 273.15)
        except ImportError:
            pass
        except wmi.x_wmi as e:
            print(f"Error querying WMI: {e}")
    cpu_name = get_cpu_name()
    return cpu_name, cpu_usage, cpu_temps

