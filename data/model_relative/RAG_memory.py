import os
from pathlib import Path
import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.memory.chromadb import ChromaDBVectorMemory, PersistentChromaDBVectorMemoryConfig


from data.model_relative.document_indexer import SimpleDocumentIndexer


async def setup_memory():
    # Initialize vector memory
    rag_memory = ChromaDBVectorMemory(
        config=PersistentChromaDBVectorMemoryConfig(
            collection_name="autogen_docs",
            persistence_path=os.path.join(str(Path.home()), ".chromadb_autogen"),
            k=3,  # Return top 3 results
            score_threshold=0.4,  # Minimum similarity score
        )
    )

    await rag_memory.clear()  # Clear existing memory
    return rag_memory

async def index_autogen_docs(rag_memory) -> None:
    indexer = SimpleDocumentIndexer(memory=rag_memory)
    sources = [
        "https://raw.githubusercontent.com/microsoft/autogen/main/README.md",
        "https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/tutorial/agents.html",
        "https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/tutorial/teams.html",
        "https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/tutorial/termination.html",
    ]
    chunks: int = await indexer.index_documents(sources)
    print(f"Indexed {chunks} chunks from {len(sources)} AutoGen documents")
    print(rag_memory)

async def main():
    rag_memory = await setup_memory()
    await index_autogen_docs(rag_memory)
    # 在这里可以使用rag_memory进行其他操作

if __name__ == "__main__":
    asyncio.run(main())
