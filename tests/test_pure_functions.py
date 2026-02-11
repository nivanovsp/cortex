"""Phase 1: Pure function unit tests (no mocking required)."""

import pytest
import numpy as np
from datetime import datetime, timedelta


# ── core/utils.py ──

class TestParseFrontmatter:
    def test_basic_key_value(self):
        from core.utils import parse_frontmatter
        content = '---\nid: CHK-AUTH-001-001\ntokens: 120\n---\nBody'
        result = parse_frontmatter(content)
        assert result['id'] == 'CHK-AUTH-001-001'
        assert result['tokens'] == 120

    def test_quoted_strings(self):
        from core.utils import parse_frontmatter
        content = '---\nsource_section: "My Section"\n---\n'
        result = parse_frontmatter(content)
        assert result['source_section'] == 'My Section'

    def test_json_array(self):
        from core.utils import parse_frontmatter
        content = '---\nkeywords: ["auth", "login"]\n---\n'
        result = parse_frontmatter(content)
        assert result['keywords'] == ['auth', 'login']

    def test_null_and_booleans(self):
        from core.utils import parse_frontmatter
        content = '---\nlast_retrieved: null\nverified: true\nactive: false\n---\n'
        result = parse_frontmatter(content)
        assert result['last_retrieved'] is None
        assert result['verified'] is True
        assert result['active'] is False

    def test_no_frontmatter_returns_empty(self):
        from core.utils import parse_frontmatter
        assert parse_frontmatter('No frontmatter here') == {}

    def test_unclosed_frontmatter_returns_empty(self):
        from core.utils import parse_frontmatter
        assert parse_frontmatter('---\nid: test\nNo closing') == {}


class TestParseChunkId:
    def test_valid_chunk_id(self):
        from core.utils import parse_chunk_id
        result = parse_chunk_id('CHK-AUTH-001-003')
        assert result == ('CHK', 'AUTH', '001', '003')

    def test_invalid_chunk_id_too_few_parts(self):
        from core.utils import parse_chunk_id
        assert parse_chunk_id('CHK-AUTH') is None

    def test_minimal_four_parts(self):
        from core.utils import parse_chunk_id
        result = parse_chunk_id('A-B-C-D')
        assert result == ('A', 'B', 'C', 'D')


class TestExtractKeywords:
    def test_extracts_frequent_words(self):
        from core.utils import extract_keywords
        text = 'authentication authentication login login login session'
        result = extract_keywords(text)
        assert result[0] == 'login'  # most frequent
        assert 'authentication' in result

    def test_filters_stopwords(self):
        from core.utils import extract_keywords, STOPWORDS
        text = 'the and for are but not authentication'
        result = extract_keywords(text)
        assert 'authentication' in result
        for word in result:
            assert word not in STOPWORDS

    def test_max_keywords_limit(self):
        from core.utils import extract_keywords
        text = ' '.join(f'word{i}' * (10 - i) for i in range(20))
        result = extract_keywords(text, max_keywords=5)
        assert len(result) <= 5

    def test_strips_markdown_syntax(self):
        from core.utils import extract_keywords
        text = '# Header\n**bold** and `inline code` plus [link](http://url)'
        result = extract_keywords(text)
        # 'bold', 'inline', 'code', 'link' should survive; markdown syntax should not
        assert all(c not in '#*`[]()' for word in result for c in word)


# ── core/chunker.py ──

class TestCountTokens:
    def test_empty_string(self):
        from core.chunker import count_tokens
        assert count_tokens('') == 0

    def test_nonempty_string(self):
        from core.chunker import count_tokens
        result = count_tokens('Hello world, this is a test.')
        assert isinstance(result, int)
        assert result > 0


class TestSplitByParagraphs:
    def test_single_paragraph_under_limit(self):
        from core.chunker import split_by_paragraphs
        text = 'A short paragraph that fits easily.'
        result = split_by_paragraphs(text, max_tokens=500)
        assert len(result) == 1
        assert result[0] == text

    def test_multiple_paragraphs_split(self):
        from core.chunker import split_by_paragraphs
        # Create text that will exceed the token limit when combined
        para = 'Word ' * 100  # ~100 tokens
        text = f'{para}\n\n{para}\n\n{para}'
        result = split_by_paragraphs(text, max_tokens=150)
        assert len(result) > 1


class TestAddOverlap:
    def test_single_chunk_unchanged(self):
        from core.chunker import add_overlap
        chunks = ['Only one chunk here.']
        result = add_overlap(chunks, 50)
        assert result == chunks

    def test_zero_overlap_unchanged(self):
        from core.chunker import add_overlap
        chunks = ['First chunk.', 'Second chunk.']
        result = add_overlap(chunks, 0)
        assert result == chunks

    def test_overlap_adds_prefix(self):
        from core.chunker import add_overlap
        # First chunk needs enough words so len(prev_words) > overlap_words
        # overlap_words = int(overlap_tokens / 1.3), so for 10 tokens -> ~7 words
        first = ' '.join(f'word{i}' for i in range(20))
        chunks = [first, 'Second chunk content.']
        result = add_overlap(chunks, 10)
        assert len(result) == 2
        assert result[0] == chunks[0]  # first chunk unchanged
        assert result[1].startswith('...')  # second chunk has overlap prefix


class TestParseSections:
    def test_single_header(self):
        from core.chunker import parse_sections
        content = '# Title\n\nSome content here.'
        result = parse_sections(content)
        assert len(result) == 1
        assert result[0]['title'] == 'Title'
        assert 'Some content here.' in result[0]['content']

    def test_multiple_headers(self):
        from core.chunker import parse_sections
        content = '# First\n\nContent 1\n\n# Second\n\nContent 2'
        result = parse_sections(content)
        assert len(result) == 2
        assert result[0]['title'] == 'First'
        assert result[1]['title'] == 'Second'

    def test_content_before_first_header(self):
        from core.chunker import parse_sections
        content = 'Preamble text\n\n# Header\n\nBody'
        result = parse_sections(content)
        assert result[0]['title'] == 'Introduction'


