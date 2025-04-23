#!/bin/bash

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# Install requirements if needed
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py 