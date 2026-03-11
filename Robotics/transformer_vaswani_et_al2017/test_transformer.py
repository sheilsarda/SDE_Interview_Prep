import unittest

import torch

from transformer import BarebonesTransformer, MultiHeadAttention, generate_causal_mask


class TestTransformerPaperBarebones(unittest.TestCase):
    def setUp(self) -> None:
        torch.manual_seed(7)

    def test_forward_output_shape(self) -> None:
        model = BarebonesTransformer(
            vocab_size=50,
            d_model=32,
            num_heads=4,
            num_encoder_layers=2,
            num_decoder_layers=2,
            d_ff=64,
            dropout=0.0,
            pad_token_id=0,
        )
        src = torch.tensor([[1, 2, 3, 0, 0], [4, 5, 6, 7, 8]], dtype=torch.long)
        tgt = torch.tensor([[1, 2, 3, 4], [9, 8, 0, 0]], dtype=torch.long)

        logits = model(src, tgt)
        self.assertEqual(tuple(logits.shape), (2, 4, 50))

    def test_causal_mask_structure(self) -> None:
        mask = generate_causal_mask(seq_len=4, device=torch.device("cpu"))
        self.assertEqual(tuple(mask.shape), (1, 1, 4, 4))
        self.assertFalse(bool(mask[0, 0, 2, 0]))  # can attend to past
        self.assertFalse(bool(mask[0, 0, 2, 2]))  # can attend to self
        self.assertTrue(bool(mask[0, 0, 1, 2]))   # cannot attend to future

    def test_attention_mask_blocks_future_positions(self) -> None:
        mha = MultiHeadAttention(d_model=4, num_heads=1, dropout=0.0)

        # Make Q/K/V projections identity so attention behavior is easy to inspect.
        with torch.no_grad():
            eye = torch.eye(4)
            mha.q_proj.weight.copy_(eye)
            mha.k_proj.weight.copy_(eye)
            mha.v_proj.weight.copy_(eye)
            mha.out_proj.weight.copy_(eye)
            mha.q_proj.bias.zero_()
            mha.k_proj.bias.zero_()
            mha.v_proj.bias.zero_()
            mha.out_proj.bias.zero_()

        x = torch.tensor([[[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]]])
        mask = generate_causal_mask(seq_len=2, device=x.device)
        _, weights = mha(x, x, x, attn_mask=mask, need_weights=True)

        self.assertIsNotNone(weights)
        # Position 0 must not attend to position 1 because of causal masking.
        self.assertAlmostEqual(float(weights[0, 0, 1].detach()), 0.0, places=6)

    def test_backward_pass_runs(self) -> None:
        model = BarebonesTransformer(
            vocab_size=20,
            d_model=16,
            num_heads=4,
            num_encoder_layers=1,
            num_decoder_layers=1,
            d_ff=32,
            dropout=0.0,
        )
        src = torch.tensor([[1, 2, 3], [4, 5, 0]], dtype=torch.long)
        tgt = torch.tensor([[1, 2], [3, 0]], dtype=torch.long)

        logits = model(src, tgt)
        loss = logits.sum()
        loss.backward()

        self.assertIsNotNone(model.src_embedding.weight.grad)

    def test_embedding_tying_enabled(self) -> None:
        model = BarebonesTransformer(vocab_size=30, d_model=24, num_heads=4, tie_embeddings=True)
        self.assertIs(model.src_embedding.weight, model.tgt_embedding.weight)
        self.assertIs(model.tgt_embedding.weight, model.output_projection.weight)


if __name__ == "__main__":
    unittest.main()
