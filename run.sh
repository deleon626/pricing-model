#!/bin/bash

# Create a virtual environment with uv if it doesn't exist
if [ ! -d ".venv" ]; then
  uv venv
fi

# Install requirements using uv
uv pip install -r requirements.txt

# Run the Streamlit app using uv
uv run streamlit run app.py 