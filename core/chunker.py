"""
Cortex Chunker

Semantic-aware markdown chunking with embedding generation.
"""

import os
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional
import numpy as np

from .config import Config
from .embedder import embed_passage


@dataclass
class Chunk:
    """Represents a document chunk."""
    id: str
    source_doc: str
    source_section: str
    source_lines: tuple[int, int]
    tokens: int
    keywords: list[str]
    content: str
    created: str
    source_path: str = ""
    source_hash: str = ""


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken (cl100k_base for GPT-4 compatibility)."""
    import tiktoken
    encoder = tiktoken.get_encoding("cl100k_base")
    return len(encoder.encode(text))


def extract_keywords(text: str, max_keywords: int = 10) -> list[str]:
    """
    Extract keywords from text using simple TF-based approach.

    For Phase 1, uses word frequency. Can be upgraded to TF-IDF later.
    """
    # Clean and tokenize
    text_lower = text.lower()
    # Remove markdown syntax, code blocks, etc.
    text_clean = re.sub(r'```[\s\S]*?```', '', text_lower)
    text_clean = re.sub(r'`[^`]+`', '', text_clean)
    text_clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text_clean)
    text_clean = re.sub(r'[#*_~`>\-|]', ' ', text_clean)

    # Tokenize
    words = re.findall(r'\b[a-z]{3,}\b', text_clean)

    # Filter stopwords
    stopwords = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
        'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been', 'were',
        'being', 'their', 'there', 'this', 'that', 'with', 'they', 'from',
        'will', 'would', 'could', 'should', 'which', 'when', 'where', 'what',
        'each', 'into', 'than', 'then', 'also', 'only', 'other', 'such',
        'more', 'some', 'very', 'just', 'about', 'over', 'after', 'before'
    }
    words = [w for w in words if w not in stopwords]

    # Count frequency
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    # Sort by frequency and return top keywords
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:max_keywords]]


def detect_domain(path: str) -> str:
    """
    Auto-detect domain from file path.

    Priority:
    1. Parent folder name (docs/auth/spec.md -> AUTH)
    2. Filename prefix before hyphen (auth-spec.md -> AUTH)
    3. Fallback to GENERAL
    """
    p = Path(path)

    # Try parent folder name (if not generic like 'docs')
    parent = p.parent.name.upper()
    if parent and parent not in ('DOCS', 'DOC', 'DOCUMENTATION', '.'):
        return parent

    # Try filename prefix before hyphen
    stem = p.stem
    if '-' in stem:
        prefix = stem.split('-')[0].upper()
        if len(prefix) >= 2:
            return prefix

    # Fallback
    return "GENERAL"


def get_next_doc_number(chunks_path: str, domain: str) -> int:
    """Get next document number for a domain."""
    domain_path = os.path.join(chunks_path, domain)
    if not os.path.exists(domain_path):
        return 1

    # Find existing doc numbers
    existing = set()
    for f in os.listdir(domain_path):
        if f.endswith('.md'):
            # Parse CHK-DOMAIN-DOC-SEQ.md
            parts = f.replace('.md', '').split('-')
            if len(parts) >= 4:
                try:
                    existing.add(int(parts[2]))
                except ValueError:
                    pass

    if not existing:
        return 1
    return max(existing) + 1


def parse_sections(content: str) -> list[dict]:
    """
    Parse markdown into sections based on headers.

    Returns list of {title, content, start_line, end_line}
    """
    lines = content.split('\n')
    sections = []
    current_section = None
    current_content = []
    current_start = 0

    for i, line in enumerate(lines):
        # Check for header (# ## ### etc)
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)

        if header_match:
            # Save previous section
            if current_section is not None or current_content:
                sections.append({
                    'title': current_section or 'Introduction',
                    'content': '\n'.join(current_content).strip(),
                    'start_line': current_start + 1,  # 1-indexed
                    'end_line': i  # exclusive
                })

            # Start new section
            current_section = header_match.group(2).strip()
            current_content = []
            current_start = i
        else:
            current_content.append(line)

    # Don't forget last section
    if current_section is not None or current_content:
        sections.append({
            'title': current_section or 'Introduction',
            'content': '\n'.join(current_content).strip(),
            'start_line': current_start + 1,
            'end_line': len(lines)
        })

    return sections


def split_by_paragraphs(text: str, max_tokens: int, overlap: int) -> list[str]:
    """
    Split text into chunks by paragraphs.

    Tries to keep paragraphs together, splits at sentence boundaries if needed.
    """
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_tokens = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        para_tokens = count_tokens(para)

        # If single paragraph exceeds max, split it
        if para_tokens > max_tokens:
            # Flush current chunk first
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = []
                current_tokens = 0

            # Split paragraph by sentences
            sentences = re.split(r'(?<=[.!?])\s+', para)
            sent_chunk = []
            sent_tokens = 0

            for sent in sentences:
                sent_tok = count_tokens(sent)
                if sent_tokens + sent_tok > max_tokens and sent_chunk:
                    chunks.append(' '.join(sent_chunk))
                    sent_chunk = []
                    sent_tokens = 0
                sent_chunk.append(sent)
                sent_tokens += sent_tok

            if sent_chunk:
                chunks.append(' '.join(sent_chunk))
            continue

        # Check if adding this paragraph exceeds limit
        if current_tokens + para_tokens > max_tokens and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_tokens = 0

        current_chunk.append(para)
        current_tokens += para_tokens

    # Flush remaining
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks


def add_overlap(chunks: list[str], overlap_tokens: int) -> list[str]:
    """Add overlap between consecutive chunks."""
    if len(chunks) <= 1 or overlap_tokens <= 0:
        return chunks

    result = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            result.append(chunk)
            continue

        # Get overlap from previous chunk
        prev_chunk = chunks[i - 1]
        prev_words = prev_chunk.split()

        # Estimate words for overlap (rough: 1.3 tokens per word)
        overlap_words = int(overlap_tokens / 1.3)
        if overlap_words > 0 and len(prev_words) > overlap_words:
            overlap_text = ' '.join(prev_words[-overlap_words:])
            chunk = f"...{overlap_text}\n\n{chunk}"

        result.append(chunk)

    return result


def chunk_document(
    path: str,
    project_root: str = ".",
    domain: Optional[str] = None,
    force: bool = False
) -> list[Chunk]:
    """
    Chunk a markdown document into semantic units.

    Args:
        path: Path to markdown file
        project_root: Project root directory
        domain: Optional domain override (auto-detected if not provided)
        force: Re-chunk even if chunks exist

    Returns:
        List of Chunk objects
    """
    path = os.path.abspath(path)
    project_root = os.path.abspath(project_root)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Document not found: {path}")

    # Auto-detect domain if not provided
    if domain is None:
        domain = detect_domain(path)

    # Setup paths
    chunks_path = Config.get_chunks_path(project_root)
    domain_path = os.path.join(chunks_path, domain)
    os.makedirs(domain_path, exist_ok=True)

    # Get document number
    doc_num = get_next_doc_number(chunks_path, domain)
    doc_id = f"DOC-{domain}-{doc_num:03d}"

    # Read document and compute hash
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    source_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

    # Store relative path for portability
    try:
        source_path = os.path.relpath(path, project_root)
    except ValueError:
        # On Windows, relpath fails across drives
        source_path = path

    # Parse into sections
    sections = parse_sections(content)

    # Process each section into chunks
    all_chunks = []
    chunk_seq = 1

    for section in sections:
        section_content = section['content']
        if not section_content.strip():
            continue

        section_tokens = count_tokens(section_content)

        # If section fits in one chunk, keep it together
        if section_tokens <= Config.CHUNK_SIZE:
            # Skip if too small
            if section_tokens < Config.CHUNK_MIN:
                continue

            text_chunks = [section_content]
        else:
            # Split by paragraphs
            text_chunks = split_by_paragraphs(
                section_content,
                Config.CHUNK_SIZE,
                Config.CHUNK_OVERLAP
            )

        # Add overlap between chunks
        text_chunks = add_overlap(text_chunks, Config.CHUNK_OVERLAP)

        # Create chunk objects
        for chunk_text in text_chunks:
            chunk_tokens = count_tokens(chunk_text)
            if chunk_tokens < Config.CHUNK_MIN:
                continue

            chunk_id = f"CHK-{domain}-{doc_num:03d}-{chunk_seq:03d}"
            chunk = Chunk(
                id=chunk_id,
                source_doc=doc_id,
                source_section=section['title'],
                source_lines=(section['start_line'], section['end_line']),
                tokens=chunk_tokens,
                keywords=extract_keywords(chunk_text),
                content=chunk_text,
                created=datetime.now().isoformat(),
                source_path=source_path,
                source_hash=source_hash
            )
            all_chunks.append(chunk)
            chunk_seq += 1

    # Save chunks
    for chunk in all_chunks:
        save_chunk(chunk, domain_path)

    print(f"Created {len(all_chunks)} chunks from {path}")
    print(f"  Domain: {domain}")
    print(f"  Doc ID: {doc_id}")
    print(f"  Chunks: {all_chunks[0].id} to {all_chunks[-1].id}" if all_chunks else "  Chunks: (none)")

    return all_chunks


def save_chunk(chunk: Chunk, domain_path: str):
    """Save chunk as .md file with frontmatter and .emb embedding file."""
    # Build frontmatter
    frontmatter = f"""---
