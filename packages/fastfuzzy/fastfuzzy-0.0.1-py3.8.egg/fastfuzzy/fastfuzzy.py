from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import IO, Callable, Collection, Dict, List, Optional, Set, Tuple, Union

from abydos.tokenizer import QGrams
from tqdm import tqdm

from .settings import DEFAULT_CMP, DEFAULT_Q, N_CANDIDATES


def _lowercase_strip(s: str) -> str:
    """Strip leading and trailing whitespace, and lowercase.

    Args:
        s (str): a string

    Returns:
        str: a cleaned string
    """
    return s.strip().casefold()


class QGramIndex:
    def __init__(
        self,
        tokens: Collection[str],
        q: int = DEFAULT_Q,
        cmp=DEFAULT_CMP,
        transform_f: Callable[[str], str] = _lowercase_strip,
    ) -> None:
        """Construct a q-gram index object.

        Args:
            tokens (Collection[str]): a collection (e.g. a list) of tokens to index
            q (int, optional): The character q-gram length. Defaults to DEFAULT_Q (3).
            cmp ([type], optional): A distance comparison class from abydos.distance.
                Defaults to abydos.distance.QGram.
            transform_f (Callable[[str], str], optional): a function to be applied to each token.
                Defaults to _lowercase_strip.

        Raises:
            ValueError: if no tokens for indexing are specified.
        """
        if not tokens:
            raise ValueError("No tokens for indexing specified.")

        super().__init__()

        self._q = q

        self._token_set: Set[str] = set(tokens)
        self._token_list: List[str] = list(self._token_set)

        self._transform: Callable[[str], str] = transform_f

        self._tokenizer = QGrams(qval=q)
        self._cmp = cmp(tokenizer=self._tokenizer)

        self._qgram_index: Dict[str, List[int]] = self._build_index()

    def __add__(self, other: "QGramIndex") -> "QGramIndex":
        """Merge two QGramIndex objects.

        Create a new index based on the tokens of both indices, eliminating duplicate entries.
        The q values of both indices must be identical.

        Args:
            other (QGramIndex): a QGramIndex object

        Raises:
            ValueError: if the q values of the two indices differ

        Returns:
            QGramIndex: a new QGramIndex object containing all elements from both input indices.
        """
        if not self._q == other._q:
            raise ValueError(
                f"Cannot merge indices with different q's ({self._q}, {other._q})."
            )

        return QGramIndex(q=self._q, tokens=self._token_set.union(other._token_set))

    def __len__(self):
        """Get the number of tokens in the index.

        Returns:
            int: the number of tokens
        """
        return len(self._token_list)

    def _build_index(self) -> Dict[str, List[int]]:
        """Build q-gram index.

        Returns:
            Dict[str, List[int]]: an inverse index pointing from each q-gram to the tokens in which it occurs.
        """
        index = defaultdict(list)

        for i, token in enumerate(
            tqdm(self._token_list, desc="Building index", unit="tok", unit_scale=True)
        ):
            for qgram in self._tokenizer.tokenize(self._transform(token)).get_list():
                index[qgram].append(i)
        return index

    def _candidates(self, token: str, n: int = N_CANDIDATES) -> List[str]:
        """Retrieve candidate strings from index for exact distance measuring.

        Args:
            token (str): a token to get similar candidates for
            n (int, optional): [description]. Defaults to 100.

        Returns:
            List[str]: a list of tokens with largest q-gram overlap
        """
        qgram_overlap: Counter = Counter()
        for qgram in self._tokenizer.tokenize(self._transform(token)).get_list():
            for candidate_i in self._qgram_index[qgram]:
                qgram_overlap[candidate_i] += 1
        return [
            self._token_list[candidate_i]
            for candidate_i, count in qgram_overlap.most_common(n)
        ]

    @lru_cache(maxsize=128)
    def max_sim(self, token: str) -> Tuple[Optional[str], float]:
        """Find the index entry with maximum string similarity.

        Args:
            token (str): a string

        Returns:
            Tuple[str, float]: the most similar index entry with similarity value.
                If there is no q-gram overlap at all, returns (None, 0.0)
        """

        if token in self._token_set:
            return (token, 1.0)
        else:
            return max(
                (
                    (
                        candidate,
                        self._cmp.sim(
                            self._transform(token), self._transform(candidate)
                        ),
                    )
                    for candidate in self._candidates(token)
                ),
                key=lambda token_sim: token_sim[1],
                default=(None, 0.0),
            )

    @classmethod
    def from_file(
        cls,
        file: IO,
        q: int = DEFAULT_Q,
        cmp=DEFAULT_CMP,
        transform_f: Callable[[str], str] = _lowercase_strip,
    ):
        """Initialize a QGramIndex object from an IO file object.

        The tokens read from the file are used for the initial token list.

        Args:
            file (IO): an open input stream
            q (int, optional): the q value to use.
                Defaults to DEFAULT_Q (3).

        Returns:
            QGramIndex: an object initialized with the tokens read from the file.
        """
        return cls(
            tokens={line.strip() for line in file.readlines() if line.strip()},
            q=q,
            cmp=cmp,
            transform_f=transform_f,
        )

    @classmethod
    def from_path(
        cls,
        filename: Union[Path, str],
        q: int = DEFAULT_Q,
        cmp=DEFAULT_CMP,
        transform_f: Callable[[str], str] = _lowercase_strip,
    ):
        """Initialize a QGramIndex object from a file path.

        Args:
            filename (Union[Path, str]): a path to a file
            q (int, optional): the q value to use.
                Defaults to DEFAULT_Q (3).

        Returns:
            QGramIndex: an object initialized with the tokens read from the file.
        """
        with open(filename) as file:
            return cls.from_file(file=file, q=q, cmp=cmp, transform_f=transform_f)
