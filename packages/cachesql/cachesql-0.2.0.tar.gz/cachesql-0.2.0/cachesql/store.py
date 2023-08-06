import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Tuple, Union
from zipfile import ZipFile

import pandas as pd

from . import serializer
from .utils import normalize_query


def hash_query(query: str, normalize: bool = False) -> str:
    """Return the hash of a query. Normalized or not."""
    if normalize:
        query = normalize_query(query)

    return hashlib.sha1(query.encode()).hexdigest()


class BaseStore:
    pass


class FileStore(BaseStore):
    """Flat file store.

    Parameters
    ----------
    cache_store
        Root path where the cached files are stored.
    normalize
        If True, normalize the queries to make the cache independent from
        formatting changes. Normalization is done with the sqlparse library.
    compression
        Optional compression parameter to be passed to the serializer.

    """

    _serializers = {
        "parquet": serializer.ParquetSerializer,
        "joblib": serializer.JoblibSerializer,
    }

    def __init__(
        self,
        cache_store: Path,
        backend: str = "parquet",
        normalize: bool = False,
        compression: Any = None,
    ) -> None:
        if backend not in self._serializers:
            raise ValueError(
                f"store_backend={backend!r} is invalid. Choose one of {'parquet', 'joblib'}"
            )
        self.serializer = self._serializers[backend](compression=compression)
        self.cache_store = Path(cache_store).expanduser() / self.serializer.fmt
        self.cache_store.mkdir(parents=True, exist_ok=True)
        self.normalize = normalize

    def exists(self, query: str) -> bool:
        """Return True if the results of the given query exist in cache."""
        metadata_file = self.get_metadata_filepath(query)
        cache_file = self.get_cache_filepath(query)
        return metadata_file.exists() and cache_file.exists()

    def get_metadata_filepath(self, query: str) -> Path:
        """Return the metadata filepath corresponding to that query."""
        arg_hash = hash_query(query, normalize=self.normalize)
        return self.cache_store / (arg_hash + ".json")

    def get_cache_filepath(self, query: str) -> Path:
        """Return the cached results filepath corresponding to that query."""
        arg_hash = hash_query(query, normalize=self.normalize)
        return self.cache_store / (arg_hash + self.serializer.extension)

    def load_metadata(self, query: str) -> dict:
        """Load metadata of cached results for query if it exists in cache."""
        metadata_file = self.get_metadata_filepath(query)
        if metadata_file.exists():
            return json.loads(metadata_file.read_text())
        else:
            raise ValueError("Metadata for the given query does not exist.")

    def load_results(self, query: str) -> pd.DataFrame:
        """Load cached results for query if it exists in cache."""
        cache_file = self.get_cache_filepath(query)
        if cache_file.exists():
            return self.serializer.load(cache_file)
        else:
            raise ValueError("Cached results for the given query do not exist.")

    def load(self, query: str) -> Tuple[pd.DataFrame, dict]:
        """Load results and metadata for a query if they exist in cache."""
        return self.load_results(query), self.load_metadata(query)

    def dump_metadata(self, query: str, metadata: dict) -> None:
        """Dump metadata of query results to cache."""
        metadata["cache_file"] = self.get_cache_filepath(query).name
        metadata["query"] = normalize_query(query) if self.normalize else query
        metadata_file = self.get_metadata_filepath(query)
        metadata_file.write_text(json.dumps(metadata, indent=True))

    def dump_results(self, query: str, results: pd.DataFrame) -> None:
        """Dump query results to cache."""
        cache_file = self.get_cache_filepath(query)
        self.serializer.dump(results, cache_file)

    def dump(self, query: str, results: pd.DataFrame, metadata: dict) -> None:
        """Dump results and metadata for given query to cache."""
        self.dump_results(query, results)
        self.dump_metadata(query, metadata)

    def list(self) -> pd.DataFrame:
        """List cached function calls with some useful metadata."""
        # List everything first
        cache_list = [
            json.loads(f.read_text()) for f in self.cache_store.glob("*.json")
        ]

        if len(cache_list) == 0:
            default_metadata = [
                "query",
                "cache_file",
                "executed_at",
                "duration",
            ]
            return pd.DataFrame(columns=default_metadata)

        return pd.DataFrame(cache_list)

    def export(self, filename: Union[str, Path], queries: Iterable = None) -> None:
        """Export contents of cache to a zip file.

        Used in conjunction with the :py:meth:`Cache.import_cache <Cache.import_cache>` method,
        you can share your cache with your colleagues in order to guarantee reproducibility of
        your code. Or you can simply use it to migrate your cache from one environment to the
        other.

        Parameters
        ----------
        filename
            Path to a zip file where cache will be exported
        queries
            List of queries to be exported (Optional). If None, all cache contents will
            be exported.
        """
        queries = queries or self.list().loc[:, "query"]
        filename = Path(filename)
        filename = filename.with_suffix(".zip") if filename.suffix == "" else filename
        with ZipFile(filename, "w") as myzip:
            for query in queries:
                cache_file = self.get_cache_filepath(query)
                metadata_file = self.get_metadata_filepath(query)
                myzip.write(str(cache_file), arcname=Path(cache_file).name)
                myzip.write(str(metadata_file), arcname=Path(metadata_file).name)

    def import_cache(self, filename: Union[str, Path]) -> None:
        """Import contents to cache.

        Used in conjunction with the :py:meth:`Cache.export <Cache.export>` method,
        you can share your cache with your colleagues in order to guarantee reproducibility of
        your code. Or you can simply use it to migrate your cache from one environment to the
        other.

        Parameters
        ----------
        filename : Union[str, Path]
            Path to a zip file containing a previously exported cache
        """
        with ZipFile(filename, "r") as myzip:
            myzip.extractall(path=self.cache_store)
