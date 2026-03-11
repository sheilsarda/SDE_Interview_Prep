# Attention Is All You Need (2017) - Barebones PyTorch Transformer

This folder contains a minimal, interview-focused implementation of the core architecture from:

- Vaswani et al., **"Attention Is All You Need"** (NeurIPS 2017)

## What Is Implemented

- Sinusoidal positional encoding
- Scaled dot-product attention
- Multi-head attention
- Encoder and decoder blocks with:
  - residual connections
  - layer normalization
  - position-wise feed-forward network
- Decoder causal masking (prevents attention to future tokens)
- Full encoder-decoder forward pass that returns token logits
- Optional embedding/softmax weight tying

## Paper Concepts to Code Mapping

- **Attention(Q, K, V) = softmax(QK^T / sqrt(dk)) V**
  - `MultiHeadAttention.forward(...)`
- **Multi-head projections + concat + output projection**
  - `q_proj`, `k_proj`, `v_proj`, `out_proj` in `MultiHeadAttention`
- **Stacked encoder and decoder layers**
  - `EncoderLayer`, `DecoderLayer`, and `ModuleList` stacks in `BarebonesTransformer`
- **Masking in decoder self-attention**
  - `generate_causal_mask(...)`
- **Position-wise FFN**
  - `PositionwiseFeedForward`
- **Sinusoidal positional information**
  - `PositionalEncoding`

## Files

- `transformer.py` - implementation
- `test_transformer.py` - unit tests (`unittest`)

## Run Tests

From this directory (using the parent virtual environment):

```bash
..\..\..\.venv\Scripts\python.exe -m unittest -q
```

Or from `SDE_Interview_Prep` root:

```bash
.\.venv\Scripts\python.exe -m unittest discover -s Robotics\transformer_vaswani2017 -p "test_*.py" -q
```

## Simplifications (Intentional)

- Barebones educational implementation, not production training code
- No tokenizer/data pipeline/training loop
- No label smoothing, beam search, or checkpointing
- Uses small default dimensions for fast local testing
