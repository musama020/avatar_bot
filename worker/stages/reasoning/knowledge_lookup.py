from worker import config
from worker.stages.reasoning.knowledge_chunker import MarkdownSectionChunker
from worker.stages.reasoning.knowledge_index import QdrantKnowledgeIndex
from worker.stages.reasoning.text_embedder import BgeM3Embedder


class KnowledgeLookup:
    """RAG: indexes the knowledge base and finds the passages for a question. Must stay under ~100 ms per search."""

    def __init__(self):
        self.embedder = BgeM3Embedder()
        self.index = QdrantKnowledgeIndex()

    def rebuild_index(self):
        markdown_text = config.KNOWLEDGE_BASE_PATH.read_text(encoding="utf-8")
        chunks = MarkdownSectionChunker().split(markdown_text)
        texts = []
        for chunk in chunks:
            texts.append(chunk.text_for_embedding())
        embeddings = self.embedder.embed(texts)
        self.index.rebuild(chunks, embeddings)
        return chunks

    def find_relevant_passages(self, search_query):
        """Returns no passages when even the closest match is too far in meaning; the reply then says 'contact the team'."""
        query_embedding = self.embedder.embed([search_query])[0]
        if self.index.best_dense_score(query_embedding) < config.RETRIEVAL_MIN_DENSE_SCORE:
            return []
        return self.index.hybrid_search(query_embedding, config.RETRIEVAL_TOP_K)
