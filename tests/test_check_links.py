"""Tests for scripts/check_links.py, the citation validator."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "tabpfn-wiki"

spec = importlib.util.spec_from_file_location("check_links", ROOT / "scripts" / "check_links.py")
check_links = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_links)

SOURCE = """---
id: smith-2024-example
---

## Key claims

- **thm-1**: The estimator is unbiased. ^thm-1
- **sec-3**: Variance shrinks with n. ^sec-3
"""


def make_wiki(tmp_path: Path, concept: str) -> Path:
    for d in ("concepts", "sources", "indices"):
        (tmp_path / d).mkdir()
    (tmp_path / "sources" / "smith-2024-example.md").write_text(SOURCE, encoding="utf-8")
    (tmp_path / "concepts" / "estimator.md").write_text(concept, encoding="utf-8")
    aliases = {"estimator": "estimator", "variance": "variance"}
    (tmp_path / "indices" / "aliases.json").write_text(json.dumps(aliases), encoding="utf-8")
    (tmp_path / "concepts" / "variance.md").write_text("Variance.\n", encoding="utf-8")
    return tmp_path


def run(wiki: Path) -> int:
    return check_links.main(["check_links.py", str(wiki)])


def test_valid_citations_pass(tmp_path):
    wiki = make_wiki(tmp_path, "Unbiased[^1], and see [[variance]][^2].\n\n## Notes\n\n"
                               "[^1]: [[smith-2024-example#^thm-1|Smith 2024, §thm-1]]\n"
                               "[^2]: [[smith-2024-example#^sec-3|Smith 2024, §sec-3]]\n")
    assert run(wiki) == 0


def test_fabricated_anchor_in_a_real_source_fails(tmp_path, capsys):
    wiki = make_wiki(tmp_path, "Claim[^1].\n\n## Notes\n\n"
                               "[^1]: [[smith-2024-example#^thm-9|Smith 2024, §thm-9]]\n")
    assert run(wiki) == 1
    assert "no ^thm-9 in sources/smith-2024-example.md" in capsys.readouterr().err


def test_unknown_source_fails(tmp_path):
    wiki = make_wiki(tmp_path, "Claim[^1].\n\n## Notes\n\n[^1]: [[jones-2023-missing#^thm-1|Jones 2023]]\n")
    assert run(wiki) == 1


def test_footnote_without_definition_fails(tmp_path, capsys):
    wiki = make_wiki(tmp_path, "Claim[^1] and another[^2].\n\n## Notes\n\n"
                               "[^1]: [[smith-2024-example#^thm-1|Smith 2024, §thm-1]]\n")
    assert run(wiki) == 1
    assert "[^2] has no [^2]: definition" in capsys.readouterr().err


def test_unused_footnote_definition_is_only_a_warning(tmp_path, capsys):
    wiki = make_wiki(tmp_path, "Claim.\n\n## Notes\n\n"
                               "[^1]: [[smith-2024-example#^thm-1|Smith 2024, §thm-1]]\n")
    assert run(wiki) == 0
    assert "UNUSED FOOTNOTE DEFINITIONS" in capsys.readouterr().err


def test_red_concept_link_is_only_a_warning(tmp_path):
    assert run(make_wiki(tmp_path, "See [[not-written-yet]].\n")) == 0


def test_syntax_examples_in_code_are_ignored(tmp_path):
    wiki = make_wiki(tmp_path, "Write citations as `[[source#^made-up]]` with a `[^1]` note.\n\n"
                               "```\n[^2]: [[other#^x]]\n```\n")
    assert run(wiki) == 0


def test_example_wiki_passes():
    assert run(EXAMPLE) == 0


@pytest.mark.parametrize("name", ["build_alias_index.py", "build_backlinks.py",
                                  "check_links.py", "unused_claims.py"])
def test_example_wiki_ships_the_current_scripts(name):
    assert (EXAMPLE / "scripts" / name).read_bytes() == (ROOT / "scripts" / name).read_bytes()
