from flask import Flask, request, jsonify
from icmplib import ping
import socket
import json

app = Flask(__name__)

@app.route('/ping', methods=['POST'])
def _ping():
    _data = request.json
    print(_data)
    _ip = _data['ip']
    _count = int(_data['time'])
    host = ping(_ip, count=_count, interval=0.2, timeout=1.5)
    if host.packets_received > 0:
        return jsonify({"status": "success", "ip": _ip, "result": f'{host.packets_received}/{host.packets_sent}'}), 200
    else:
        return jsonify({"status": "error", "ip": _ip, "result": host.packets_received}), 200

@app.route('/port', methods=['POST'])
def check_port() -> json:
    _data = request.json
    _ip = _data['ip']
    _port = int(_data['port'])
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            if sock.connect_ex((_ip, _port)) == 0:
                return jsonify({"status": "success", "ip": _ip, "result": "1"}), 200
        return jsonify({"status": "error", "ip": _ip, "result": "0"}), 200  # unreachable
    except (OSError, ValueError):
        return jsonify({"status": "error", "ip": _ip, "result": "-1"}), 200 # Exception

if __name__ == '__main__':

    # from waitress import serve
    # serve(app, host='0.0.0.0', port=4488)
    app.run(debug=True, host='0.0.0.0', port=44488)