id: {chunk.id}
source_doc: {chunk.source_doc}
source_section: "{chunk.source_section}"
source_lines: [{chunk.source_lines[0]}, {chunk.source_lines[1]}]
source_path: "{chunk.source_path}"
source_hash: "{chunk.source_hash}"
tokens: {chunk.tokens}
keywords: {json.dumps(chunk.keywords)}
created: "{chunk.created}"
last_retrieved: null
retrieval_count: 0
---

{chunk.content}
"""

    # Save markdown file
    md_path = os.path.join(domain_path, f"{chunk.id}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    # Generate and save embedding
    embedding = embed_passage(chunk.content)
    emb_path = os.path.join(domain_path, f"{chunk.id}.npy")
    np.save(emb_path, embedding)


def chunk_directory(
    path: str,
    project_root: str = ".",
    domain: Optional[str] = None,
    force: bool = False
) -> list[Chunk]:
    """
    Chunk all markdown files in a directory.

    Args:
        path: Path to directory
        project_root: Project root directory
        domain: Optional domain override for all files
        force: Re-chunk even if chunks exist

    Returns:
        List of all Chunk objects
    """
    path = os.path.abspath(path)
    all_chunks = []

    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith('.md'):
                file_path = os.path.join(root, f)
                try:
                    chunks = chunk_document(file_path, project_root, domain, force)
                    all_chunks.extend(chunks)
                except Exception as e:
                    print(f"Error chunking {file_path}: {e}")

    return all_chunks


def compute_file_hash(path: str) -> str:
    """Compute SHA256 hash of a file's content."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def parse_chunk_metadata(chunk_path: str) -> dict:
    """Parse metadata from a chunk's markdown frontmatter."""
    with open(chunk_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return {}

    end_idx = content.find('---', 3)
    if end_idx == -1:
        return {}

    frontmatter = content[3:end_idx].strip()
    meta = {}

    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Parse quoted strings
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]

            meta[key] = value

    return meta


