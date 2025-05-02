#!/bin/bash

escaped_content=$(jq -Rs . < data/changes.diff)
prompt=$(cat "static/prompt-file.txt")

escaped_content=$(jq -R <<<"$prompt$(jq -r <<<"$escaped_content")" | jq -Rs .)

response=$(curl -s -w "%{response_code}" -X POST http://127.0.0.1:11434/api/generate \
          -H "Content-Type: application/json" \
          -d "{\"model\":\"deepseek-coder-v2:latest\",\"system\":\"You are the best code reviewer in the world with extensive knowledge of software development.\",\"prompt\":$escaped_content,\"stream\": false,\"options\":{\"num_ctx\":4096} }")

http_code=${response: -3}
content=$(echo ${response} | head -c-4)

if [ $http_code -ne 200 ]; then
    echo "The operation failed!"
    echo "$response"
    if [[ "${{ inputs.fail-on-error }}" == "true" ]]; then
        exit 1
    fi
else
    echo "The operation succeeded!"
    message=$(echo $content | jq -r '.response')
    echo $message > "data/response.json"
    echo $message
fi
