from flask import Flask, render_template
import psutil
import socket

app = Flask(__name__, template_folder="temp/")

@app.route("/")
def home():
    # CPU bilgileri
    cpu_usage = psutil.cpu_percent()
    cpu_count = psutil.cpu_count()
    per_cpu = psutil.cpu_percent(percpu=True)

    # Bellek bilgileri
    mem = psutil.virtual_memory()
    total_mem = mem.total // (1024*1024)
    used_mem = mem.used // (1024*1024)
    available_mem = mem.available // (1024*1024)

    # İşlem bilgileri
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
        except psutil.NoSuchProcess:
            pass
        else:
            processes.append(pinfo)

    # Açık portlar
    open_ports = []
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    return render_template("index.html",
                           cpu_usage=cpu_usage,
                           cpu_count=cpu_count,
                           per_cpu=per_cpu,
                           total_mem=total_mem,
                           used_mem=used_mem,
                           available_mem=available_mem,
                           processes=processes,
                           open_ports=open_ports)

if __name__ == "__main__":
    app.run(debug=True)
