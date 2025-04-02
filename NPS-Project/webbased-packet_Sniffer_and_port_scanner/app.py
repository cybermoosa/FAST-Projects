from flask import Flask, request, render_template
import socket
from datetime import datetime

app = Flask(__name__)

def port_scan(target):
    open_ports = []
    try:
        ip = socket.gethostbyname(target)

        for port in range(130, 140):  # Scanning ports 130-139
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()

    except Exception as e:
        return f"Error: {e}"

    return open_ports

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portscanner')
def portscanner():
    return render_template('portscanner.html', result='')

@app.route('/scan', methods=['POST'])
def scan():
    target_ip = request.form['target_ip']
    open_ports = port_scan(target_ip)
    result = f"Open ports for {target_ip}: \n {', '.join(map(str, open_ports))}" if open_ports else f"No open ports found for {target_ip}."

    return render_template('portscanner.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
