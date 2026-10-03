import os
from datetime import datetime

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

nome = os.getenv("NOME")
outros = os.getenv("OUTROS").split(",")

arquivo_msgs = f"/data/mensagens_{nome}.txt"
arquivo_log = f"/data/{nome}.log"


def log(texto):
    with open(arquivo_log, "a") as f:
        f.write(f"{datetime.now()} - {texto}\n")


@app.route("/send", methods=["POST"])
def send():
    msg = request.json["message"]

    with open(arquivo_msgs, "a") as f:
        f.write(msg + "\n")
    log(f"mensagem salva: {msg}")

    if request.args.get("copia"):
        return jsonify({"status": "ok"})

    replicacao = {}
    for outro in outros:
        try:
            r = requests.post(f"http://{outro}:5000/send?copia=1", json={"message": msg})
            replicacao[outro] = r.status_code == 200
        except:
            replicacao[outro] = False
        log(f"replicacao para {outro}: {replicacao[outro]}")

    return jsonify({"status": "ok", "replicacao": replicacao})


@app.route("/messages", methods=["GET"])
def messages():
    if not os.path.exists(arquivo_msgs):
        return jsonify([])
    with open(arquivo_msgs) as f:
        return jsonify(f.read().splitlines())


app.run(host="0.0.0.0", port=5000)
