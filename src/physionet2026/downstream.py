from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


def masked_mean(sequence: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    weights = mask.float().unsqueeze(-1)
    return (sequence * weights).sum(dim=1) / weights.sum(dim=1).clamp(min=1.0)


class SleepFMClassifier(nn.Module):
    def __init__(self, variant: str = "B1"):
        super().__init__()
        self.variant = variant
        self.use_demographics = variant == "B2"
        if variant in {"B1", "B2"}:
            self.encoder = nn.LSTM(
                input_size=128,
                hidden_size=64,
                num_layers=2,
                dropout=0.3,
                bidirectional=True,
                batch_first=True,
            )
        else:
            self.encoder = None
        input_dim = 128 + (2 if self.use_demographics else 0)
        self.head = nn.Linear(input_dim, 1)

    def forward(
        self,
        embeddings: torch.Tensor,
        mask: torch.Tensor,
        demographics: torch.Tensor | None = None,
    ) -> torch.Tensor:
        if self.encoder is not None:
            lengths = mask.sum(dim=1).clamp(min=1).cpu()
            packed = nn.utils.rnn.pack_padded_sequence(
                embeddings,
                lengths=lengths,
                batch_first=True,
                enforce_sorted=False,
            )
            encoded, _ = self.encoder(packed)
            embeddings, _ = nn.utils.rnn.pad_packed_sequence(
                encoded,
                batch_first=True,
                total_length=embeddings.shape[1],
            )
        pooled = masked_mean(embeddings, mask)
        if self.use_demographics:
            if demographics is None:
                raise ValueError("Demographics are required for B2.")
            pooled = torch.cat([pooled, demographics], dim=1)
        return self.head(pooled).squeeze(-1)


@dataclass
class DemographicStats:
    age_mean: float
    age_std: float

    def encode(self, age: torch.Tensor, sex_code: torch.Tensor) -> torch.Tensor:
        age_norm = (age - self.age_mean) / max(self.age_std, 1e-6)
        return torch.stack([age_norm, sex_code], dim=1)

