# Domain Expert LLM

Fine-tune a small language model using LoRA/QLoRA on domain-specific data (e.g., technical support conversations). Implement data preparation, training with PEFT, evaluation with domain-specific metrics, and comparison with the base model.

## Overview

This project walks you through the full lifecycle of fine-tuning an LLM for a specific domain. You will prepare instruction-tuning data from raw conversations, configure LoRA adapters for parameter-efficient training, train the model using the HuggingFace ecosystem, evaluate with both standard NLP metrics and domain-specific measures, and merge the adapter back into the base model for deployment.

## Learning Objectives

- Understand the difference between full fine-tuning and parameter-efficient methods (LoRA, QLoRA)
- Prepare instruction-tuning datasets from raw domain data
- Configure LoRA hyperparameters (rank, alpha, target modules) with informed trade-offs
- Train a causal language model using HuggingFace Trainer with PEFT integration
- Implement custom training callbacks for logging, early stopping, and checkpointing
- Evaluate generative models with perplexity, ROUGE, BERTScore, and domain-specific metrics
- Compare fine-tuned model performance against the base model systematically
- Merge LoRA adapters back into the base model for efficient inference

## Project Description

You are building a domain expert model for technical support. The pipeline includes:

1. **Data Preparation** — Load raw conversations, clean and format them into instruction/response pairs, handle edge cases
2. **Tokenization** — Build a tokenization pipeline with proper padding, truncation, and special token handling
3. **Configuration** — Define training hyperparameters and LoRA settings as validated Pydantic models
4. **Training** — Fine-tune using HuggingFace Trainer with PEFT, custom callbacks, and gradient checkpointing
5. **Evaluation** — Measure model quality with perplexity, ROUGE, BERTScore, and domain accuracy
6. **Benchmarking** — Compare fine-tuned vs base model on a held-out test set
7. **Inference** — Build an inference pipeline for the fine-tuned model
8. **Merging** — Merge the LoRA adapter weights back into the base model

## Architecture

```
src/llm_fine_tuning/
├── data/
│   ├── dataset_preparation.py     # Data loading, cleaning, formatting
│   ├── data_collator.py           # Custom data collator for causal LM
│   └── tokenization.py            # Tokenization pipeline
├── config/
│   ├── training_config.py         # Training hyperparameters (Pydantic)
│   └── lora_config.py             # LoRA/QLoRA configuration
├── training/
│   ├── trainer.py                 # Training loop with PEFT
│   └── callbacks.py               # Custom training callbacks
├── evaluation/
│   ├── metrics.py                 # Evaluation metrics
│   └── benchmark.py               # Base vs fine-tuned comparison
├── inference/
│   └── generate.py                # Inference pipeline
└── merge/
    └── merge_adapter.py           # Merge LoRA into base model

tests/
├── test_data_preparation.py
├── test_training_config.py
└── test_evaluation.py
```

## Implementation Tasks

### Phase 1: Data Pipeline
- [ ] Implement data loading and cleaning (`data/dataset_preparation.py`)
- [ ] Build the tokenization pipeline (`data/tokenization.py`)
- [ ] Create the custom data collator (`data/data_collator.py`)

### Phase 2: Configuration
- [ ] Define training config as a Pydantic model (`config/training_config.py`)
- [ ] Define LoRA config with validation (`config/lora_config.py`)

### Phase 3: Training
- [ ] Implement the training loop with PEFT (`training/trainer.py`)
- [ ] Build custom callbacks (`training/callbacks.py`)

### Phase 4: Evaluation & Benchmarking
- [ ] Implement evaluation metrics (`evaluation/metrics.py`)
- [ ] Build the benchmark comparison pipeline (`evaluation/benchmark.py`)

### Phase 5: Inference & Merging
- [ ] Create the inference pipeline (`inference/generate.py`)
- [ ] Implement adapter merging (`merge/merge_adapter.py`)

### Phase 6: Testing
- [ ] Write tests for data preparation
- [ ] Write tests for config validation
- [ ] Write tests for evaluation metrics

## Evaluation Criteria

- Data pipeline correctly transforms raw conversations into instruction-tuning format
- LoRA configuration validates hyperparameter constraints
- Training runs without errors with gradient checkpointing enabled
- Evaluation metrics are computed correctly
- Benchmark shows measurable improvement over the base model on domain tasks
- Merged model produces identical outputs to the adapter-based model
- Tests pass with `pytest`

## Resources

- [HuggingFace PEFT Documentation](https://huggingface.co/docs/peft)
- [LoRA Paper: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [HuggingFace Trainer](https://huggingface.co/docs/transformers/main_classes/trainer)
- [TRL: Transformer Reinforcement Learning](https://huggingface.co/docs/trl)
- [BitsAndBytes Quantization](https://huggingface.co/docs/bitsandbytes)
