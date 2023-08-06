"""Module offers basic Corpus Transformer object, a simple class to tekenize textual corpuses."""
import math
import string
from collections import Counter
from multiprocessing import Pool, cpu_count
from typing import Dict, Generator, List, Set

import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from tensorflow.keras.preprocessing.text import \
    Tokenizer  # pylint: disable=import-error
from tqdm.auto import tqdm


class CorpusTransformer:
    """Simple class to tekenize textual corpuses."""

    def __init__(
        self,
        synonyms: Dict = None,
        language: str = "english",
        apply_stemming: bool = True,
        remove_stop_words: bool = True,
        remove_punctuation: bool = True,
        remove_digits: bool = False,
        extra_stop_words: Set[str] = None,
        min_word_length: int = 2,
        min_sequence_length: int = 0,
        min_count: int = 0,
        max_count: int = math.inf,
        to_lower_case: bool = True,
        verbose: bool = True,
        processes: int = None
    ):
        """Create new CorpusTransformer object.

        This is a GENERIC text tokenizer and is only useful for basic examples
        as in any advanced settings there will be need for a custom tokenizer.

        Parameters
        ----------------------------
        synonyms: Dict = None,
            The synonyms to use.
        language: str = "english",
            The language for the stopwords.
        apply_stemming: bool = True,
            Wethever to apply or not a stemming procedure, which
            by default is enabled.
            The algorithm used is a Porter Stemmer.
        remove_stop_words: bool = True,
            Whether to remove stopwords,
            as defined from NLTK for the given language.
        remove_punctuation: bool = True,
            Whether to remove punctuation, as defined from the string package.
        remove_digits: bool = False,
            Whether to remove words composed of only digits.
        extra_stop_words: Set[str] = None,
            The additional stop words to be removed.
        min_word_length: int = 2,
            Minimum length of the corpus words.
        min_sequence_length: int = 0,
            Minimum length of the tokenized sequences.
            If you are using word2vec, the sequences MUST be longer than
            two times the window size plus one.
        min_count: int = 0,
            Whether to drop terms that appear less than the given amount.
        max_count: int = math.inf,
            Whether to drop terms that appear more than the given amount.
        to_lower_case: bool = True,
            Whether to convert terms to lowercase.
        processes: int = None,
            Number of parallel processes to use.
            If given processes is None, all the available processes is used.
        verbose: bool = True,
            Whether to show loading bars and log process.
        """
        self._synonyms = {} if synonyms is None else synonyms
        self._stopwords = set() if extra_stop_words is None else extra_stop_words
        if remove_stop_words:
            self._stopwords |= set(stopwords.words(language))
        if remove_punctuation:
            self._stopwords |= set(string.punctuation)
        self._remove_digits = remove_digits
        self._min_word_length = min_word_length
        self._min_count = min_count
        self._max_count = max_count
        self._min_sequence_length = min_sequence_length
        self._to_lower_case = to_lower_case
        self._processes = cpu_count() if processes is None else processes
        self._verbose = verbose
        self._stemmer = PorterStemmer() if apply_stemming else None
        self._tokenizer = None

    def get_synonym(self, word: str) -> str:
        """Return the synonym of the given word, if available.

        Parameters
        ----------------------------
        word: str,
            The word whose synonym is to be found.

        Returns
        ----------------------------
        The given word synonym.
        """
        return self._synonyms.get(word, word)

    def tokenize_line(self, line: str) -> List[str]:
        """Return tokenized line.

        Parameters
        ---------------------
        line: str,
            The line to be tokenized.

        Returns
        ---------------------
        The list of string tokens.
        """
        return [
            self._stemmer.stem(self.get_synonym(word))
            if self._stemmer is not None
            else self.get_synonym(word)
            for word in word_tokenize(line.lower() if self._to_lower_case else line)
            if word not in self._stopwords and
            len(word) > self._min_word_length and
            (not self._remove_digits or not word.isnumeric())
        ]

    def tokenize_lines(self, lines: List[str]) -> List[List[str]]:
        """Return tokenized lines.

        Parameters
        ---------------------
        lines: List[str],
            List of lines to be tokenized.

        Returns
        ---------------------
        The list of string tokens.
        """
        return [
            self.tokenize_line(line)
            for line in lines
        ]

    def tokenize(self, texts: List[str], return_counts: bool = False):
        """Fit model using stemming from given text.

        Parameters
        ----------------------------
        texts: List[str],
            The text to use to fit the transformer.
        return_counts: bool = False,
            Wethever to return the counts of the terms or not.

        Return
        -----------------------------
        Either the tokens or tuple containing the tokens and the counts.
        """
        processes = min(cpu_count(), len(texts))
        chunks_number = processes*2
        chunk_size = max(len(texts) // chunks_number, 1)
        with Pool(processes) as p:
            all_tokens = [
                line
                for chunk in tqdm(
                    p.imap(
                        self.tokenize_lines,
                        (texts[i:i + chunk_size]
                         for i in range(0, len(texts), chunk_size))
                    ),
                    desc="Tokenizing",
                    total=chunks_number,
                    disable=not self._verbose
                )
                for line in chunk
            ]
            p.close()
            p.join()

        if return_counts:
            counter = Counter((
                term
                for terms in tqdm(
                    all_tokens,
                    desc="Computing counts of terms",
                    disable=not self._verbose
                )
                for term in terms
            ))
            return all_tokens, counter
        return all_tokens

    def parse_tokens_for_low_frequency(self, tokens_list: List[List[str]]) -> Generator:
        """Yields tokens parsed according to updated stopwords.

        Parameters
        --------------------
        tokens_list: List[List[str]],
            List of the string tokens.

        Yields
        --------------------
        The filtered out tokens.
        """
        for tokens in tqdm(
            tokens_list,
            total=len(tokens_list),
            desc="Filtering low frequency terms",
            disable=not self._verbose
        ):
            new_tokens = [
                token
                for token in tokens
                if token not in self._stopwords
            ]
            if len(new_tokens) > 0:
                yield new_tokens

    def fit(self, texts: List[str]):
        """Fit the transformer.

        Parameters
        ----------------------------
        texts: List[str],
            The texts to use for the fitting.
        """
        tokens_list, counts = self.tokenize(texts, True)

        if self._min_count > 0 or math.isfinite(self._max_count):
            self._stopwords |= {
                word
                for word, count in counts.items()
                if count <= self._min_count or count >= self._max_count
            }
            tokens_list = self.parse_tokens_for_low_frequency(tokens_list)

        self._tokenizer = Tokenizer(
            lower=self._to_lower_case
        )
        self._tokenizer.fit_on_texts((
            " ".join(tokens)
            for tokens in tqdm(
                tokens_list,
                desc="Fitting tokenizer",
                total=len(texts),
                disable=not self._verbose
            )
        ))

    @property
    def vocabulary_size(self) -> int:
        """Return number of different terms."""
        return len(self._tokenizer.word_counts)

    def reverse_transform(self, sequences: np.ndarray) -> List[str]:
        """Reverse the sequence to texts.

        Parameters
        ------------------------
        sequences: np.ndarray,
            The sequences to counter transform.

        Returns
        ------------------------
        The texts created from the given sequences.
        """
        if isinstance(sequences, (list, tuple)):
            sequences = np.array(sequences)
        return self._tokenizer.sequences_to_texts(sequences + 1)

    def get_word_id(self, word: str) -> int:
        """Get the given words IDs.

        Parameters
        ------------------------
        word: int
            The word whose ID is to be retrieved.

        Returns
        ------------------------
        The word numeric ID.
        """
        return self._tokenizer.word_index[word] - 1

    def transform(self, texts: List[str]) -> np.ndarray:
        """Transform given text.

        Parameters
        --------------------------
        texts: List[str],
            The texts to encode as digits.

        Returns
        --------------------------
        Numpy array with numpy arrays of tokens.
        """
        return np.array([
            np.array(tokens, dtype=np.uint64) - 1
            for tokens in self._tokenizer.texts_to_sequences((
                " ".join(tokens)
                for tokens in tqdm(
                    self.tokenize(texts),
                    desc="Transform texts",
                    total=len(texts),
                    disable=not self._verbose
                )
                if len(tokens) >= self._min_sequence_length
            ))
        ], dtype=object)
