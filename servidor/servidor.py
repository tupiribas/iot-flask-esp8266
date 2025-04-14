from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

server_ip = os.environ.get('SERVER_IP')
server_port = int(os.environ.get('SERVER_PORT', 5000))


@app.route('/', methods=['GET'])
def hello():
    return "Funcionando"


@app.route('/data', methods=['POST'])
def receive_data():
    if request.is_json:
        data = request.get_json()
        print('\nESP8266: ', data)
        response = {'status': "success",
                    "message": "Dados recebidos com sucesso!"}
        return jsonify(response), 200
    else:
        return jsonify({"error": "Estou esperando o formato JSON"}), 400


if __name__ == "__main__":
    app.run(host=server_ip, port=server_port, debug=True)