class TestDetectDomain:
    def test_parent_folder_detection(self):
        from core.chunker import detect_domain
        assert detect_domain('project/auth/spec.md') == 'AUTH'

    def test_filename_prefix_detection(self):
        from core.chunker import detect_domain
        assert detect_domain('docs/auth-spec.md') == 'AUTH'

    def test_generic_parent_falls_through(self):
        from core.chunker import detect_domain
        # 'docs' is in the generic list, so should use filename prefix
        assert detect_domain('docs/api-routes.md') == 'API'

    def test_fallback_to_general(self):
        from core.chunker import detect_domain
        assert detect_domain('docs/readme.md') == 'GENERAL'


# ── core/retriever.py ──

class TestComputeKeywordOverlap:
    def test_full_overlap(self):
        from core.retriever import compute_keyword_overlap
        assert compute_keyword_overlap(['auth', 'login'], ['auth', 'login']) == 1.0

    def test_no_overlap(self):
        from core.retriever import compute_keyword_overlap
        assert compute_keyword_overlap(['auth'], ['database']) == 0.0

    def test_partial_overlap(self):
        from core.retriever import compute_keyword_overlap
        result = compute_keyword_overlap(['auth', 'login'], ['auth', 'session'])
        assert 0.0 < result < 1.0

    def test_empty_lists_return_zero(self):
        from core.retriever import compute_keyword_overlap
        assert compute_keyword_overlap([], ['auth']) == 0.0
        assert compute_keyword_overlap(['auth'], []) == 0.0


class TestComputeRecencyScore:
    def test_recent_date_high_score(self):
        from core.retriever import compute_recency_score
        now = datetime.now().isoformat()
        score = compute_recency_score(now)
        assert score > 0.9

    def test_old_date_low_score(self):
        from core.retriever import compute_recency_score
        old = (datetime.now() - timedelta(days=365)).isoformat()
        score = compute_recency_score(old)
        assert score < 0.1

    def test_none_returns_default(self):
        from core.retriever import compute_recency_score
        assert compute_recency_score(None) == 0.5

    def test_thirty_days_returns_half(self):
        from core.retriever import compute_recency_score
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        score = compute_recency_score(thirty_days_ago)
        # score = 1/(1+30/30) = 0.5
        assert abs(score - 0.5) < 0.05


class TestComputeFrequencyScore:
    def test_zero_count(self):
        from core.retriever import compute_frequency_score
        score = compute_frequency_score(0)
        assert score == 0.0

    def test_positive_count(self):
        from core.retriever import compute_frequency_score
        score = compute_frequency_score(10)
        assert 0.0 < score < 1.0

    def test_monotonically_increasing(self):
        from core.retriever import compute_frequency_score
        scores = [compute_frequency_score(i) for i in range(0, 50, 10)]
        for i in range(len(scores) - 1):
            assert scores[i] < scores[i + 1]


# ── core/assembler.py ──

class TestContextBudget:
    def test_from_total_proportions(self):
        from core.assembler import ContextBudget
        budget = ContextBudget.from_total(10000)
        assert budget.chunks == 6500  # 65%
        assert budget.task_definition == 1300  # 13%
        assert budget.memories == 1300  # 13%

    def test_total_property(self):
        from core.assembler import ContextBudget
        budget = ContextBudget()
        expected = (budget.task_definition + budget.chunks + budget.memories +
                    budget.current_state + budget.instructions)
        assert budget.total == expected


class TestTruncateToBudget:
    def test_short_text_unchanged(self):
        from core.assembler import truncate_to_budget
        text = 'Short text.'
        assert truncate_to_budget(text, 1000) == text

    def test_long_text_truncated(self):
        from core.assembler import truncate_to_budget
        text = 'word ' * 500  # ~500 tokens
        result = truncate_to_budget(text, 10)
        assert result.endswith('...')
        assert len(result) < len(text)


# ── core/extractor.py ──

class TestExtractorDetectDomain:
    def test_auth_domain(self):
        from core.extractor import detect_domain
        assert detect_domain('Fixed the login authentication bug') == 'AUTH'

    def test_api_domain(self):
        from core.extractor import detect_domain
        assert detect_domain('The API endpoint returns 404') == 'API'

    def test_fallback_to_general(self):
        from core.extractor import detect_domain
        assert detect_domain('Some generic text here') == 'GENERAL'

    def test_scoring_picks_highest(self):
        from core.extractor import detect_domain
        # Multiple auth keywords should win over single API keyword
        result = detect_domain('login session token password for the api')
        assert result == 'AUTH'


class TestExtractMemories:
    def test_verified_fix_extraction(self):
        from core.extractor import extract_memories
        text = 'Fixed by adding a null check before the database query.'
        result = extract_memories(text)
        assert len(result) > 0
        assert any(m.trigger == 'verified_fix' for m in result)

    def test_discovery_extraction(self):
        from core.extractor import extract_memories
        text = 'Found that the cache expires after 60 seconds.'
        result = extract_memories(text)
        assert len(result) > 0
        assert any(m.trigger == 'discovery' for m in result)

    def test_min_confidence_filter(self):
        from core.extractor import extract_memories
        text = 'The API uses REST. Found that caching helps. Fixed by adding retry logic.'
        all_results = extract_memories(text, min_confidence='low')
        high_results = extract_memories(text, min_confidence='high')
        assert len(all_results) >= len(high_results)
