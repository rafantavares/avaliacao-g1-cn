#!/bin/bash

docker compose up -d --build
sleep 5

echo "Enviando mensagem para o app1..."
curl -s -X POST -H "Content-Type: application/json" -d '{"message":"hello"}' http://localhost:5001/send
echo

echo "Mensagens no app1:"
curl -s http://localhost:5001/messages
echo

echo "Mensagens no app2:"
curl -s http://localhost:5002/messages
echo

echo "Mensagens no app3:"
curl -s http://localhost:5003/messages
echo

echo "Arquivos no volume:"
docker compose exec app1 ls /data
