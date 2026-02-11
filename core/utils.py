"""
Cortex Utilities

Shared helpers used across core modules.
"""

import os
import re
import json
from typing import Optional


def parse_frontmatter(content: str) -> dict:
    """
    Parse YAML frontmatter from markdown content.

    Handles value types: quoted strings, JSON arrays, null, booleans,
    integers, and floats (including negatives).
    """
    if not content.startswith('---'):
        return {}

    end_idx = content.find('---', 3)
    if end_idx == -1:
        return {}

    frontmatter = content[3:end_idx].strip()
    result = {}

    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Parse value types
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith('[') and value.endswith(']'):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    pass
            elif value == 'null':
                value = None
            elif value == 'true':
                value = True
            elif value == 'false':
                value = False
            elif value.replace('.', '').replace('-', '').isdigit():
                try:
                    value = float(value) if '.' in value else int(value)
                except ValueError:
                    pass

            result[key] = value

    return result


def parse_chunk_id(chunk_id: str) -> Optional[tuple[str, str, str, str]]:
    """
    Parse a chunk ID into its components.

    Format: CHK-DOMAIN-DOC-SEQ (e.g., CHK-AUTH-001-003)

    Returns:
        Tuple of (prefix, domain, doc_num, seq_num) or None if invalid.
    """
    parts = chunk_id.split('-')
    if len(parts) < 4:
        return None
    return (parts[0], parts[1], parts[2], parts[3])


def load_chunk_content(chunk_id: str, project_root: str) -> Optional[str]:
    """
    Load the body content of a chunk file (after frontmatter).

    Args:
        chunk_id: Chunk ID (e.g., CHK-AUTH-001-003)
        project_root: Project root directory

    Returns:
        Content string or None if not found.
    """
    from .config import Config

    parsed = parse_chunk_id(chunk_id)
    if not parsed:
        return None

    domain = parsed[1]
    chunks_path = Config.get_chunks_path(project_root)
    md_path = os.path.join(chunks_path, domain, f"{chunk_id}.md")

    if not os.path.exists(md_path):
        return None

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract content after frontmatter
    if '---' in content:
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[2].strip()

    return content


# Unified stopword set (union of chunker and memory stopwords)
STOPWORDS = {
    'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
    'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been', 'were',
    'being', 'their', 'there', 'this', 'that', 'with', 'they', 'from',
    'will', 'would', 'could', 'should', 'which', 'when', 'where', 'what',
    'each', 'into', 'than', 'then', 'also', 'only', 'other', 'such',
    'more', 'some', 'very', 'just', 'about', 'over', 'after', 'before'
}


def extract_keywords(text: str, max_keywords: int = 10) -> list[str]:
    """
    Extract keywords from text using TF-based approach.

    Cleans markdown syntax, removes stopwords, and returns top keywords
    by frequency.
    """
    text_lower = text.lower()
    # Remove code blocks, inline code, markdown links, and syntax
    text_clean = re.sub(r'```[\s\S]*?```', '', text_lower)
    text_clean = re.sub(r'`[^`]+`', '', text_clean)
    text_clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text_clean)
    text_clean = re.sub(r'[#*_~`>\-|]', ' ', text_clean)

    # Tokenize
    words = re.findall(r'\b[a-z]{3,}\b', text_clean)

    # Filter stopwords
    words = [w for w in words if w not in STOPWORDS]

    # Count frequency
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    # Sort by frequency and return top keywords
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:max_keywords]]
