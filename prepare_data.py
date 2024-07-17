from pathlib import Path

from llama_index.readers.file.pymu_pdf import PyMuPDFReader

loader = PyMuPDFReader()
documents = loader.load(file_path=Path("./rag-foundation/data/llama2.pdf"))

from llama_index.core.node_parser import SentenceSplitter

node_parser = SentenceSplitter(chunk_size=256)
nodes = node_parser.get_nodes_from_documents(documents)
