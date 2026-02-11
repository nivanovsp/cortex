"""
Cortex Memory System

Manages atomic learnings from past sessions with CRUD operations
and similarity-based relationship discovery.
"""

import os
import json
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, Literal
from enum import Enum
import numpy as np

from .config import Config
from .embedder import embed_passage
from .utils import parse_frontmatter, extract_keywords


class MemoryType(str, Enum):
    """Types of memories."""
    FACTUAL = "factual"           # Stable knowledge
    EXPERIENTIAL = "experiential"  # Lessons learned
    PROCEDURAL = "procedural"      # How to do something


class Confidence(str, Enum):
    """Confidence levels for memories."""
    HIGH = "high"      # Verified fixes, explicit "remember this"
    MEDIUM = "medium"  # Reasonable inference
    LOW = "low"        # Uncertain, needs verification


@dataclass
class Memory:
    """Represents an atomic learning/memory."""
    id: str
    type: str
    domain: str
    confidence: str
    keywords: list[str]
    learning: str
    context: str
    source_session: Optional[str] = None
    source_task: Optional[str] = None
    trigger: Optional[str] = None
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    updated: str = field(default_factory=lambda: datetime.now().isoformat())
    verified: bool = False
    retrieval_count: int = 0
    last_retrieved: Optional[str] = None
    usefulness_score: float = 0.5


def get_memories_path(project_root: str) -> str:
    """Get the memories directory path."""
    return os.path.join(project_root, Config.CORTEX_DIR, Config.MEMORIES_DIR)


def get_next_memory_id(memories_path: str) -> str:
    """Generate the next memory ID based on date and sequence."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Find existing memories for today
    # Format: MEM-YYYY-MM-DD-SEQ (e.g., MEM-2026-01-26-001)
    seq = 1
    if os.path.exists(memories_path):
        for f in os.listdir(memories_path):
            if f.startswith(f"MEM-{today}") and f.endswith('.md'):
                # Parse sequence number - it's the last segment after the date
                # MEM-2026-01-26-001.md -> sequence is 001
                filename = f.replace('.md', '')
                # Split from the right to get the sequence
                parts = filename.rsplit('-', 1)
                if len(parts) == 2:
                    try:
                        existing_seq = int(parts[1])
                        seq = max(seq, existing_seq + 1)
                    except ValueError:
                        pass

    return f"MEM-{today}-{seq:03d}"


def create_memory(
    learning: str,
    context: str = "",
    memory_type: str = "experiential",
    domain: str = "GENERAL",
    confidence: str = "medium",
    source_session: Optional[str] = None,
    source_task: Optional[str] = None,
    trigger: Optional[str] = None,
    project_root: str = "."
) -> Memory:
    """
    Create a new memory.

    Args:
        learning: The core learning/insight
        context: Additional context about when/how this was learned
        memory_type: factual, experiential, or procedural
        domain: Domain tag (e.g., AUTH, UI, API)
        confidence: high, medium, or low
        source_session: Session identifier
        source_task: Task that triggered this learning
        trigger: What triggered saving this memory
        project_root: Project root directory

    Returns:
        Created Memory object
    """
    project_root = os.path.abspath(project_root)
    memories_path = get_memories_path(project_root)
    os.makedirs(memories_path, exist_ok=True)

    # Generate ID
    memory_id = get_next_memory_id(memories_path)

    # Extract keywords from learning + context
    full_text = f"{learning}\n{context}"
    keywords = extract_keywords(full_text)

    # Create memory object
    memory = Memory(
        id=memory_id,
        type=memory_type,
        domain=domain.upper(),
        confidence=confidence,
        keywords=keywords,
        learning=learning,
        context=context,
        source_session=source_session,
        source_task=source_task,
        trigger=trigger
    )

    # Save to disk
    save_memory(memory, memories_path)

    print(f"Created memory: {memory_id}")
    print(f"  Type: {memory_type}")
    print(f"  Domain: {domain}")
    print(f"  Confidence: {confidence}")

    return memory


def save_memory(memory: Memory, memories_path: str):
    """Save memory to disk as .md file with embedding."""
    # Build frontmatter
    frontmatter = f"""---
