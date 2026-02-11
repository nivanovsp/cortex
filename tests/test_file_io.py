"""Phase 3: File I/O round-trip tests using tmp_path."""

import os
import json
import pytest
import numpy as np
from unittest.mock import patch


class TestChunkRoundTrip:
    def test_save_and_load_chunk(self, project_root, sample_embedding):
        """chunk_document + save_chunk round-trip via file system."""
        from core.chunker import Chunk, save_chunk
        from core.utils import parse_frontmatter

        domain_path = os.path.join(project_root, '.cortex', 'chunks', 'TEST')
        os.makedirs(domain_path, exist_ok=True)

        chunk = Chunk(
            id='CHK-TEST-001-001',
            source_doc='DOC-TEST-001',
            source_section='Test Section',
            source_lines=(1, 10),
            tokens=50,
            keywords=['test', 'chunk'],
            content='This is test chunk content for round-trip verification.',
            created='2026-01-15T10:00:00',
            source_path='test.md',
            source_hash='abc123'
        )

        # Mock embed_passage to avoid loading the ML model
        with patch('core.chunker.embed_passage', return_value=sample_embedding):
            save_chunk(chunk, domain_path)

        # Verify .md file exists and has correct frontmatter
        md_path = os.path.join(domain_path, 'CHK-TEST-001-001.md')
        assert os.path.exists(md_path)

        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        meta = parse_frontmatter(content)
        assert meta['id'] == 'CHK-TEST-001-001'
        assert meta['source_doc'] == 'DOC-TEST-001'
        assert meta['tokens'] == 50
        assert meta['keywords'] == ['test', 'chunk']

        # Verify content after frontmatter
        assert 'round-trip verification' in content

        # Verify .npy file exists and has correct shape
        npy_path = os.path.join(domain_path, 'CHK-TEST-001-001.npy')
        assert os.path.exists(npy_path)
        loaded_emb = np.load(npy_path)
        assert loaded_emb.shape == (384,)
        np.testing.assert_array_almost_equal(loaded_emb, sample_embedding)


class TestMemoryRoundTrip:
    def test_create_and_get_memory(self, project_root, sample_embedding):
        """create_memory + get_memory round-trip."""
        from core.memory import create_memory, get_memory

        with patch('core.memory.embed_passage', return_value=sample_embedding):
            memory = create_memory(
                learning='Always validate input before database queries',
                context='Found during security review of the API layer',
                memory_type='procedural',
                domain='API',
                confidence='high',
                project_root=project_root
            )

        assert memory.id.startswith('MEM-')
        assert memory.learning == 'Always validate input before database queries'
        assert memory.domain == 'API'
        assert memory.confidence == 'high'

        # Retrieve it back
        retrieved = get_memory(memory.id, project_root)
        assert retrieved is not None
        assert retrieved.id == memory.id
        assert retrieved.learning == memory.learning
        assert retrieved.domain == 'API'
        assert retrieved.type == 'procedural'


class TestIndexRoundTrip:
    def test_build_and_load_index(self, project_root, sample_embedding):
        """build_index + load_index round-trip with .npy + .ids.json format."""
        from core.indexer import build_index, load_index
        from core.chunker import Chunk, save_chunk

        # Create some chunks first
        domain_path = os.path.join(project_root, '.cortex', 'chunks', 'TEST')
        os.makedirs(domain_path, exist_ok=True)

        rng = np.random.default_rng(42)
        chunk_ids = []
        for i in range(3):
            chunk_id = f'CHK-TEST-001-{i+1:03d}'
            chunk_ids.append(chunk_id)

            chunk = Chunk(
                id=chunk_id,
                source_doc='DOC-TEST-001',
                source_section=f'Section {i+1}',
                source_lines=(i * 10 + 1, (i + 1) * 10),
                tokens=50 + i * 10,
                keywords=['test', f'section{i+1}'],
                content=f'Content for test section {i+1}.',
                created='2026-01-15T10:00:00',
                source_path='test.md',
                source_hash='abc123'
            )

            # Create a unique embedding for each chunk
            vec = rng.standard_normal(384).astype(np.float32)
            vec = vec / np.linalg.norm(vec)

            with patch('core.chunker.embed_passage', return_value=vec):
                save_chunk(chunk, domain_path)

        # Build the index
        count, index_path = build_index(project_root, 'chunks')
        assert count == 3
        assert index_path.endswith('.npy')

        # Verify index files exist
        index_dir = os.path.join(project_root, '.cortex', 'index')
        assert os.path.exists(os.path.join(index_dir, 'chunks.npy'))
        assert os.path.exists(os.path.join(index_dir, 'chunks.ids.json'))
        assert os.path.exists(os.path.join(index_dir, 'chunks.meta.json'))

        # Load the index back
        embeddings, ids, metadata = load_index(project_root, 'chunks')
        assert embeddings.shape == (3, 384)
        assert len(ids) == 3
        assert all(cid in ids for cid in chunk_ids)
        assert all(cid in metadata for cid in chunk_ids)

    def test_load_nonexistent_index_raises(self, project_root):
        """load_index raises FileNotFoundError for missing index."""
        from core.indexer import load_index
        with pytest.raises(FileNotFoundError):
            load_index(project_root, 'chunks')


class TestMemoryIndexRoundTrip:
    def test_build_memory_index(self, project_root, sample_embedding):
        """build_index for memories uses the same .npy + .ids.json format."""
        from core.indexer import build_index, load_index
        from core.memory import create_memory

        rng = np.random.default_rng(99)

        for i in range(2):
            vec = rng.standard_normal(384).astype(np.float32)
            vec = vec / np.linalg.norm(vec)
            with patch('core.memory.embed_passage', return_value=vec):
                create_memory(
                    learning=f'Learning number {i+1}',
                    context=f'Context for learning {i+1}',
                    project_root=project_root
                )

        count, index_path = build_index(project_root, 'memories')
        assert count == 2

        embeddings, ids, metadata = load_index(project_root, 'memories')
        assert embeddings.shape == (2, 384)
        assert len(ids) == 2
