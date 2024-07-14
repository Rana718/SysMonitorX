import psutil

def get_ram_info():
    ram_info = psutil.virtual_memory()
    return ram_info