id: {memory.id}
type: {memory.type}
domain: {memory.domain}
confidence: {memory.confidence}
keywords: {json.dumps(memory.keywords)}
source_session: {json.dumps(memory.source_session)}
source_task: {json.dumps(memory.source_task)}
trigger: {json.dumps(memory.trigger)}
created: "{memory.created}"
updated: "{memory.updated}"
verified: {str(memory.verified).lower()}
retrieval_count: {memory.retrieval_count}
last_retrieved: {json.dumps(memory.last_retrieved)}
usefulness_score: {memory.usefulness_score}
---

## Learning

{memory.learning}

## Context

{memory.context}
"""

    # Save markdown file
    md_path = os.path.join(memories_path, f"{memory.id}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    # Generate and save embedding
    embedding_text = f"{memory.learning}\n{memory.context}"
    embedding = embed_passage(embedding_text)
    npy_path = os.path.join(memories_path, f"{memory.id}.npy")
    np.save(npy_path, embedding)


def parse_memory_file(md_path: str) -> Optional[Memory]:
    """Parse a memory from its markdown file."""
    if not os.path.exists(md_path):
        return None

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter
    if not content.startswith('---'):
        return None

    end_idx = content.find('---', 3)
    if end_idx == -1:
        return None

    body = content[end_idx + 3:].strip()
    meta = parse_frontmatter(content)

    # Parse body sections
    learning = ""
    context = ""

    if "## Learning" in body:
        parts = body.split("## Learning", 1)
        if len(parts) > 1:
            rest = parts[1]
            if "## Context" in rest:
                learning_part, context_part = rest.split("## Context", 1)
                learning = learning_part.strip()
                context = context_part.strip()
            else:
                learning = rest.strip()

    return Memory(
        id=meta.get('id', ''),
        type=meta.get('type', 'experiential'),
        domain=meta.get('domain', 'GENERAL'),
        confidence=meta.get('confidence', 'medium'),
        keywords=meta.get('keywords', []),
        learning=learning,
        context=context,
        source_session=meta.get('source_session'),
        source_task=meta.get('source_task'),
        trigger=meta.get('trigger'),
        created=meta.get('created', ''),
        updated=meta.get('updated', ''),
        verified=meta.get('verified', False),
        retrieval_count=meta.get('retrieval_count', 0),
        last_retrieved=meta.get('last_retrieved'),
        usefulness_score=meta.get('usefulness_score', 0.5)
    )


def get_memory(memory_id: str, project_root: str = ".") -> Optional[Memory]:
    """Get a specific memory by ID."""
    project_root = os.path.abspath(project_root)
    memories_path = get_memories_path(project_root)
    md_path = os.path.join(memories_path, f"{memory_id}.md")
    return parse_memory_file(md_path)


def list_memories(
    project_root: str = ".",
    domain: Optional[str] = None,
    memory_type: Optional[str] = None,
    confidence: Optional[str] = None
) -> list[Memory]:
    """
    List all memories, optionally filtered.

    Args:
        project_root: Project root directory
        domain: Filter by domain
        memory_type: Filter by type
        confidence: Filter by confidence level

    Returns:
        List of Memory objects
    """
    project_root = os.path.abspath(project_root)
    memories_path = get_memories_path(project_root)

    if not os.path.exists(memories_path):
        return []

    memories = []
    for f in os.listdir(memories_path):
        if not f.endswith('.md'):
            continue

        md_path = os.path.join(memories_path, f)
        memory = parse_memory_file(md_path)

        if memory is None:
            continue

        # Apply filters
        if domain and memory.domain.upper() != domain.upper():
            continue
        if memory_type and memory.type != memory_type:
            continue
        if confidence and memory.confidence != confidence:
            continue

        memories.append(memory)

    # Sort by created date descending
    memories.sort(key=lambda m: m.created, reverse=True)
    return memories


def update_memory(
    memory_id: str,
    project_root: str = ".",
    confidence: Optional[str] = None,
    verified: Optional[bool] = None,
    usefulness_score: Optional[float] = None,
    learning: Optional[str] = None,
    context: Optional[str] = None
) -> Optional[Memory]:
    """
    Update an existing memory.

    Args:
        memory_id: Memory ID to update
        project_root: Project root directory
        confidence: New confidence level
        verified: New verified status
        usefulness_score: New usefulness score
        learning: Updated learning content
        context: Updated context

    Returns:
        Updated Memory object, or None if not found
    """
    project_root = os.path.abspath(project_root)
    memories_path = get_memories_path(project_root)

    memory = get_memory(memory_id, project_root)
    if memory is None:
        print(f"Memory not found: {memory_id}")
        return None

    # Apply updates
    if confidence is not None:
        memory.confidence = confidence
    if verified is not None:
        memory.verified = verified
    if usefulness_score is not None:
        memory.usefulness_score = usefulness_score
    if learning is not None:
        memory.learning = learning
        memory.keywords = extract_keywords(f"{learning}\n{memory.context}")
    if context is not None:
        memory.context = context
        memory.keywords = extract_keywords(f"{memory.learning}\n{context}")

    memory.updated = datetime.now().isoformat()

    # Re-save
    save_memory(memory, memories_path)

    print(f"Updated memory: {memory_id}")
    return memory


def delete_memory(memory_id: str, project_root: str = ".") -> bool:
    """
    Delete a memory.

    Args:
        memory_id: Memory ID to delete
        project_root: Project root directory

    Returns:
        True if deleted, False if not found
    """
    project_root = os.path.abspath(project_root)
    memories_path = get_memories_path(project_root)

    md_path = os.path.join(memories_path, f"{memory_id}.md")
    npy_path = os.path.join(memories_path, f"{memory_id}.npy")

    if not os.path.exists(md_path):
        print(f"Memory not found: {memory_id}")
        return False

    os.remove(md_path)
    if os.path.exists(npy_path):
        os.remove(npy_path)

    print(f"Deleted memory: {memory_id}")
    return True


def increment_retrieval(memory_id: str, project_root: str = "."):
    """Increment retrieval count for a memory."""
    memory = get_memory(memory_id, project_root)
    if memory:
        memory.retrieval_count += 1
        memory.last_retrieved = datetime.now().isoformat()
        memories_path = get_memories_path(os.path.abspath(project_root))
        save_memory(memory, memories_path)


def find_related_memories(
    memory_id: str,
    project_root: str = ".",
    top_k: int = 5
) -> list[tuple[Memory, float]]:
    """
    Find memories related to a given memory via embedding similarity.

    Args:
        memory_id: Source memory ID
        project_root: Project root directory
        top_k: Number of related memories to return

    Returns:
        List of (Memory, similarity_score) tuples
    """
    project_root = os.path.abspath(project_root)
    memories_path = get_memories_path(project_root)

    # Load source memory embedding
    source_npy = os.path.join(memories_path, f"{memory_id}.npy")
    if not os.path.exists(source_npy):
        return []

    source_emb = np.load(source_npy)

    # Load all other memory embeddings and compute similarity
    results = []
    for f in os.listdir(memories_path):
        if not f.endswith('.npy') or f.startswith(memory_id):
            continue

        other_id = f.replace('.npy', '')
        other_npy = os.path.join(memories_path, f)
        other_emb = np.load(other_npy)

        # Cosine similarity (embeddings are normalized)
        similarity = float(np.dot(source_emb, other_emb))

        memory = get_memory(other_id, project_root)
        if memory:
            results.append((memory, similarity))

    # Sort by similarity and return top_k
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]


# CLI entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m core.memory <action> [args]")
        print("Actions: create, list, get, update, delete, related")
        sys.exit(1)

    action = sys.argv[1]

    if action == "list":
        memories = list_memories()
        for m in memories:
            print(f"{m.id} [{m.type}] ({m.confidence}): {m.learning[:50]}...")
    elif action == "create":
        if len(sys.argv) < 3:
            print("Usage: python -m core.memory create <learning> [context]")
            sys.exit(1)
        learning = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        create_memory(learning, context)
