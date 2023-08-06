import torch
from torch import nn
from torch.nn import functional as F
from math import sqrt, sin, cos, pow
from enum import Enum

from .activations import parse_activation_function

__all__ = [
    "Attention",
    "NonTransformingAttention",
    "MiniBert",
    "MiniBertForMLM",
    "MiniBertForRegression",
    "MiniBertEmbedding",
    "PositionEmbeddingType",
    "AttentionType",
]


class PositionEmbeddingType(Enum):
    TRAINED = 1
    FIXED = 2
    NONE = 3


class AttentionType(Enum):
    SelfAttention = 1
    AttentionEmbedding = 2
    NonTransformingAttention = 3


class PositionnalEmbedding(nn.Module):
    def __init__(self, embedding_dim, max_seq_len, position_type=PositionEmbeddingType.TRAINED):
        super().__init__()

        self.embedding_dim = embedding_dim
        self.max_seq_len = max_seq_len

        if position_type == PositionEmbeddingType.TRAINED:
            self.position_embeddings = nn.Embedding(
                max_seq_len, embedding_dim)
        elif position_type == PositionEmbeddingType.FIXED:
            # See Attention is all you need, section 3.5 (https://arxiv.org/pdf/1706.03762.pdf)
            d = embedding_dim
            positions = torch.zeros((max_seq_len, d), dtype=torch.float)
            for pos in range(max_seq_len):
                for i in range(d):
                    if i % 2 == 0:
                        positions[pos, i] = sin(pos / pow(10000, 2 * i / d))
                    else:
                        positions[pos, i] = cos(pos / pow(10000, 2 * i / d))
            self.position_embeddings = nn.Embedding.from_pretrained(
                positions, freeze=True
            )
        elif position_type == PositionEmbeddingType.NONE:
            positions = torch.zeros(
                (max_seq_len, embedding_dim), dtype=torch.float)
            self.position_embeddings = nn.Embedding.from_pretrained(
                positions, freeze=True
            )
        else:
            raise Exception("Invalid position type")

        self.register_buffer(
            "position_ids", torch.arange(max_seq_len).expand((1, -1)))

    def forward(self, input):
        seq_len = input.shape[-1]
        return self.position_embeddings(self.position_ids[:, :seq_len])


class MiniBertEmbedding(nn.Module):
    def __init__(self, voc_size, embedding_dim, position_count, position_type, normalize_embeddings):
        super().__init__()

        self.position_count = position_count
        self.position_type = position_type
        self.normalize_embeddings = normalize_embeddings

        self.word_embeddings = nn.Embedding(voc_size, embedding_dim)

        if position_type == PositionEmbeddingType.TRAINED:
            self.position_embeddings = nn.Embedding(
                position_count, embedding_dim)
        elif position_type == PositionEmbeddingType.FIXED:
            # See Attention is all you need, section 3.5 (https://arxiv.org/pdf/1706.03762.pdf)
            d = embedding_dim
            positions = torch.zeros((position_count, d), dtype=torch.float)
            for pos in range(position_count):
                for i in range(d):
                    if i % 2 == 0:
                        positions[pos, i] = sin(pos / pow(10000, 2 * i / d))
                    else:
                        positions[pos, i] = cos(pos / pow(10000, 2 * i / d))
            self.position_embeddings = nn.Embedding.from_pretrained(
                positions, freeze=True
            )
        elif position_type == PositionEmbeddingType.NONE:
            positions = torch.zeros(
                (position_count, embedding_dim), dtype=torch.float)
            self.position_embeddings = nn.Embedding.from_pretrained(
                positions, freeze=True
            )
        else:
            raise Exception("Invalid position type")

        self.register_buffer(
            "position_ids", torch.arange(position_count).expand((1, -1)))

        self.norm = None
        if normalize_embeddings:
            self.norm = nn.LayerNorm(embedding_dim)

    def forward(self, input):
        seq_len = input.shape[-1]
        word_emb = self.word_embeddings(input)
        pos_emb = self.position_embeddings(self.position_ids[:, :seq_len])
        emb = word_emb + pos_emb

        if self.normalize_embeddings:
            return self.norm(emb)
        else:
            return emb


class AttentionEmbedding(nn.Module):
    def __init__(self, embedding_dim, voc_size, out_dim=None, position_type=PositionEmbeddingType.TRAINED, normalize_embeddings=True):
        super(AttentionEmbedding, self).__init__()
        if out_dim is None:
            out_dim = embedding_dim

        self.embedding_dim = embedding_dim
        self.voc_size = voc_size
        self.out_dim = out_dim

        self.key = nn.Embedding(voc_size, embedding_dim)
        self.query = nn.Embedding(voc_size, embedding_dim)
        self.value = nn.Embedding(voc_size, out_dim)
        self._sqrt_embedding = sqrt(embedding_dim)

        self.position_embedding = PositionnalEmbedding(
            embedding_dim, 1024, position_type=position_type)

        self.norm = None
        self.normalize_embeddings = normalize_embeddings
        if normalize_embeddings:
            self.norm = nn.LayerNorm(embedding_dim)

    def forward(self, input):
        pos = self.position_embedding(input)
        key = self.key(input) + pos
        query = self.query(input) + pos
        value = self.value(input)

        if self.normalize_embeddings:
            key = self.norm(key)
            query = self.norm(query)
            value = self.norm(value)

        key_t = torch.transpose(key, -2, -1)
        qk = torch.matmul(query, key_t) / self._sqrt_embedding
        attention = F.softmax(qk, dim=-1)
        return torch.matmul(attention, value)


