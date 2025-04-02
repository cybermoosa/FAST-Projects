from flask import Flask, jsonify, render_template, request
from scapy.all import sniff
from threading import Thread, Event
import socket
import os

app = Flask(__name__)

capture_thread = None
stop_event = Event()
packets = []

def packet_callback(packet):
    if stop_event.is_set():
        return
    packets.append(packet.summary())

def capture_packets():
    sniff(prn=packet_callback, stop_filter=lambda p: stop_event.is_set())

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

@app.route('/packet_sniffer')
def packet_sniffer():
    return render_template('packetsniffer.html')

@app.route('/port_scanner')
def port_scanner():
    return render_template('portscanner.html', result='')

@app.route('/start_capture')
def start_capture():
    global capture_thread, stop_event, packets
    stop_event.clear()
    packets = []
    capture_thread = Thread(target=capture_packets)
    capture_thread.start()
    return jsonify({'status': 'started'})

@app.route('/stop_capture')
def stop_capture():
    global stop_event
    stop_event.set()
    capture_thread.join()
    return jsonify({'status': 'stopped'})

@app.route('/get_packets')
def get_packets():
    return jsonify({'packets': packets})

@app.route('/get_packet_details')
def get_packet_details():
    packet_index = int(request.args.get('index', 0))
    if packet_index < len(packets):
        # Replace `repr(packet)` with detailed analysis of the packet.
        details = repr(packets[packet_index])  
        return jsonify({'details': details})
    return jsonify({'details': 'Packet not found'})


@app.route('/scan', methods=['POST'])
def scan():
    target_ip = request.form['target_ip']
    open_ports = port_scan(target_ip)
    result = f"Open ports for {target_ip}: \n {', '.join(map(str, open_ports))}" if open_ports else f"No open ports found for {target_ip}."

    return render_template('portscanner.html', result=result)

if __name__ == '__main__':
    print(f"Current working directory: {os.getcwd()}")
    app.run(debug=True)
