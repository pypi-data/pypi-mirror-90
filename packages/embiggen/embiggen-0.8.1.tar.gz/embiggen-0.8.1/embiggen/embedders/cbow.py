"""CBOW model for graph and words embedding."""
from typing import Union, Tuple
from tensorflow.keras.optimizers import Optimizer   # pylint: disable=import-error
from tensorflow.keras.layers import Layer   # pylint: disable=import-error
from .node2vec import Node2Vec


class CBOW(Node2Vec):
    """CBOW model for graph and words embedding.

    The CBOW model for graoh embedding receives a list of contexts and tries
    to predict the central word. The model makes use of an NCE loss layer
    during the training process to generate the negatives.
    """

    def __init__(
        self,
        vocabulary_size: int,
        embedding_size: int,
        optimizer: Union[str, Optimizer] = "nadam",
        window_size: int = 4,
        negative_samples: int = 10
    ):
        """Create new CBOW-based Embedder object.

        Parameters
        -------------------------------------------
        vocabulary_size: int,
            Number of terms to embed.
            In a graph this is the number of nodes, while in a text is the
            number of the unique words.
        embedding_size: int,
            Dimension of the embedding.
        optimizer: Union[str, Optimizer] = "nadam",
            The optimizer to be used during the training of the model.
        window_size: int = 4,
            Window size for the local context.
            On the borders the window size is trimmed.
        negative_samples: int,
            The number of negative classes to randomly sample per batch.
            This single sample of negative classes is evaluated for each element in the batch.
        """
        super().__init__(
            vocabulary_size=vocabulary_size,
            embedding_size=embedding_size,
            model_name="CBOW",
            optimizer=optimizer,
            window_size=window_size,
            negative_samples=negative_samples
        )

    def _get_true_input_length(self) -> int:
        """Return length of true input layer."""
        return self._window_size*2

    def _get_true_output_length(self) -> int:
        """Return length of true output layer."""
        return 1

    def _sort_input_layers(
        self,
        true_input_layer: Layer,
        true_output_layer: Layer
    ) -> Tuple[Layer, Layer]:
        """Return input layers for training with the same input sequence.

        Parameters
        ----------------------------
        true_input_layer: Layer,
            The input layer that will contain the true input.
        true_output_layer: Layer,
            The input layer that will contain the true output.

        Returns
        ----------------------------
        Return tuple with the tuple of layers.
        """
        return (
            true_input_layer,
            true_output_layer
        )
