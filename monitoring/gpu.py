import GPUtil

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