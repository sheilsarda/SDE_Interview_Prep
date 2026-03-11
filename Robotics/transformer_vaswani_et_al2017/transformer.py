"""Barebones Transformer (Vaswani et al., 2017) in PyTorch.

This module intentionally focuses on the core architecture:
- Scaled dot-product attention
- Multi-head attention
- Encoder/decoder stacks
- Sinusoidal positional encoding
"""

from __future__ import annotations

import math
from typing import Optional, Tuple

import torch
from torch import Tensor, nn


def generate_causal_mask(seq_len: int, device: torch.device) -> Tensor:
    """Return a boolean mask for decoder self-attention.

    Shape: [1, 1, seq_len, seq_len]
    True means "masked out" (cannot attend).
    """
    upper = torch.triu(torch.ones(seq_len, seq_len, device=device, dtype=torch.bool), diagonal=1)
    return upper.unsqueeze(0).unsqueeze(0)


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding from Attention Is All You Need."""

    def __init__(self, d_model: int, max_len: int = 512, dropout: float = 0.1) -> None:
        super().__init__()
        self.dropout = nn.Dropout(dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float32).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2, dtype=torch.float32) * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0), persistent=False)  # [1, max_len, d_model]

    def forward(self, x: Tensor) -> Tensor:
        seq_len = x.size(1)
        x = x + self.pe[:, :seq_len, :]
        return self.dropout(x)


class MultiHeadAttention(nn.Module):
    """Multi-head scaled dot-product attention."""

    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1) -> None:
        super().__init__()
        if d_model % num_heads != 0:
            raise ValueError("d_model must be divisible by num_heads.")

        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads

        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def _split_heads(self, x: Tensor) -> Tensor:
        # [B, T, D] -> [B, H, T, D_head]
        bsz, seq_len, _ = x.shape
        x = x.view(bsz, seq_len, self.num_heads, self.head_dim)
        return x.transpose(1, 2)

    def _merge_heads(self, x: Tensor) -> Tensor:
        # [B, H, T, D_head] -> [B, T, D]
        bsz, _, seq_len, _ = x.shape
        x = x.transpose(1, 2).contiguous()
        return x.view(bsz, seq_len, self.d_model)

    def forward(
        self,
        query: Tensor,
        key: Tensor,
        value: Tensor,
        attn_mask: Optional[Tensor] = None,
        key_padding_mask: Optional[Tensor] = None,
        need_weights: bool = False,
    ) -> Tuple[Tensor, Optional[Tensor]]:
        """
        Args:
            query, key, value: [B, T, D]
            attn_mask: bool mask broadcastable to [B, H, Tq, Tk]
            key_padding_mask: [B, Tk] where True means padded token
        """
        q = self._split_heads(self.q_proj(query))
        k = self._split_heads(self.k_proj(key))
        v = self._split_heads(self.v_proj(value))

        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)

        if attn_mask is not None:
            scores = scores.masked_fill(attn_mask, float("-inf"))

        if key_padding_mask is not None:
            pad = key_padding_mask.unsqueeze(1).unsqueeze(2)  # [B,1,1,Tk]
            scores = scores.masked_fill(pad, float("-inf"))

        weights = torch.softmax(scores, dim=-1)
        weights = self.dropout(weights)

        attended = torch.matmul(weights, v)
        out = self.out_proj(self._merge_heads(attended))

        if need_weights:
            # Average across heads for easier inspection in tests/debug.
            return out, weights.mean(dim=1)
        return out, None


class PositionwiseFeedForward(nn.Module):
    """Per-token MLP: Linear -> ReLU -> Linear."""

    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.net(x)


class EncoderLayer(nn.Module):
    """One encoder block with post-norm residual pattern from the paper."""

    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.1) -> None:
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.ffn = PositionwiseFeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: Tensor, src_padding_mask: Optional[Tensor]) -> Tensor:
        attn_out, _ = self.self_attn(x, x, x, key_padding_mask=src_padding_mask)
        x = self.norm1(x + self.dropout(attn_out))
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        return x


class DecoderLayer(nn.Module):
    """One decoder block with masked self-attention and cross-attention."""

    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.1) -> None:
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.cross_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.ffn = PositionwiseFeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(
        self,
        x: Tensor,
        memory: Tensor,
        causal_mask: Tensor,
        tgt_padding_mask: Optional[Tensor],
        src_padding_mask: Optional[Tensor],
    ) -> Tensor:
        self_attn_out, _ = self.self_attn(
            x, x, x, attn_mask=causal_mask, key_padding_mask=tgt_padding_mask
        )
        x = self.norm1(x + self.dropout(self_attn_out))

        cross_out, _ = self.cross_attn(x, memory, memory, key_padding_mask=src_padding_mask)
        x = self.norm2(x + self.dropout(cross_out))

        ffn_out = self.ffn(x)
        x = self.norm3(x + self.dropout(ffn_out))
        return x


class BarebonesTransformer(nn.Module):
    """Minimal encoder-decoder Transformer for educational/interview use."""

    def __init__(
        self,
        vocab_size: int,
        d_model: int = 128,
        num_heads: int = 4,
        num_encoder_layers: int = 2,
        num_decoder_layers: int = 2,
        d_ff: int = 256,
        max_seq_len: int = 512,
        dropout: float = 0.1,
        pad_token_id: int = 0,
        tie_embeddings: bool = True,
    ) -> None:
        super().__init__()
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.pad_token_id = pad_token_id

        self.src_embedding = nn.Embedding(vocab_size, d_model)
        self.tgt_embedding = nn.Embedding(vocab_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model, max_seq_len, dropout)
        self.dropout = nn.Dropout(dropout)

        self.encoder_layers = nn.ModuleList(
            [EncoderLayer(d_model, num_heads, d_ff, dropout) for _ in range(num_encoder_layers)]
        )
        self.decoder_layers = nn.ModuleList(
            [DecoderLayer(d_model, num_heads, d_ff, dropout) for _ in range(num_decoder_layers)]
        )

        self.output_projection = nn.Linear(d_model, vocab_size, bias=False)

        # A common Transformer optimization: share token embedding and output weights.
        if tie_embeddings:
            self.tgt_embedding.weight = self.src_embedding.weight
            self.output_projection.weight = self.tgt_embedding.weight

    def encode(self, src_tokens: Tensor, src_padding_mask: Optional[Tensor]) -> Tensor:
        x = self.src_embedding(src_tokens) * math.sqrt(self.d_model)
        x = self.positional_encoding(x)
        x = self.dropout(x)
        for layer in self.encoder_layers:
            x = layer(x, src_padding_mask)
        return x

    def decode(
        self,
        tgt_tokens: Tensor,
        memory: Tensor,
        causal_mask: Tensor,
        tgt_padding_mask: Optional[Tensor],
        src_padding_mask: Optional[Tensor],
    ) -> Tensor:
        x = self.tgt_embedding(tgt_tokens) * math.sqrt(self.d_model)
        x = self.positional_encoding(x)
        x = self.dropout(x)
        for layer in self.decoder_layers:
            x = layer(x, memory, causal_mask, tgt_padding_mask, src_padding_mask)
        return x

    def forward(self, src_tokens: Tensor, tgt_tokens: Tensor) -> Tensor:
        """
        Args:
            src_tokens: [B, S]
            tgt_tokens: [B, T]
        Returns:
            logits: [B, T, vocab_size]
        """
        src_padding_mask = src_tokens.eq(self.pad_token_id)  # [B, S]
        tgt_padding_mask = tgt_tokens.eq(self.pad_token_id)  # [B, T]
        causal_mask = generate_causal_mask(tgt_tokens.size(1), tgt_tokens.device)

        memory = self.encode(src_tokens, src_padding_mask)
        dec_out = self.decode(tgt_tokens, memory, causal_mask, tgt_padding_mask, src_padding_mask)
        return self.output_projection(dec_out)
