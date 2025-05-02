1. curl -fsSL https://ollama.com/install.sh | sudo -E sh
2. Start Ollama:
    ```bash
    nohup ollama serve &
    sleep 5
    curl -i http://localhost:11434
    ```
3. Install the model:
    ```bash
    ollama pull deepseek-coder-v2:latest
    ```

