"""
Cortex Memory Extractor

Analyzes text for potential learnings and proposes memories.
Used for session-end memory extraction.
"""

import re
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ProposedMemory:
    """A proposed memory extracted from text."""
    learning: str
    context: str
    memory_type: str  # factual, experiential, procedural
    confidence: str   # high, medium, low
    domain: str
    trigger: str      # What pattern triggered this extraction
    source_text: str  # Original text that led to this


# Extraction patterns with their confidence and type mappings
EXTRACTION_PATTERNS = [
    # High confidence - verified fixes
    {
        'pattern': r'(?:fixed|solved|resolved)\s+(?:by|with|using)\s+(.+?)(?:\.|$)',
        'type': 'experiential',
        'confidence': 'high',
        'trigger': 'verified_fix'
    },
    {
        'pattern': r'the\s+(?:issue|problem|bug)\s+was\s+(.+?)(?:\.|$)',
        'type': 'experiential',
        'confidence': 'high',
        'trigger': 'issue_resolution'
    },
    {
        'pattern': r'(?:remember|note|important):\s*(.+?)(?:\.|$)',
        'type': 'experiential',
        'confidence': 'high',
        'trigger': 'explicit_remember'
    },

    # Medium confidence - discoveries
    {
        'pattern': r'(?:found|discovered|learned)\s+that\s+(.+?)(?:\.|$)',
        'type': 'experiential',
        'confidence': 'medium',
        'trigger': 'discovery'
    },
    {
        'pattern': r'(?:turns out|it appears|apparently)\s+(.+?)(?:\.|$)',
        'type': 'experiential',
        'confidence': 'medium',
        'trigger': 'realization'
    },
    {
        'pattern': r'(?:this|that)\s+(?:requires?|needs?)\s+(.+?)(?:\.|$)',
        'type': 'factual',
        'confidence': 'medium',
        'trigger': 'requirement'
    },

    # Procedural patterns
    {
        'pattern': r'(?:always|never|must|should)\s+(.+?)(?:\.|$)',
        'type': 'procedural',
        'confidence': 'medium',
        'trigger': 'rule'
    },
    {
        'pattern': r'(?:to|in order to)\s+(.+?),?\s+(?:you need to|we need to|must)\s+(.+?)(?:\.|$)',
        'type': 'procedural',
        'confidence': 'medium',
        'trigger': 'procedure'
    },
    {
        'pattern': r'(?:before|after)\s+(.+?),?\s+(?:make sure|ensure|verify)\s+(.+?)(?:\.|$)',
        'type': 'procedural',
        'confidence': 'medium',
        'trigger': 'sequence'
    },

    # Factual patterns
    {
        'pattern': r'(.+?)\s+(?:uses?|expects?|requires?)\s+(.+?)(?:\.|$)',
        'type': 'factual',
        'confidence': 'low',
        'trigger': 'fact'
    },
    {
        'pattern': r'(.+?)\s+is\s+(?:located|stored|found)\s+(?:in|at)\s+(.+?)(?:\.|$)',
        'type': 'factual',
        'confidence': 'low',
        'trigger': 'location'
    },
]

# Domain detection patterns
DOMAIN_PATTERNS = {
    'AUTH': r'\b(?:auth|login|logout|session|token|password|credential|oauth|jwt)\b',
    'UI': r'\b(?:component|button|form|input|modal|dialog|ui|ux|style|css|layout)\b',
    'API': r'\b(?:api|endpoint|request|response|rest|graphql|fetch|axios)\b',
    'DB': r'\b(?:database|query|sql|mongodb|postgres|mysql|schema|migration)\b',
    'TEST': r'\b(?:test|spec|jest|pytest|unittest|mock|fixture|assert)\b',
    'DEV': r'\b(?:build|deploy|ci|cd|docker|kubernetes|git|npm|pip)\b',
}


def detect_domain(text: str) -> str:
    """Detect the most likely domain from text."""
    text_lower = text.lower()
    scores = {}

    for domain, pattern in DOMAIN_PATTERNS.items():
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        scores[domain] = len(matches)

    if not scores or max(scores.values()) == 0:
        return 'GENERAL'

    return max(scores, key=scores.get)


def clean_extracted_text(text: str) -> str:
    """Clean up extracted text."""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove leading/trailing punctuation
    text = text.strip('.,;:!? ')
    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]
    return text


