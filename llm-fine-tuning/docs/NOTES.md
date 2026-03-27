# Domain Expert LLM — Theory & Notes

## Transfer Learning and Fine-Tuning

### Core Concept

Pre-trained language models learn general language understanding from massive corpora. Fine-tuning adapts this general knowledge to a specific domain or task by continuing training on a smaller, task-specific dataset.

The key insight: it is far more efficient to adapt an existing model than to train one from scratch. A 7B parameter model trained on trillions of tokens encodes vast linguistic knowledge that transfers to downstream tasks with relatively little additional data.

### Full Fine-Tuning vs Parameter-Efficient Methods

**Full fine-tuning** updates all model parameters. For a 7B model with fp16 weights, this requires ~14GB for the model, ~14GB for gradients, and ~56GB for optimizer states (Adam) — roughly 84GB of GPU memory.

**Parameter-efficient fine-tuning (PEFT)** freezes the base model and only trains a small number of additional parameters:
- **LoRA** — Adds low-rank decomposition matrices to attention layers
- **Prefix Tuning** — Prepends trainable tokens to the input
- **Adapters** — Inserts small trainable layers between frozen layers
- **IA3** — Learns scaling vectors for keys, values, and FFN outputs

PEFT reduces memory by 10-100x while achieving comparable quality to full fine-tuning on most tasks.

## LoRA (Low-Rank Adaptation)

### How It Works

For a pre-trained weight matrix W ∈ ℝ^(d×k), LoRA adds a low-rank decomposition:

```
W' = W + ΔW = W + B·A
```

Where:
- A ∈ ℝ^(r×k) — down-projection (initialized with random Gaussian)
- B ∈ ℝ^(d×r) — up-projection (initialized with zeros)
- r << min(d, k) — the rank (typically 4, 8, 16, 32, or 64)

At initialization, ΔW = B·A = 0, so the model starts identical to the pre-trained one. During training, only A and B are updated; W remains frozen.

### Rank and Alpha Hyperparameters

**Rank (r):** Controls the expressiveness of the adaptation. Higher rank = more parameters = more capacity, but also more memory and risk of overfitting.

- r=4: Minimal adaptation, good for very similar tasks
- r=8-16: Sweet spot for most fine-tuning tasks
- r=32-64: Maximum expressiveness, use for very different domains

**Alpha (α):** A scaling factor applied to the LoRA update: `ΔW = (α/r) · B·A`. Higher alpha amplifies the adaptation signal.

- Common practice: Set α = 2r (e.g., r=16, α=32)
- The ratio α/r controls the effective learning rate of the LoRA layers

### Target Modules

Which layers to apply LoRA to matters significantly:

- **Attention projections** (q_proj, k_proj, v_proj, o_proj) — Most common, good default
- **MLP layers** (gate_proj, up_proj, down_proj) — Adds capacity but more parameters
- **All linear layers** — Maximum adaptation but diminishing returns

Rule of thumb: Start with attention projections only. Add MLP layers if quality is insufficient.

## QLoRA and Quantization

### 4-bit Quantization

QLoRA combines LoRA with 4-bit quantization of the base model:

1. Load the base model in 4-bit precision (NF4 — Normal Float 4)
2. Apply LoRA adapters (trained in fp16/bf16)
3. During forward pass: dequantize on-the-fly → compute → discard

This reduces memory from ~14GB (fp16) to ~3.5GB (4-bit) for a 7B model, enabling fine-tuning on consumer GPUs.

### Key QLoRA Innovations

- **NF4 data type** — Optimal for normally distributed weights (better than INT4)
- **Double quantization** — Quantize the quantization constants themselves, saving ~0.4 bits/param
- **Paged optimizers** — Use CPU memory as overflow for optimizer states

### Memory Requirements

| Method | 7B Model | 13B Model | 70B Model |
|--------|----------|-----------|-----------|
| Full fine-tune (fp16) | ~84 GB | ~156 GB | ~840 GB |
| LoRA (fp16 base) | ~16 GB | ~30 GB | ~160 GB |
| QLoRA (4-bit base) | ~6 GB | ~11 GB | ~48 GB |

## Learning Rate Scheduling

### Recommendations for Fine-Tuning

- **Base LR**: 1e-4 to 2e-4 for LoRA (10x higher than full fine-tuning)
- **Scheduler**: Cosine annealing with warmup
- **Warmup**: 3-10% of total steps
- **Weight decay**: 0.01 (standard) or 0.0 (if regularization from LoRA rank is sufficient)

