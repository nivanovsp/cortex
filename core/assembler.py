"""
Cortex Context Assembler

Builds position-optimized context frames from retrieved chunks and memories.
Implements "lost in middle" awareness by placing critical info at edges.
"""

import os
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
import tiktoken

from .config import Config
from .retriever import retrieve
from .memory import increment_retrieval
from .utils import load_chunk_content


@dataclass
class ContextBudget:
    """Token budget allocation for context frame sections."""
    task_definition: int = 2000
    chunks: int = 10000
    memories: int = 2000
    current_state: int = 1000
    instructions: int = 500

    @property
    def total(self) -> int:
        return (
            self.task_definition +
            self.chunks +
            self.memories +
            self.current_state +
            self.instructions
        )

    @classmethod
    def from_total(cls, total: int) -> 'ContextBudget':
        """Create budget proportionally from total."""
        # Default proportions: task 13%, chunks 65%, memories 13%, state 6%, instructions 3%
        return cls(
            task_definition=int(total * 0.13),
            chunks=int(total * 0.65),
            memories=int(total * 0.13),
            current_state=int(total * 0.06),
            instructions=int(total * 0.03)
        )


@dataclass
class ContextFrame:
    """Assembled context frame."""
    task: str
    acceptance_criteria: list[str]
    chunks: list[dict]
    memories: list[dict]
    current_state: Optional[str]
    instructions: Optional[str]
    generated_at: str
    budget_total: int
    budget_used: int

    def to_markdown(self) -> str:
        """Render context frame as markdown."""
        lines = []

        # Header with metadata
        lines.append(f"<!-- CONTEXT FRAME: {self.task[:50]} -->")
        lines.append(f"<!-- Generated: {self.generated_at} -->")
        lines.append(f"<!-- Budget: {self.budget_total:,} / Used: {self.budget_used:,} -->")
        lines.append("")

        # Section 1: Task Definition (CRITICAL - primacy zone)
        lines.append("## CRITICAL: Task Definition")
        lines.append("")
        lines.append(f"**Task:** {self.task}")
        lines.append("")
        if self.acceptance_criteria:
            lines.append("**Acceptance Criteria:**")
            for criterion in self.acceptance_criteria:
                lines.append(f"- {criterion}")
            lines.append("")
        lines.append("---")
        lines.append("")

        # Section 2: Relevant Knowledge (upper-middle)
        if self.chunks:
            lines.append("## Relevant Knowledge")
            lines.append("")
            for chunk in self.chunks:
                section = chunk.get('metadata', {}).get('source_section', 'Unknown')
                source = chunk.get('metadata', {}).get('source_doc', '')
                score = chunk.get('score', 0)
                lines.append(f"### {section} ({source})")
                lines.append(f"<!-- Relevance: {score:.2f} -->")
                lines.append("")
                if 'content' in chunk:
                    lines.append(chunk['content'])
                    lines.append("")
            lines.append("---")
            lines.append("")

        # Section 3: Past Learnings (lower-middle)
        if self.memories:
            lines.append("## Past Learnings")
            lines.append("")
            for mem in self.memories:
                meta = mem.get('metadata', {})
                mem_id = mem.get('id', 'unknown')
                confidence = meta.get('confidence', 'unknown')
                domain = meta.get('domain', '')
                # Get learning content if available
                learning = meta.get('learning', '')
                if not learning and 'content' in mem:
                    learning = mem['content']
                lines.append(f"- **{mem_id}** ({confidence}, {domain}): {learning}")
            lines.append("")
            lines.append("---")
            lines.append("")

        # Section 4: Current State (bottom - recency zone)
        if self.current_state:
            lines.append("## Current State")
            lines.append("")
            lines.append(self.current_state)
            lines.append("")
            lines.append("---")
            lines.append("")

        # Section 5: Instructions (very end - max recency)
        lines.append("## Instructions")
        lines.append("")
        if self.instructions:
            lines.append(self.instructions)
        else:
            lines.append(f"Complete the task described above using the relevant knowledge and learnings provided.")
        lines.append("")

        return "\n".join(lines)


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken."""
    encoder = tiktoken.get_encoding("cl100k_base")
    return len(encoder.encode(text))


def truncate_to_budget(text: str, max_tokens: int) -> str:
    """Truncate text to fit within token budget."""
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    if len(tokens) <= max_tokens:
        return text
    # Truncate and add ellipsis
    truncated = encoder.decode(tokens[:max_tokens - 3])
    return truncated + "..."


def load_memory_content(memory_id: str, project_root: str) -> Optional[str]:
    """Load learning content for a memory."""
    from .memory import get_memory
    memory = get_memory(memory_id, project_root)
    if memory:
        return memory.learning
    return None


def assemble_context(
    task: str,
    project_root: str = ".",
    acceptance_criteria: Optional[list[str]] = None,
    current_state: Optional[str] = None,
    instructions: Optional[str] = None,
    budget: Optional[int] = None,
    chunk_top_k: int = 10,
    memory_top_k: int = 5
) -> ContextFrame:
    """
    Assemble a context frame for a task.

    Args:
        task: Task description
        project_root: Project root directory
        acceptance_criteria: List of acceptance criteria
        current_state: Current state description
        instructions: Custom instructions
        budget: Total token budget (default from config)
        chunk_top_k: Max chunks to retrieve
        memory_top_k: Max memories to retrieve

    Returns:
        ContextFrame object
    """
    project_root = os.path.abspath(project_root)

    # Set up budget
    total_budget = budget or Config.TOKEN_BUDGET
    budget_alloc = ContextBudget.from_total(total_budget)

    # Retrieve relevant chunks
    chunks = []
    try:
        chunk_results = retrieve(
            task,
            project_root,
            top_k=chunk_top_k,
            index_type="chunks",
            include_content=False
        )
        # Load content and track tokens
        chunks_tokens = 0
        for result in chunk_results:
            content = load_chunk_content(result['id'], project_root)
            if content:
                content_tokens = count_tokens(content)
                if chunks_tokens + content_tokens <= budget_alloc.chunks:
                    result['content'] = content
                    chunks.append(result)
                    chunks_tokens += content_tokens
                else:
                    # Truncate last chunk to fit
                    remaining = budget_alloc.chunks - chunks_tokens
                    if remaining > 100:  # Only if there's meaningful space
                        result['content'] = truncate_to_budget(content, remaining)
                        chunks.append(result)
                    break
    except FileNotFoundError:
        pass  # No chunks index

    # Retrieve relevant memories
    memories = []
    try:
        memory_results = retrieve(
            task,
            project_root,
            top_k=memory_top_k,
            index_type="memories",
            include_content=False
        )
        # Load content and track tokens
        memories_tokens = 0
        for result in memory_results:
            content = load_memory_content(result['id'], project_root)
            if content:
                content_tokens = count_tokens(content)
                if memories_tokens + content_tokens <= budget_alloc.memories:
                    result['content'] = content
                    # Also store in metadata for rendering
                    if 'metadata' not in result:
                        result['metadata'] = {}
                    result['metadata']['learning'] = content
                    memories.append(result)
                    increment_retrieval(result['id'], project_root)
                    memories_tokens += content_tokens
    except FileNotFoundError:
        pass  # No memories index

    # Build task definition section
    task_section = f"**Task:** {task}\n"
    if acceptance_criteria:
        task_section += "\n**Acceptance Criteria:**\n"
        for criterion in acceptance_criteria:
            task_section += f"- {criterion}\n"

    # Truncate sections to budget
    task_section = truncate_to_budget(task_section, budget_alloc.task_definition)
    if current_state:
        current_state = truncate_to_budget(current_state, budget_alloc.current_state)
    if instructions:
        instructions = truncate_to_budget(instructions, budget_alloc.instructions)

    # Create context frame
    frame = ContextFrame(
        task=task,
        acceptance_criteria=acceptance_criteria or [],
        chunks=chunks,
        memories=memories,
        current_state=current_state,
        instructions=instructions,
        generated_at=datetime.now().isoformat(),
        budget_total=total_budget,
        budget_used=0  # Calculate below
    )

    # Calculate actual usage
    markdown = frame.to_markdown()
    frame.budget_used = count_tokens(markdown)

    return frame


def assemble_and_render(
    task: str,
    project_root: str = ".",
    acceptance_criteria: Optional[list[str]] = None,
    current_state: Optional[str] = None,
    instructions: Optional[str] = None,
    budget: Optional[int] = None,
    output_path: Optional[str] = None
) -> str:
    """
    Assemble context frame and render to markdown.

    Args:
        task: Task description
        project_root: Project root directory
        acceptance_criteria: List of acceptance criteria
        current_state: Current state description
        instructions: Custom instructions
        budget: Total token budget
        output_path: Optional file path to write output

    Returns:
        Rendered markdown string
    """
    frame = assemble_context(
        task=task,
        project_root=project_root,
        acceptance_criteria=acceptance_criteria,
        current_state=current_state,
        instructions=instructions,
        budget=budget
    )

    markdown = frame.to_markdown()

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"Context frame written to: {output_path}")

    return markdown


# CLI entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m core.assembler <task> [--budget N] [--output FILE]")
        sys.exit(1)

    task = sys.argv[1]
    budget = None
    output = None

    # Parse args
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--budget" and i + 1 < len(sys.argv):
            budget = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    markdown = assemble_and_render(task, ".", budget=budget, output_path=output)
    if not output:
        print(markdown)
