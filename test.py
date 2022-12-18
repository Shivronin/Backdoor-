import subprocess


result = subprocess.check_output("ls", shell=True).decode()

print(result)
