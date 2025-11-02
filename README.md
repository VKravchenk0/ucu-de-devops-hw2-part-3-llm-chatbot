# HW2 + HW3: Containerized LLM chat

HW2: Зроблено на Streamlit + Docker model runner, запуск через docker compose  

HW3: Зроблено на Streamlit + Ollama, запускається в k8s

Код для streamlit-частини взято з офіційного прикладу:  
https://streamlit.io/playground?example=llm_chat

## HW2: docker-compose + docker model runner
### Налаштування Windows + WSL
```
Docker desktop -> Settings -> AI -> Enable Docker Model Runner + Enable host-side TCP support
```

### Запуск
```bash
docker compose -f ./docker-compose/docker-compose.yaml up --build
```

### URL
http://localhost:8051


## HW3: Kubernetes + Ollama

1. Старт кластеру
    ```bash
    minikube start --kubernetes-version=v1.32.0 
    ```

2. Білд докер-імеджу
    ```bash
    docker build -t llm-chatbot-app:latest ./web
    ```

2. Створення неймспейсу, apply конфігурацій
    ```bash
    kubectl create namespace hw3-llm-chatbot
    kubectl config set-context --current --namespace=hw3-llm-chatbot
    kubectl apply -f k8s/
    ```

3. Чекаємо, поки відпрацює завантаження моделі в ollama init-контейнері, перевіряємо ресурси
    ```bash
    kubectl get all
    ```

4. Створюємо тунель
    ```bash
    sudo --preserve-env=HOME minikube tunnel
    ```

5. Переходимо на http://localhost:8050