### Catastrophic Forgetting

Fine-tuning too aggressively causes the model to lose its general capabilities. Mitigations:

- Use a low learning rate
- Train for few epochs (1-3 is often sufficient)
- Mix in general-purpose data (replay buffer)
- Use LoRA (implicitly limits the magnitude of weight changes)
- Evaluate on both domain tasks AND general benchmarks

## Instruction Tuning vs Continued Pre-Training

### Instruction Tuning

Format data as instruction/response pairs. The model learns to follow instructions in your domain.

```
### Instruction: {task description}
### Input: {optional context}
### Response: {desired output}
```

Best for: Task-specific applications, chatbots, Q&A systems.

### Continued Pre-Training

Feed raw domain text to the model using the standard causal LM objective (predict next token). The model absorbs domain knowledge without learning a specific task format.

Best for: Domain knowledge injection before instruction tuning (two-stage approach).

## RLHF and DPO

### RLHF (Reinforcement Learning from Human Feedback)

1. Supervised fine-tuning (SFT) on high-quality examples
2. Train a reward model on human preference data
3. Optimize the policy model using PPO against the reward model

Complex, expensive, requires reward model training.

### DPO (Direct Preference Optimization)

Directly optimize the policy model on preference pairs (chosen vs rejected) without a separate reward model. Simpler, more stable, increasingly popular.

## Evaluation Challenges for Generative Models

### Why Standard Metrics Fall Short

- **BLEU/ROUGE** measure n-gram overlap, not semantic correctness
- A perfectly valid answer with different wording scores poorly
- These metrics correlate weakly with human judgments for open-ended generation

### Better Evaluation Strategies

- **Perplexity** — How surprised is the model by the test data? Lower = better language modeling
- **BERTScore** — Semantic similarity using contextual embeddings
- **Domain-specific accuracy** — Task-specific metrics (e.g., correct entity extraction)
- **LLM-as-judge** — Use a stronger model to evaluate outputs
- **Human evaluation** — Gold standard but expensive and slow

## Training Data Quality

### Quality > Quantity

A small, high-quality dataset (1K-10K examples) typically outperforms a large, noisy one. Focus on:

- **Accuracy** — Responses must be correct
- **Consistency** — Similar inputs should have similar output styles
- **Diversity** — Cover the full range of expected inputs
- **Formatting** — Consistent instruction/response structure
- **Deduplication** — Remove near-duplicates that cause overfitting

### Data Preparation Checklist

1. Remove PII and sensitive information
2. Filter out low-quality or irrelevant examples
3. Standardize formatting (instruction template)
4. Split into train/validation/test (80/10/10)
5. Verify class/topic distribution across splits
6. Validate a random sample manually

## Compute Requirements Estimation

### Rules of Thumb

- **Training tokens**: Fine-tuning typically processes 1M-100M tokens
- **GPU hours**: For QLoRA on a 7B model, expect 2-8 hours on a single A100
- **Epochs**: 1-3 epochs is usually sufficient; more risks overfitting
- **Batch size**: Limited by GPU memory; use gradient accumulation to simulate larger batches

### Cost Estimation Formula

```
GPU hours ≈ (dataset_tokens × epochs) / (tokens_per_second × batch_size)
```

Where tokens_per_second depends on model size, quantization, and GPU type.

## Key Terminology

- **LoRA** — Low-Rank Adaptation: adds trainable low-rank matrices to frozen model layers
- **QLoRA** — Quantized LoRA: combines 4-bit quantization with LoRA for memory efficiency
- **PEFT** — Parameter-Efficient Fine-Tuning: umbrella term for methods that train few parameters
- **Rank** — Dimensionality of the LoRA decomposition matrices
- **Alpha** — Scaling factor for LoRA updates
- **Target modules** — Which model layers to apply LoRA to
- **Adapter** — The small set of trainable parameters added to the model
- **Merging** — Combining adapter weights back into the base model
- **Instruction tuning** — Fine-tuning on instruction/response pairs
- **Catastrophic forgetting** — Loss of general capabilities during fine-tuning
- **NF4** — Normal Float 4-bit: quantization format optimized for neural network weights
- **Gradient checkpointing** — Trade compute for memory by recomputing activations
