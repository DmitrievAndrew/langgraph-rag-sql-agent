#!/bin/bash
set -e

# Запускаем сервер Ollama в фоне
ollama serve &

# Ждём, пока сервер поднимется
sleep 5

# Скачиваем модели (если их нет)
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# Оставляем процесс работающим
wait