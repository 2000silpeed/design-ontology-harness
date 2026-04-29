from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


def _load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


sync_issue = _load_script("sync_issue_template_presets", "sync-issue-template-presets.py")
verify_demo = _load_script("verify_demo_scripts", "verify-demo-scripts.py")
security_scan = _load_script("security_scan_launch", "security-scan-launch.py")


def test_sync_issue_template_presets_updates_dropdown(tmp_path: Path):
    presets_dir = tmp_path / "presets"
    presets_dir.mkdir()
    (presets_dir / "matrix.json").write_text(
        json.dumps(
            {
                "presets": [
                    {"id": "dashboard--minimal-tech"},
                    {"id": "commerce--bold-confident"},
                ]
            }
        ),
        encoding="utf-8",
    )
    template = tmp_path / "preset-feedback.yml"
    template.write_text(
        """body:
  - type: dropdown
    id: preset_id
    attributes:
      label: preset
      description: 카탈로그 15종 중에서 선택하세요. old
      options:
        - old--preset
        - other (specify in body)
    validations:
      required: true
""",
        encoding="utf-8",
    )

    changed = sync_issue.sync_template(template, sync_issue.load_preset_ids(presets_dir), write=True)

    text = template.read_text(encoding="utf-8")
    assert changed
    assert "카탈로그 2종" in text
    assert "dashboard--minimal-tech" in text
    assert "commerce--bold-confident" in text
    assert "old--preset" not in text


def test_verify_demo_scripts_parses_free_text_and_question_flow():
    text = """
### Demo 1 — Foo (`dashboard--minimal-tech`)

**입력**:
```
/design-start "한국어 SaaS 관리자 대시보드, 미니멀 테크"
```

**예상 매칭 출력**:
```
1. ⭐ dashboard--minimal-tech  [High]
```

### Demo 2 — Bar (`commerce--editorial-warm`)

**입력**:
```
/design-start
? 뭘 만들고 있어요?  → ④ commerce
? 분위기는?           → ② editorial-warm
? 색상 모드?          → ② light
? 스택?               → ① nextjs-tailwind-shadcn
? 한글 UI 인가요?     → Y
```

**예상 매칭 출력**:
```
1. ⭐ commerce--editorial-warm  [High]
```
"""

    scenarios = verify_demo.parse_scenarios(text)

    assert len(scenarios) == 2
    assert scenarios[0].query.free_text == "한국어 SaaS 관리자 대시보드, 미니멀 테크"
    assert scenarios[1].query.app_mode == "commerce"
    assert scenarios[1].query.brand_tone == "editorial-warm"
    assert scenarios[1].query.color_mode == "light"
    assert scenarios[1].query.locale == "ko"


def test_security_scan_launch_finds_high_confidence_token(tmp_path: Path):
    safe = tmp_path / "safe"
    safe.mkdir()
    (safe / "README.md").write_text("token is a documentation word\n", encoding="utf-8")
    assert security_scan.scan_roots([safe]) == []

    leaked = tmp_path / "leaked"
    leaked.mkdir()
    fake_token = "ghp_" + "abcdefghijklmnopqrstuvwxyzABCDE12345"
    (leaked / "secret.txt").write_text(
        f"{fake_token}\n",
        encoding="utf-8",
    )
    findings = security_scan.scan_roots([leaked])
    assert findings
    assert "github-token" in findings[0]
