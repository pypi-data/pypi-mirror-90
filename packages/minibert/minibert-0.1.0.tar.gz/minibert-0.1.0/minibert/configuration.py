from minibert.modules import AttentionType, PositionEmbeddingType

__all__ = [
    "MiniBertConfiguration",
    "MiniBertForMLMConfiguration",
    "MiniBertForRegressionConfiguration",
]


class MiniBertConfiguration:
    def __init__(self, **kwargs):
        self.vocabulary = kwargs["vocabulary"]

        # Attention configuration
        self.embedding_dim = kwargs.get("embedding_dim", 64)
        self.hidden_dim = kwargs.get("hidden_dim", self.embedding_dim)
        self.key_is_query = kwargs.get("key_is_query", False)
        self.attention_type = kwargs.get(
            "attention_type", AttentionType.SelfAttention)

        # Embeddings configuration
        self.position_embeddings_count = kwargs.get(
            "position_embeddings_count", 1024)
        self.position_type = kwargs.get(
            "position_type", PositionEmbeddingType.TRAINED)
        self.normalize_embeddings = kwargs.get(
            "normalize_embeddings", True)


class MiniBertForMLMConfiguration(MiniBertConfiguration):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mask_idx = kwargs["mask_idx"]
        self.mask_token = kwargs.get("mask_token", "<mask>")

        # Masking strategy
        self.mask_prob = kwargs.get("mask_prob", 0.15)
        self.keep_mask_prob = kwargs.get("keep_mask_prob", 0.8)
        self.corrupt_mask_prob = kwargs.get("corrupt_mask_prob", 0.1)
        self.reveal_mask_prob = kwargs.get("reveal_mask_prob", 0.1)

        if self.keep_mask_prob + self.corrupt_mask_prob + self.reveal_mask_prob != 1:
            raise ValueError("Sum of masking strategies is not 1")

        # Prediction layers
        self.first_layer_output_size = kwargs.get(
            "first_layer_output_size", self.embedding_dim)
        self.activation_fun = kwargs.get("activation_fun", "gelu")


class MiniBertForRegressionConfiguration(MiniBertConfiguration):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Prediction layers
        self.first_layer_output_size = kwargs.get(
            "first_layer_output_size", self.embedding_dim)
        self.activation_fun = kwargs.get("activation_fun", "gelu")
        self.output_size = kwargs["output_size"]
