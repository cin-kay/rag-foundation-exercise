import sys
from typing import Dict, List, cast

import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer

from .base import BaseVectorStore
from .node import TextNode, VectorStoreQueryResult

logger.add(
    sink=sys.stdout,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
)


class SemanticVectorStore(BaseVectorStore):
    """Semantic Vector Store using SentenceTransformer embeddings."""

    saved_file: str = "rag-foundation/data/test_db_00.csv"
    embed_model_name: str = "all-MiniLM-L6-v2"
    embed_model: SentenceTransformer = SentenceTransformer(embed_model_name)

    def __init__(self, **data):
        super().__init__(**data)
        self._setup_store()

    def get(self, text_id: str) -> TextNode:
        """Get node."""
        try:
            return self.node_dict[text_id]
        except KeyError:
            logger.error(f"Node with id `{text_id}` not found.")
            return None

    def add(self, nodes: List[TextNode]) -> List[str]:
        """Add nodes to index."""
        for node in nodes:
            if node.embedding is None:
                logger.info(
                    "Found node without embedding, calculating "
                    f"embedding with model {self.embed_model_name}"
                )
                node.embedding = self._get_text_embedding(node.text)
            self.node_dict[node.id_] = node
        self._update_csv()  # Update CSV after adding nodes
        return [node.id_ for node in nodes]

    def _get_text_embedding(self, text: str) -> List[float]:
        """Calculate embedding."""
        return self.embed_model.encode(text).tolist()

    def delete(self, node_id: str, **delete_kwargs: Dict) -> None:
        """Delete nodes using node_id."""
        if node_id in self.node_dict:
            del self.node_dict[node_id]
            self._update_csv()  # Update CSV after deleting nodes
        else:
            logger.error(f"Node with id `{node_id}` not found.")

    def _calculate_similarity(
        self,
        query_embedding: List[float],
        doc_embeddings: List[List[float]],
        doc_ids: List[str],
        similarity_top_k: int = 3,
    ) -> float:
        """Get top nodes by similarity to the query."""
        qembed_np = np.array(query_embedding)
        dembed_np = np.array(doc_embeddings)
        dproduct_arr = np.dot(dembed_np, qembed_np)
        norm_arr = np.linalg.norm(qembed_np) * np.linalg.norm(
            dembed_np, axis=1, keepdims=False
        )
        cos_sim_arr = dproduct_arr / norm_arr

        sorted_tups = sorted(
            [(cos_sim_arr[i], doc_ids[i]) for i in range(len(doc_ids))],
            key=lambda t: t[0],
            reverse=True,
        )[:similarity_top_k]

        result_similarities = [s for s, _ in sorted_tups]
        result_ids = [n for _, n in sorted_tups]
        return result_similarities, result_ids

    def query(self, query: str, top_k: int = 3) -> VectorStoreQueryResult:
        """Query similar nodes."""
        query_embedding = cast(List[float], self._get_text_embedding(query))
        doc_embeddings = [node.embedding for node in self.node_dict.values()]
        doc_ids = list(self.node_dict.keys())
        if len(doc_embeddings) == 0:
            logger.error("No documents found in the index.")
            result_nodes, similarities, node_ids = [], [], []
        else:
            similarities, node_ids = self._calculate_similarity(
                query_embedding, doc_embeddings, doc_ids, top_k
            )
            result_nodes = [self.node_dict[node_id] for node_id in node_ids]
        return VectorStoreQueryResult(
            nodes=result_nodes, similarities=similarities, ids=node_ids
        )

    def batch_query(
        self, query: List[str], top_k: int = 3
    ) -> List[VectorStoreQueryResult]:
        """Batch query similar nodes."""
        return [self.query(q, top_k) for q in query]
