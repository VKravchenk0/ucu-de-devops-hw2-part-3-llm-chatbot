# DevOps HW2: LLM Chatbot (docker-compose)
Зроблено на Streamlit + Docker Model Runner.

Код для streamlit-частини взято з офіційного прикладу:  
https://streamlit.io/playground?example=llm_chat

## Налаштування Windows + WSL
`Docker desktop -> Settings -> AI -> Enable Docker Model Runner + Enable host-side TCP support`

## Запуск
```bash
docker compose up --build
```

## URL
http://localhost:8050

# DevOps HW3: LLM Chatbot (kubernetes)

1. Старт кластеру
    ```bash
    minikube start --kubernetes-version=v1.32.0 
    ```

2. Білд докер-імеджу
    ```bash
    # build your web image
    eval $(minikube docker-env)
    docker build -t llm-chatbot-app:latest ./web

    # deploy all resources
    ```

2. Створення неймспейсу, apply конфігурацій
    ```bash
    kubectl create namespace hw3-llm-chatbot
    kubectl config set-context --current --namespace=hw3-llm-chatbot
    kubectl apply -f k8s/
    ```

3. Створення тунелю
    ```bash
    sudo --preserve-env=HOME minikube tunnel
    ```