def get_stale_chunks(project_root: str = ".") -> list[dict]:
    """
    Find chunks whose source files have changed.

    Returns list of {chunk_id, source_path, stored_hash, current_hash}
    """
    project_root = os.path.abspath(project_root)
    chunks_path = Config.get_chunks_path(project_root)

    if not os.path.exists(chunks_path):
        return []

    stale = []
    checked_sources = {}  # Cache: source_path -> current_hash

    for domain in os.listdir(chunks_path):
        domain_path = os.path.join(chunks_path, domain)
        if not os.path.isdir(domain_path):
            continue

        for f in os.listdir(domain_path):
            if not f.endswith('.md'):
                continue

            chunk_path = os.path.join(domain_path, f)
            meta = parse_chunk_metadata(chunk_path)

            source_path = meta.get('source_path', '')
            stored_hash = meta.get('source_hash', '')

            if not source_path or not stored_hash:
                continue  # Old chunk without provenance data

            # Resolve source path relative to project root
            full_source_path = os.path.join(project_root, source_path)

            if not os.path.exists(full_source_path):
                # Source file deleted - mark as stale
                stale.append({
                    'chunk_id': meta.get('id', f.replace('.md', '')),
                    'source_path': source_path,
                    'stored_hash': stored_hash,
                    'current_hash': None,
                    'status': 'deleted'
                })
                continue

            # Get or compute current hash
            if source_path not in checked_sources:
                checked_sources[source_path] = compute_file_hash(full_source_path)

            current_hash = checked_sources[source_path]

            if current_hash != stored_hash:
                stale.append({
                    'chunk_id': meta.get('id', f.replace('.md', '')),
                    'source_path': source_path,
                    'stored_hash': stored_hash,
                    'current_hash': current_hash,
                    'status': 'modified'
                })

    return stale


