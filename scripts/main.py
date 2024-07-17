from pathlib import Path

from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file.pymu_pdf import PyMuPDFReader

from ..vector_store.node import TextNode, VectorStoreQueryResult
from ..vector_store.semantic_vector_store import SemanticVectorStore
from ..vector_store.sparse_vector_store import SparseVectorStore


def prepare_data_nodes(
    pdf_path: str | Path = Path("./rag-foundation/data/llama2.pdf"),
) -> list[TextNode]:
    loader = PyMuPDFReader()
    documents = loader.load(file_path=pdf_path)
    node_parser = SentenceSplitter(chunk_size=512)
    nodes = node_parser.get_nodes_from_documents(documents)
    text_node = [
        TextNode(id_=str(id_), text=node.text, metadata=node.metadata)
        for id_, node in enumerate(nodes)
    ]
    return text_node


def prepare_vector_store(pdf_path: str, mode: str, force_index=False):
    if mode == "sparse":
        vector_store = SparseVectorStore(
            persist=True,
            saved_file="rag-foundation/data/sparse.csv",
            metadata_file="rag-foundation/data/sparse_metadata.json",
            force_index=force_index,
        )
    elif mode == "semantic":
        vector_store = SemanticVectorStore(
            persist=True,
            saved_file="rag-foundation/data/dense.csv",
            force_index=force_index,
        )
    else:
        raise ValueError("Invalid mode. Choose either `sparse` or `semantic`.")

    if force_index:
        nodes = prepare_data_nodes(pdf_path)
        vector_store.add(nodes)

    return vector_store


class RAGPipeline:
    def __init__(self, vector_store: SemanticVectorStore, prompt_template: str):
        self.vector_store = vector_store
        self.prompt_template = prompt_template

    def retrieve(self, query: str, top_k: int = 5) -> VectorStoreQueryResult:
        query_result = self.vector_store.query(query, top_k=top_k)
        return query_result

    def answer(self, query: str, top_k: int = 5):
        pass


if __name__ == "__main__":
    pdf_path = Path("./rag-foundation/data/llama2.pdf")
    vector_store = prepare_vector_store(pdf_path, mode="semantic")
    prompt_template = """Question: {query} \nAnswer:"""
    rag_pipeline = RAGPipeline(vector_store, prompt_template=prompt_template)

    query = "What is the name of the author?"
    result = rag_pipeline.retrieve(query)
    print(result)