class Attention(nn.Module):
    def __init__(self, in_dim, out_dim, hidden_dim=None, key_is_query=False):
        super(Attention, self).__init__()
        if hidden_dim is None:
            hidden_dim = out_dim

        self.in_dim = in_dim
        self.out_dim = out_dim
        self.key_is_query = key_is_query
        self.hidden_dim = hidden_dim
        self.key = nn.Parameter(torch.rand((in_dim, hidden_dim)))
        if key_is_query:
            self.query = self.key
        else:
            self.query = nn.Parameter(torch.rand((in_dim, hidden_dim)))
        self.value = nn.Parameter(torch.rand((in_dim, out_dim)))
        self._sqrt_hidden = sqrt(hidden_dim)

    @classmethod
    def from_weights(cls, key, query, value):
        in_dim, hidden_dim = key.shape
        out_dim = value.shape[1]
        x = cls(in_dim, out_dim, hidden_dim)
        with torch.no_grad():
            x.key = nn.Parameter(key)
            x.query = nn.Parameter(query)
            x.value = nn.Parameter(value)
        return x

    def forward(self, input):
        key = torch.matmul(input, self.key)
        query = torch.matmul(input, self.query)
        value = torch.matmul(input, self.value)

        key_t = torch.transpose(key, -2, -1)
        qk = torch.matmul(query, key_t) / self._sqrt_hidden
        attention = F.softmax(qk, dim=-1)
        return torch.matmul(attention, value)


class NonTransformingAttention(nn.Module):
    def __init__(self, dim):
        super(NonTransformingAttention, self).__init__()
        self.dim = dim
        self._sqrt_dim = sqrt(dim)

    def forward(self, input):
        query = input
        key = input
        key_t = torch.transpose(key, -2, -1)
        qk = torch.matmul(query, key_t) / self._sqrt_dim
        attention = F.softmax(qk, dim=-1)
        return torch.matmul(attention, input)


class MiniBert(nn.Module):
    def __init__(self, configuration):
        super(MiniBert, self).__init__()

        self.configuration = configuration

        self._voc_size = len(configuration.vocabulary)
        self._embedding_dim = configuration.embedding_dim

        if configuration.attention_type == AttentionType.AttentionEmbedding:
            self.attention_embedding = AttentionEmbedding(
                self._embedding_dim,
                self._voc_size,
                position_type=configuration.position_type,
                normalize_embeddings=configuration.normalize_embeddings
            )
        else:
            self.embedding = MiniBertEmbedding(
                self._voc_size,
                self._embedding_dim,
                position_count=configuration.position_embeddings_count,
                position_type=configuration.position_type,
                normalize_embeddings=configuration.normalize_embeddings
            )

            if configuration.attention_type == AttentionType.SelfAttention:
                self.attention = Attention(
                    self._embedding_dim,
                    self._embedding_dim,
                    hidden_dim=configuration.hidden_dim,
                    key_is_query=configuration.key_is_query
                )
            elif configuration.attention_type == AttentionType.NonTransformingAttention:
                self.attention = NonTransformingAttention(
                    self._embedding_dim
                )
            else:
                raise Exception("Invalid attention type")

    def forward(self, input):
        if self.configuration.attention_type == AttentionType.AttentionEmbedding:
            x = self.attention_embedding(input)
        else:
            x = self.embedding(input)
            x = self.attention(x)
        return x


class MiniBertForMLM(nn.Module):
    def __init__(self, configuration):
        super().__init__()
        self.minibert = MiniBert(configuration)
        self.configuration = configuration

        self._voc_size = len(configuration.vocabulary)
        self._embedding_dim = configuration.embedding_dim

        self.l1 = nn.Linear(self._embedding_dim,
                            configuration.first_layer_output_size, bias=False)
        self.l2 = nn.Linear(
            configuration.first_layer_output_size, self._voc_size, bias=True)

        self.mask_idx = configuration.mask_idx

        self.activation_fun = parse_activation_function(
            configuration.activation_fun)

        self._mask_prob = configuration.mask_prob
        self._keep_mask_prob = configuration.keep_mask_prob
        self._inv_corrupt_mask_prob = 1 - configuration.corrupt_mask_prob

    def forward(self, input):
        if self.training:
            masked_input = input.detach().clone()
            masked = torch.rand_like(
                input, dtype=torch.float) <= self._mask_prob

            masking_strategy = torch.rand_like(input, dtype=torch.float)
            masking = masked & (masking_strategy <=
                                self._keep_mask_prob)  # Keep masks
            corrupt = masked & (self._inv_corrupt_mask_prob <
                                masking_strategy)  # Corrupt masks

            replacements = torch.randint(
                self._voc_size, (torch.sum(corrupt), ), device=input.device)

            masked_input[masking] = self.mask_idx
            masked_input[corrupt] = replacements
            x = self.minibert(masked_input)
        else:
            x = self.minibert(input)

        x = self.l1(x)
        x = self.activation_fun(x)
        x = self.l2(x)

        if self.training:
            labels = input.detach().clone()
            labels[~masked] = -1

            loss_fn = nn.CrossEntropyLoss(ignore_index=-1)
            loss = loss_fn(x.view(-1, self._voc_size), labels.view(-1))
            return (x, loss)
        else:
            return x


class MiniBertForRegression(nn.Module):
    def __init__(self, configuration):
        super().__init__()
        self.minibert = MiniBert(configuration)
        self.configuration = configuration

        self._voc_size = len(configuration.vocabulary)
        self._embedding_dim = configuration.embedding_dim

        self.l1 = nn.Linear(self._embedding_dim,
                            configuration.first_layer_output_size, bias=False)
        self.activation_fun = parse_activation_function(
            configuration.activation_fun)
        self.l2 = nn.Linear(
            configuration.first_layer_output_size, configuration.output_size, bias=True)

    def forward(self, input):
        x = self.minibert(input)

        x = self.l1(x)
        x = self.activation_fun(x)
        x = self.l2(x)
        return x
