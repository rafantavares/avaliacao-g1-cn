# Sistema de Mensagens com Docker

Aplicação em Python (Flask) rodando em 3 containers (app1, app2 e app3). Quando um container recebe uma mensagem, ele salva e manda uma cópia para os outros dois.

## Endpoints

- `POST /send`: recebe `{"message": "texto"}`, salva a mensagem e replica para os outros containers
- `GET /messages`: mostra as mensagens salvas no container

## Como funciona

- Todos os containers usam o volume `dados`, montado em `/data`
- Cada container salva as mensagens em `mensagens_<nome>.txt` e o log em `<nome>.log`
- Os containers ficam na rede bridge `minha_rede` e se comunicam pelo nome do serviço
- A resposta do POST mostra se a replicação para cada container funcionou (`true`/`false`)
- A cópia é enviada com `?copia=1`, para o container que recebe não replicar de novo

Portas: app1 = 5001, app2 = 5002, app3 = 5003

## Como rodar

```bash
docker compose up -d --build
```

Enviar mensagem:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"message":"hello"}' http://localhost:5001/send
```

Ver as mensagens em outro container:

```bash
curl http://localhost:5002/messages
```

Ou rodar o teste:

```bash
bash test.sh
```

Ver os logs:

```bash
docker compose exec app1 cat /data/app1.log
```

Parar:

```bash
docker compose down -v
```
