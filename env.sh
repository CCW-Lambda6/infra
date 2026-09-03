source /AI/state/secrets.sh

export AI_HOME=/AI
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# hugging face
export HF_HOME=/AI/hfhome
export HF_TOKEN_PATH=/AI/state/secrets/huggingface-token

# open-webui
export DATA_DIR=/AI/state/open-webui

# llama.cpp
export LLAMA_CACHE=/AI/caches/llama

# PyTorch
export TORCH_HOME=/AI/caches/torch
