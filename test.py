
import psutil
import GPUtil
import time
import os
import platform


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
            import wmi
            w = wmi.WMI(namespace="root\\wmi")
            temperature_info = w.MSAcpi_ThermalZoneTemperature()
            for sensor in temperature_info:
                cpu_temps.append(sensor.CurrentTemperature / 10 - 273.15)
        except ImportError:
            pass
        except wmi.x_wmi as e:
            print(f"Error querying WMI: {e}")

    return cpu_usage, cpu_temps

def get_ram_info():
    ram_info = psutil.virtual_memory()
    return ram_info

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            'name': gpu.name,
            'load': gpu.load * 100,
            'temperature': gpu.temperature
        })
    return gpu_info
def main():
    while True:
        cpu_usage, cpu_temps = get_cpu_info()
        ram_info = get_ram_info()
        gpu_info = get_gpu_info()
        
        print(f"CPU Usage: {cpu_usage}%")
        if cpu_temps:
            for temp in cpu_temps:
                print(f"CPU Temperature: {temp.current if hasattr(temp, 'current') else temp:.2f}°C")
        else:
            print("CPU Temperature: Not available")
        
        print(f"RAM Usage: {ram_info.percent}%")
        print(f"Total RAM: {ram_info.total / (1024 ** 3):.2f} GB")
        print(f"Used RAM: {ram_info.used / (1024 ** 3):.2f} GB")
        print(f"Free RAM: {ram_info.available / (1024 ** 3):.2f} GB")

        for gpu in gpu_info:
            print(f"GPU: {gpu['name']}")
            print(f"GPU Load: {gpu['load']:.2f}%")
            print(f"GPU Temperature: {gpu['temperature']}°C")

        
        time.sleep(5)

if __name__ == "__main__":
    main()