def get_chunks_by_source(source_path: str, project_root: str = ".") -> list[str]:
    """Find all chunk IDs that came from a given source file."""
    project_root = os.path.abspath(project_root)
    chunks_path = Config.get_chunks_path(project_root)

    # Normalize source path for comparison
    try:
        normalized_source = os.path.relpath(os.path.abspath(source_path), project_root)
    except ValueError:
        normalized_source = source_path

    if not os.path.exists(chunks_path):
        return []

    chunk_ids = []

    for domain in os.listdir(chunks_path):
        domain_path = os.path.join(chunks_path, domain)
        if not os.path.isdir(domain_path):
            continue

        for f in os.listdir(domain_path):
            if not f.endswith('.md'):
                continue

            chunk_path = os.path.join(domain_path, f)
            meta = parse_chunk_metadata(chunk_path)

            chunk_source = meta.get('source_path', '')

            # Compare normalized paths
            if chunk_source == normalized_source:
                chunk_ids.append(meta.get('id', f.replace('.md', '')))

    return chunk_ids


def delete_chunks(chunk_ids: list[str], project_root: str = ".") -> int:
    """Delete chunks by their IDs. Returns count of deleted chunks."""
    project_root = os.path.abspath(project_root)
    chunks_path = Config.get_chunks_path(project_root)

    deleted = 0

    for chunk_id in chunk_ids:
        # Parse domain from chunk ID (CHK-DOMAIN-DOC-SEQ)
        parts = chunk_id.split('-')
        if len(parts) < 2:
            continue

        domain = parts[1]
        domain_path = os.path.join(chunks_path, domain)

        md_path = os.path.join(domain_path, f"{chunk_id}.md")
        npy_path = os.path.join(domain_path, f"{chunk_id}.npy")

        if os.path.exists(md_path):
            os.remove(md_path)
            deleted += 1

        if os.path.exists(npy_path):
            os.remove(npy_path)

    return deleted


# CLI entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m core.chunker <path> [domain]")
        sys.exit(1)

    target_path = sys.argv[1]
    target_domain = sys.argv[2] if len(sys.argv) > 2 else None

    if os.path.isdir(target_path):
        chunk_directory(target_path, domain=target_domain)
    else:
        chunk_document(target_path, domain=target_domain)
