# LoRA + DPO Tool Calling Platform

## Objective
This project converts natural language user requests into structured JSON tool calls using a LoRA + DPO fine-tuning pipeline and a deployable web application.

## Features
- Synthetic dataset generation
- LoRA supervised fine-tuning
- DPO preference optimization
- JSON validity evaluation
- FastAPI backend
- Streamlit frontend
- Tool calling web interface

## Supported Tools
- book_cab
- order_food
- set_reminder

## Tech Stack
- Python
- PyTorch
- Hugging Face Transformers
- PEFT
- TRL
- FastAPI
- Streamlit

## Run Training

```bash
python src/generate_data.py
python src/train_sft.py
python src/evaluate.py
python src/generate_dpo_data.py
python src/train_dpo.py