def extract_memories(
    text: str,
    min_confidence: str = "low",
    source_session: Optional[str] = None
) -> list[ProposedMemory]:
    """
    Extract potential memories from text.

    Args:
        text: Text to analyze (e.g., session transcript)
        min_confidence: Minimum confidence to include (low, medium, high)
        source_session: Optional session identifier

    Returns:
        List of ProposedMemory objects
    """
    confidence_order = ['low', 'medium', 'high']
    min_conf_idx = confidence_order.index(min_confidence)

    proposed = []
    seen_learnings = set()  # Avoid duplicates

    # Split text into sentences for context
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for pattern_def in EXTRACTION_PATTERNS:
        pattern = pattern_def['pattern']
        mem_type = pattern_def['type']
        confidence = pattern_def['confidence']
        trigger = pattern_def['trigger']

        # Check confidence threshold
        if confidence_order.index(confidence) < min_conf_idx:
            continue

        # Find matches
        for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
            # Extract the learning
            groups = match.groups()
            if len(groups) == 1:
                learning = clean_extracted_text(groups[0])
            elif len(groups) == 2:
                learning = clean_extracted_text(f"{groups[0]} - {groups[1]}")
            else:
                learning = clean_extracted_text(match.group(0))

            # Skip if too short or already seen
            if len(learning) < 10 or learning.lower() in seen_learnings:
                continue

            seen_learnings.add(learning.lower())

            # Find context (surrounding sentences)
            match_pos = match.start()
            context_sentences = []
            char_count = 0
            for sent in sentences:
                sent_start = text.find(sent, char_count)
                sent_end = sent_start + len(sent)
                if sent_start <= match_pos <= sent_end:
                    # Include previous sentence if available
                    idx = sentences.index(sent)
                    if idx > 0:
                        context_sentences.append(sentences[idx - 1])
                    context_sentences.append(sent)
                    # Include next sentence if available
                    if idx < len(sentences) - 1:
                        context_sentences.append(sentences[idx + 1])
                    break
                char_count = sent_end

            context = ' '.join(context_sentences) if context_sentences else ""

            # Detect domain
            domain = detect_domain(learning + " " + context)

            proposed.append(ProposedMemory(
                learning=learning,
                context=context[:500],  # Limit context length
                memory_type=mem_type,
                confidence=confidence,
                domain=domain,
                trigger=trigger,
                source_text=match.group(0)[:200]
            ))

    # Sort by confidence (high first)
    proposed.sort(key=lambda x: confidence_order.index(x.confidence), reverse=True)

    return proposed


def extract_and_format(
    text: str,
    min_confidence: str = "low"
) -> str:
    """
    Extract memories and format for display.

    Args:
        text: Text to analyze
        min_confidence: Minimum confidence threshold

    Returns:
        Formatted string showing proposed memories
    """
    proposed = extract_memories(text, min_confidence)

    if not proposed:
        return "No potential memories detected."

    lines = [f"Found {len(proposed)} potential memories:\n"]

    for i, mem in enumerate(proposed, 1):
        conf_icon = {'high': '[H]', 'medium': '[M]', 'low': '[L]'}[mem.confidence]
        type_icon = {'factual': 'F', 'experiential': 'E', 'procedural': 'P'}[mem.memory_type]

        lines.append(f"{i}. {conf_icon} [{type_icon}] {mem.domain}")
        lines.append(f"   Learning: {mem.learning}")
        if mem.context:
            context_preview = mem.context[:100] + "..." if len(mem.context) > 100 else mem.context
            lines.append(f"   Context: {context_preview}")
        lines.append(f"   Trigger: {mem.trigger}")
        lines.append("")

    return "\n".join(lines)


def save_proposed_memories(
    proposed: list[ProposedMemory],
    indices: list[int],
    project_root: str = ".",
    source_session: Optional[str] = None
) -> list[str]:
    """
    Save selected proposed memories.

    Args:
        proposed: List of proposed memories
        indices: Indices of memories to save (1-based)
        project_root: Project root directory
        source_session: Session identifier

    Returns:
        List of created memory IDs
    """
    from .memory import create_memory

    created_ids = []

    for idx in indices:
        if 1 <= idx <= len(proposed):
            mem = proposed[idx - 1]
            result = create_memory(
                learning=mem.learning,
                context=mem.context,
                memory_type=mem.memory_type,
                domain=mem.domain,
                confidence=mem.confidence,
                source_session=source_session,
                trigger=mem.trigger,
                project_root=project_root
            )
            created_ids.append(result.id)

    return created_ids


# CLI entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m core.extractor <text_or_file>")
        sys.exit(1)

    arg = sys.argv[1]

    # Check if it's a file
    import os
    if os.path.isfile(arg):
        with open(arg, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = arg

    print(extract_and_format(text))
