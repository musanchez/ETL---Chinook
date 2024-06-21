import subprocess
import os

scripts = [
    r"Landing\ChinookLANDING.py",
    r"Landing\CargaLanding.py",
    r"Dimensional\ChinookDW.py",
    r"Dimensional\CargaDimensional.py"
]

for script in scripts:
    try:
        # Ejecuta el script y espera a que termine
        result = subprocess.run(["python", script], check=True, capture_output=True, text=True)
        # Imprime la salida del script
        print(f"Salida de {os.path.basename(script)}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script}: {e.stderr}")