"""Phase 2: CLI-to-core interface contract tests."""

import inspect
import pytest
from pathlib import Path
from typing import Optional
from unittest.mock import patch, MagicMock


class TestBuildIndexInterface:
    def test_return_type_annotation(self):
        from core.indexer import build_index
        hints = inspect.get_annotations(build_index)
        assert hints.get('return') == tuple[int, str]

    def test_accepts_expected_parameters(self):
        from core.indexer import build_index
        sig = inspect.signature(build_index)
        params = list(sig.parameters.keys())
        assert 'project_root' in params
        assert 'index_type' in params
        assert 'full_rebuild' in params


class TestLoadIndexInterface:
    def test_return_type_annotation(self):
        import numpy as np
        from core.indexer import load_index
        hints = inspect.get_annotations(load_index)
        assert hints.get('return') == tuple[np.ndarray, list[str], dict]

    def test_accepts_expected_parameters(self):
        from core.indexer import load_index
        sig = inspect.signature(load_index)
        params = list(sig.parameters.keys())
        assert 'project_root' in params
        assert 'index_type' in params


class TestExtractAndFormatInterface:
    def test_return_type_is_dict(self):
        from core.extractor import extract_and_format
        result = extract_and_format('Fixed by adding a null check.')
        assert isinstance(result, dict)
        assert 'memories' in result
        assert 'project_root' in result

    def test_memories_list_structure(self):
        from core.extractor import extract_and_format
        result = extract_and_format('Fixed by adding a null check.')
        for mem in result['memories']:
            assert 'learning' in mem
            assert 'type' in mem
            assert 'confidence' in mem
            assert 'domain' in mem

    def test_accepts_expected_parameters(self):
        from core.extractor import extract_and_format
        sig = inspect.signature(extract_and_format)
        params = list(sig.parameters.keys())
        assert 'text' in params
        assert 'project_root' in params
        assert 'min_confidence' in params


class TestSaveProposedMemoriesInterface:
    def test_accepts_expected_parameters(self):
        from core.extractor import save_proposed_memories
        sig = inspect.signature(save_proposed_memories)
        params = list(sig.parameters.keys())
        assert 'memories' in params
        assert 'project_root' in params
        assert 'indices' in params
        assert 'source_session' in params

    def test_indices_parameter_is_optional(self):
        from core.extractor import save_proposed_memories
        sig = inspect.signature(save_proposed_memories)
        indices_param = sig.parameters['indices']
        assert indices_param.default is None


class TestRetrieveInterface:
    def test_accepts_expected_parameters(self):
        from core.retriever import retrieve
        sig = inspect.signature(retrieve)
        params = list(sig.parameters.keys())
        assert 'query' in params
        assert 'project_root' in params
        assert 'top_k' in params
        assert 'index_type' in params
        assert 'include_content' in params

    def test_index_type_default_is_both(self):
        from core.retriever import retrieve
        sig = inspect.signature(retrieve)
        assert sig.parameters['index_type'].default == 'both'


class TestCLIIndexUnpacksTuple:
    def test_cli_index_uses_tuple_unpack(self):
        """Verify CLI index command unpacks the tuple from build_index."""
        source = inspect.getsource(
            __import__('cli.commands.index', fromlist=['run']).run
        )
        # The CLI should unpack: count, path = build_index(...)
        assert 'count, path' in source or 'count,path' in source


class TestCLIRetrieveDefaultIndexType:
    def test_cli_retrieve_defaults_to_both(self):
        from cli.commands.retrieve import run
        sig = inspect.signature(run)
        assert sig.parameters['index_type'].default == 'both'


class TestCLIExtractCallsCore:
    def test_extract_command_uses_extract_and_format(self):
        """Verify CLI extract command imports and calls extract_and_format."""
        source = inspect.getsource(
            __import__('cli.commands.extract', fromlist=['run']).run
        )
        assert 'extract_and_format' in source

    def test_extract_command_uses_save_proposed_memories(self):
        """Verify CLI extract command imports save_proposed_memories."""
        source = inspect.getsource(
            __import__('cli.commands.extract', fromlist=['run']).run
        )
        assert 'save_proposed_memories' in source
