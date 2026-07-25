from __future__ import annotations

from pathlib import Path

import pytest

from design_ontology_harness.implementation_linter import lint_implementation


KOREAN_COPY = (
    "구단 순위와 경기 일정을 한 화면에서 확인하고 관심 팀의 다음 경기를 놓치지 않도록 돕는 대시보드입니다."
)


def _codes(report) -> set[str]:
    return {issue.code for issue in report.issues}


def _write_tokens(tmp_path: Path, extra_light: str = "", extra_dark: str = "") -> None:
    tokens_path = tmp_path / "design-system" / "tokens.css"
    tokens_path.parent.mkdir(parents=True, exist_ok=True)
    tokens_path.write_text(
        f""":root {{
  --ds-color-canvas: #FFFFFF;
  --ds-color-surface: #FFFFFF;
  --ds-color-ink: #0F172A;
  --ds-color-ink-muted: #475569;
  --ds-color-ink-faint: #7C8899;
  --ds-color-ink-subtle: #94A3B8;
  --ds-color-ink-dim: #475569;
  --ds-color-border: #D6DDE6;
  --ds-color-border-strong: #475569;
  --ds-color-success: #15803D;
  --ds-color-danger: #B91C1C;
  --ds-leading-tight: 1.2;
  --ds-leading-body: 1.65;
  --ds-leading-relaxed: 1.65;
  --ds-tracking-body: 0em;
  --ds-tracking-loose: 0.06em;
  --ds-wrap-word-break: keep-all;
  --ds-wrap-overflow: normal;
  --ds-text-md: 1rem;
  --ds-text-3xl: 1.875rem;
{extra_light}
}}

html[data-theme="dark"] {{
  --ds-color-canvas: #0F172A;
  --ds-color-surface: #0F172A;
  --ds-color-ink: #F8FAFC;
  --ds-color-ink-muted: #CBD5E1;
  --ds-color-ink-faint: #6B7280;
  --ds-color-ink-subtle: #64748B;
  --ds-color-ink-dim: #334155;
  --ds-color-border: #334155;
  --ds-color-border-strong: #94A3B8;
  --ds-color-success: #4ADE80;
  --ds-color-danger: #F87171;
{extra_dark}
}}
""",
        encoding="utf-8",
    )


def _write_ui(tmp_path: Path, css: str, body: str = "<main class='app-shell'></main>") -> Path:
    _write_tokens(tmp_path)
    (tmp_path / "index.html").write_text(
        f"<html><head><link rel='stylesheet' href='styles.css'></head><body>{body}</body></html>",
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(css, encoding="utf-8")
    return tmp_path


def _write_korean_ui(tmp_path: Path, css: str) -> Path:
    return _write_ui(
        tmp_path,
        css,
        body=f"<main class='app-shell'><p class='description'>{KOREAN_COPY}</p></main>",
    )


# ── DS100: 본문 행간 하한 ──


def test_ds100_flags_tight_body_leading(tmp_path: Path):
    _write_ui(tmp_path, ".article-copy { line-height: 1.3; }")
    report = lint_implementation(tmp_path)
    assert "DS100" in _codes(report)


def test_ds100_allows_relaxed_body_leading(tmp_path: Path):
    _write_ui(tmp_path, ".article-copy { line-height: var(--ds-leading-relaxed); }")
    report = lint_implementation(tmp_path)
    assert "DS100" not in _codes(report)


def test_ds100_resolves_leading_token_to_its_value(tmp_path: Path):
    _write_ui(tmp_path, ".article-copy { line-height: var(--ds-leading-tight); }")
    report = lint_implementation(tmp_path)
    assert "DS100" in _codes(report)


def test_ds100_ignores_display_type(tmp_path: Path):
    _write_ui(tmp_path, ".hero-title { line-height: 1.05; }")
    report = lint_implementation(tmp_path)
    assert "DS100" not in _codes(report)


def test_ds100_ignores_heading_element_inside_copy_container(tmp_path: Path):
    """`.status-copy h1`은 컨테이너 이름이 copy일 뿐 헤딩이다."""
    _write_ui(tmp_path, ".status-copy h1 { line-height: var(--ds-leading-tight); }")
    report = lint_implementation(tmp_path)
    assert "DS100" not in _codes(report)


def test_ds100_ignores_meta_rows(tmp_path: Path):
    _write_ui(tmp_path, ".detail-meta dd { line-height: 1.35; }")
    report = lint_implementation(tmp_path)
    assert "DS100" not in _codes(report)


def test_ds100_ignores_display_scale_blocks(tmp_path: Path):
    """이름이 본문 같아도 92px 헤드라인은 display 조판이고 좁은 행간이 정답이다."""
    _write_ui(
        tmp_path,
        ".thumb-copy strong { font-size: clamp(56px, 6vw, 92px); line-height: 0.98; }",
    )
    report = lint_implementation(tmp_path)
    assert "DS100" not in _codes(report)


def test_ds100_still_flags_body_scale_copy(tmp_path: Path):
    """clamp의 하한이 본문 크기면 제외 대상이 아니다."""
    _write_ui(
        tmp_path,
        ".article-copy p { font-size: clamp(15px, 2vw, 92px); line-height: 1.2; }",
    )
    report = lint_implementation(tmp_path)
    assert "DS100" in _codes(report)


def test_ds100_uses_korean_floor_on_korean_surface(tmp_path: Path):
    """1.55는 라틴 기준으로는 통과하지만 한글 표면에서는 미달이다."""
    _write_korean_ui(tmp_path, ".description { line-height: 1.55; }")
    report = lint_implementation(tmp_path)
    assert "DS100" in _codes(report)


def test_ds100_latin_surface_accepts_1_5(tmp_path: Path):
    _write_ui(tmp_path, ".article-copy { line-height: 1.5; }")
    report = lint_implementation(tmp_path)
    assert "DS100" not in _codes(report)


# ── DS101/DS102: 대비비 ──


def test_ds101_flags_low_contrast_body_text(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".meta-row { color: var(--ds-color-ink-subtle); background: var(--ds-color-surface); }",
    )
    report = lint_implementation(tmp_path)
    assert "DS101" in _codes(report)


def test_ds101_allows_ink_on_surface(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".meta-row { color: var(--ds-color-ink); background: var(--ds-color-surface); }",
    )
    report = lint_implementation(tmp_path)
    assert "DS101" not in _codes(report)


def test_ds101_uses_large_text_floor(tmp_path: Path):
    """ink-faint는 두 모드 모두 3~4.5:1 구간이라 본문에서만 걸려야 한다."""
    small = tmp_path / "small"
    large = tmp_path / "large"
    _write_ui(
        small,
        ".meta-row { color: var(--ds-color-ink-faint); background: var(--ds-color-surface); }",
    )
    _write_ui(
        large,
        ".stat-value { font-size: var(--ds-text-3xl); color: var(--ds-color-ink-faint);"
        " background: var(--ds-color-surface); }",
    )
    assert "DS101" in _codes(lint_implementation(small))
    assert "DS101" not in _codes(lint_implementation(large))


def test_ds101_checks_dark_mode_resolution(tmp_path: Path):
    """라이트에서는 통과하고 다크에서만 무너지는 쌍도 잡는다."""
    _write_ui(
        tmp_path,
        ".panel-note { color: var(--ds-color-ink-dim); background: var(--ds-color-surface); }",
    )
    report = lint_implementation(tmp_path)
    failures = [issue for issue in report.issues if issue.code == "DS101"]
    assert failures
    assert failures[0].snippet.endswith("(dark=1.72:1)")


def _write_tokens_with_dark_scope(tmp_path: Path, dark_scope: str) -> None:
    """어댑터마다 다크 오버라이드 스코프 형태가 다르다."""
    tokens_path = tmp_path / "design-system" / "tokens.css"
    tokens_path.parent.mkdir(parents=True, exist_ok=True)
    tokens_path.write_text(
        f""":root {{
  --ds-color-surface: #FFFFFF;
  --ds-color-ink-dim: #475569;
}}

{dark_scope} {{
  --ds-color-surface: #0F172A;
  --ds-color-ink-dim: #334155;
}}
""",
        encoding="utf-8",
    )


@pytest.mark.parametrize(
    "dark_scope",
    [
        'html[data-theme="dark"]',
        "[data-theme='dark']",
        ":root[data-theme='dark']",
        "@media (prefers-color-scheme: dark)",
    ],
)
def test_ds101_reads_every_dark_override_scope(tmp_path: Path, dark_scope: str):
    """스코프 형태를 하나만 인식하면 다크 모드를 라이트 값으로 판정해 조용히 통과시킨다."""
    _write_tokens_with_dark_scope(tmp_path, dark_scope)
    (tmp_path / "index.html").write_text(
        "<html><head><link rel='stylesheet' href='styles.css'></head>"
        "<body><main class='app-shell'></main></body></html>",
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        ".panel-note { color: var(--ds-color-ink-dim); background: var(--ds-color-surface); }",
        encoding="utf-8",
    )
    report = lint_implementation(tmp_path)
    failures = [issue for issue in report.issues if issue.code == "DS101"]
    assert failures, f"{dark_scope} 스코프의 다크 오버라이드를 읽지 못했다"
    assert "dark=" in failures[0].snippet


def test_ds102_flags_weak_control_boundary(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".search-input { background: var(--ds-color-surface); border: 1px solid var(--ds-color-border); }",
    )
    report = lint_implementation(tmp_path)
    assert "DS102" in _codes(report)


def test_ds102_allows_strong_control_boundary(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".search-input { background: var(--ds-color-surface); border: 1px solid var(--ds-color-border-strong); }",
    )
    report = lint_implementation(tmp_path)
    assert "DS102" not in _codes(report)


def test_ds102_ignores_filled_control_with_matching_border(tmp_path: Path):
    """채움형 버튼의 테두리는 배경과 같은 토큰이라 식별 단서가 아니다."""
    _write_ui(
        tmp_path,
        ".submit-button { background: var(--ds-color-ink); border: 1px solid var(--ds-color-ink); }",
    )
    report = lint_implementation(tmp_path)
    assert "DS102" not in _codes(report)


def test_ds102_ignores_decorative_dividers(tmp_path: Path):
    """카드 경계선은 WCAG 1.4.11 대상이 아니므로 컨트롤 셀렉터에서만 본다."""
    _write_ui(
        tmp_path,
        ".summary-card { background: var(--ds-color-surface); border: 1px solid var(--ds-color-border); }",
    )
    report = lint_implementation(tmp_path)
    assert "DS102" not in _codes(report)


# ── DS103: 색만으로 상태 표시 ──


def test_ds103_flags_color_only_status_dot(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .status-dot--success { background: var(--ds-color-success); }
        .status-dot--error { background: var(--ds-color-danger); }
        """,
        body=(
            "<ul><li><span class='status-dot--success'></span></li>"
            "<li><span class='status-dot--error'></span></li></ul>"
        ),
    )
    report = lint_implementation(tmp_path)
    assert "DS103" in _codes(report)


def test_ds103_reads_attribute_state_variants(tmp_path: Path):
    """`[data-status="…"]`는 --modifier 클래스만큼 흔한 상태 표현이다."""
    _write_ui(
        tmp_path,
        """
        .status-dot[data-status="pass"] { background: var(--ds-color-success); }
        .status-dot[data-status="rework"] { background: var(--ds-color-danger); }
        """,
        body=(
            "<ul><li><span class='status-dot' data-status='pass'></span></li>"
            "<li><span class='status-dot' data-status='rework'></span></li></ul>"
        ),
    )
    report = lint_implementation(tmp_path)
    assert "DS103" in _codes(report)


def test_ds103_accepts_shape_differentiated_attribute_variants(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .status-dot[data-status="pass"] { background: var(--ds-color-success); }
        .status-dot[data-status="rework"] {
          background: var(--ds-color-danger);
          border-radius: var(--ds-radius-none);
          transform: rotate(45deg);
        }
        """,
        body=(
            "<ul><li><span class='status-dot' data-status='pass'></span></li>"
            "<li><span class='status-dot' data-status='rework'></span></li></ul>"
        ),
    )
    report = lint_implementation(tmp_path)
    assert "DS103" not in _codes(report)


def test_ds103_allows_dot_paired_with_a_label(tmp_path: Path):
    """점 옆에 글자가 있으면 색이 유일한 단서가 아니다."""
    _write_ui(
        tmp_path,
        """
        .status-dot--success { background: var(--ds-color-success); }
        .status-dot--error { background: var(--ds-color-danger); }
        """,
        body=(
            "<ul><li><span class='status-dot--success'></span>통과</li>"
            "<li><span class='status-dot--error'></span>수정</li></ul>"
        ),
    )
    report = lint_implementation(tmp_path)
    assert "DS103" not in _codes(report)


def test_ds103_allows_shape_differentiated_status(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .status-dot--success { background: var(--ds-color-success); }
        .status-dot--error { background: var(--ds-color-danger); border-style: dashed; }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS103" not in _codes(report)


def test_ds103_ignores_labeled_badges(tmp_path: Path):
    """라벨이 있는 배지는 색이 유일한 단서가 아니다."""
    _write_ui(
        tmp_path,
        """
        .badge--success { background: var(--ds-color-success); }
        .badge--error { background: var(--ds-color-danger); }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS103" not in _codes(report)


# ── DS104: 서체 예산 ──


def test_ds104_flags_third_text_typeface(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .hero-title { font-family: var(--ds-font-display); }
        .section-title { font-family: var(--ds-font-heading); }
        .article-copy { font-family: var(--ds-font-body); line-height: 1.65; }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS104" in _codes(report)


def test_ds104_counts_families_not_tokens(tmp_path: Path):
    """display/heading/body가 같은 서체로 해석되면 서체는 1종이다."""
    _write_tokens(
        tmp_path,
        extra_light=(
            '  --ds-font-display: "Spoqa Han Sans Neo", sans-serif;\n'
            '  --ds-font-heading: "Spoqa Han Sans Neo", sans-serif;\n'
            '  --ds-font-body: "Spoqa Han Sans Neo", sans-serif;'
        ),
    )
    (tmp_path / "index.html").write_text(
        "<html><head><link rel='stylesheet' href='styles.css'></head>"
        "<body><main class='app-shell'></main></body></html>",
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .hero-title { font-family: var(--ds-font-display); }
        .section-title { font-family: var(--ds-font-heading); }
        .article-copy { font-family: var(--ds-font-body); line-height: 1.65; }
        """,
        encoding="utf-8",
    )
    report = lint_implementation(tmp_path)
    assert "DS104" not in _codes(report)


def test_ds104_still_flags_three_distinct_families(tmp_path: Path):
    _write_tokens(
        tmp_path,
        extra_light=(
            '  --ds-font-display: "Noto Serif KR", serif;\n'
            '  --ds-font-heading: "Wanted Sans", sans-serif;\n'
            '  --ds-font-body: "Pretendard", sans-serif;'
        ),
    )
    (tmp_path / "index.html").write_text(
        "<html><head><link rel='stylesheet' href='styles.css'></head>"
        "<body><main class='app-shell'></main></body></html>",
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .hero-title { font-family: var(--ds-font-display); }
        .section-title { font-family: var(--ds-font-heading); }
        .article-copy { font-family: var(--ds-font-body); line-height: 1.65; }
        """,
        encoding="utf-8",
    )
    report = lint_implementation(tmp_path)
    assert "DS104" in _codes(report)


def test_ds104_counts_per_surface_not_per_target(tmp_path: Path):
    """목업 여러 개가 한 프로젝트에 있으면 합산이 아니라 화면별로 세야 한다."""
    _write_tokens(
        tmp_path,
        extra_light=(
            '  --ds-font-display: "Noto Serif KR", serif;\n'
            '  --ds-font-heading: "Space Grotesk", sans-serif;\n'
            '  --ds-font-body: "Inter", sans-serif;'
        ),
    )
    for name, first, second in (
        ("a", "display", "heading"),
        ("b", "heading", "body"),
    ):
        (tmp_path / name).mkdir()
        (tmp_path / name / "index.html").write_text(
            "<html><head><link rel='stylesheet' href='styles.css'></head>"
            "<body><main class='app-shell'></main></body></html>",
            encoding="utf-8",
        )
        (tmp_path / name / "styles.css").write_text(
            f".t {{ font-family: var(--ds-font-{first}); }}\n"
            f".u {{ font-family: var(--ds-font-{second}); }}\n",
            encoding="utf-8",
        )
    report = lint_implementation(tmp_path)
    assert "DS104" not in _codes(report), "화면별 2종인데 합산해서 3종으로 읽었다"


def test_ds104_flags_a_single_surface_using_three_families(tmp_path: Path):
    _write_tokens(
        tmp_path,
        extra_light=(
            '  --ds-font-display: "Noto Serif KR", serif;\n'
            '  --ds-font-heading: "Wanted Sans", sans-serif;\n'
            '  --ds-font-body: "Pretendard", sans-serif;'
        ),
    )
    (tmp_path / "index.html").write_text(
        "<html><head><link rel='stylesheet' href='styles.css'></head>"
        "<body><main class='app-shell'></main></body></html>",
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        ".a { font-family: var(--ds-font-display); }\n"
        ".b { font-family: var(--ds-font-heading); }\n"
        ".c { font-family: var(--ds-font-body); }\n",
        encoding="utf-8",
    )
    report = lint_implementation(tmp_path)
    assert "DS104" in _codes(report)


def test_ds104_allows_mono_and_korean_pairing(tmp_path: Path):
    _write_korean_ui(
        tmp_path,
        """
        .hero-title { font-family: var(--ds-font-display); }
        .description { font-family: var(--ds-font-body); line-height: 1.65; }
        .kr-copy { font-family: var(--ds-font-ko); }
        .ticker { font-family: var(--ds-font-mono); }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS104" not in _codes(report)


# ── DS105: 한글 자간 ──


def test_ds105_flags_positive_tracking_on_korean_surface(tmp_path: Path):
    _write_korean_ui(
        tmp_path,
        ".description { letter-spacing: 0.05em; line-height: 1.65; word-break: keep-all; }",
    )
    report = lint_implementation(tmp_path)
    assert "DS105" in _codes(report)


def test_ds105_allows_negative_tracking(tmp_path: Path):
    _write_korean_ui(
        tmp_path,
        ".description { letter-spacing: -0.01em; line-height: 1.65; word-break: keep-all; }",
    )
    report = lint_implementation(tmp_path)
    assert "DS105" not in _codes(report)


def test_ds105_flags_positive_tracking_on_korean_heading(tmp_path: Path):
    _write_korean_ui(
        tmp_path,
        """
        .section-title { letter-spacing: 0.04em; }
        .description { line-height: 1.65; word-break: keep-all; }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS105" in _codes(report)


def test_ds105_allows_latin_uppercase_slot(tmp_path: Path):
    """uppercase는 한글에 무효한 선언이라 라틴 전용 슬롯 표시로 읽는다."""
    _write_korean_ui(
        tmp_path,
        """
        .section-title { letter-spacing: 0.08em; text-transform: uppercase; }
        .description { line-height: 1.65; word-break: keep-all; }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS105" not in _codes(report)


def test_ds105_ignores_wordmark_and_numeric_slots(tmp_path: Path):
    """워드마크·날짜·수치는 읽는 텍스트가 아니라 라틴 조판 관례가 유효한 자리다."""
    _write_korean_ui(
        tmp_path,
        """
        .wordmark { letter-spacing: 0.045em; }
        .kickoff-time { letter-spacing: 0.03em; }
        .stat-value { letter-spacing: 0.02em; }
        .description { line-height: 1.65; word-break: keep-all; }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS105" not in _codes(report)


def test_ds105_resolves_tracking_tokens(tmp_path: Path):
    """토큰으로 감싸도 값이 양수면 걸려야 한다."""
    _write_korean_ui(
        tmp_path,
        """
        .description {
          letter-spacing: var(--ds-tracking-loose);
          line-height: 1.65;
          word-break: keep-all;
        }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS105" in _codes(report)


def test_ds105_accepts_the_body_tracking_token(tmp_path: Path):
    _write_korean_ui(
        tmp_path,
        """
        .description {
          letter-spacing: var(--ds-tracking-body);
          line-height: 1.65;
          word-break: keep-all;
        }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS105" not in _codes(report)


def test_ds105_ignores_latin_surface(tmp_path: Path):
    _write_ui(tmp_path, ".article-copy { letter-spacing: 0.05em; line-height: 1.65; }")
    report = lint_implementation(tmp_path)
    assert "DS105" not in _codes(report)


# ── DS106: 한글 줄바꿈 계약 ──


def test_ds106_flags_korean_surface_without_keep_all(tmp_path: Path):
    _write_korean_ui(tmp_path, ".description { line-height: 1.65; }")
    report = lint_implementation(tmp_path)
    assert "DS106" in _codes(report)


def test_ds106_satisfied_by_keep_all(tmp_path: Path):
    _write_korean_ui(
        tmp_path,
        ".description { line-height: 1.65; word-break: keep-all; overflow-wrap: normal; }",
    )
    report = lint_implementation(tmp_path)
    assert "DS106" not in _codes(report)


def test_ds106_satisfied_by_the_wrap_token(tmp_path: Path):
    """토큰 소비가 권장 경로다. 리터럴만 인정하면 권장 경로가 벌을 받는다."""
    _write_korean_ui(
        tmp_path,
        """
        .description {
          line-height: var(--ds-leading-body);
          word-break: var(--ds-wrap-word-break);
          overflow-wrap: var(--ds-wrap-overflow);
        }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS106" not in _codes(report)


def test_ds106_still_fires_when_the_token_is_not_keep_all(tmp_path: Path):
    _write_korean_ui(
        tmp_path,
        ".description { line-height: 1.65; word-break: var(--ds-leading-tight); }",
    )
    report = lint_implementation(tmp_path)
    assert "DS106" in _codes(report)


def test_ds106_ignores_latin_surface(tmp_path: Path):
    _write_ui(tmp_path, ".article-copy { line-height: 1.65; }")
    report = lint_implementation(tmp_path)
    assert "DS106" not in _codes(report)


def test_ds106_ignores_korean_comments_only(tmp_path: Path):
    """주석 안의 한글만으로는 한글 표면이 아니다."""
    _write_ui(
        tmp_path,
        "/* 이 파일은 본문 타이포그래피 규칙을 담고 있으며 한글 주석이 길게 달려 있습니다 */\n"
        ".article-copy { line-height: 1.65; }",
    )
    report = lint_implementation(tmp_path)
    assert "DS106" not in _codes(report)


# ── DS107: 양쪽 정렬 ──


def test_ds107_flags_justified_text(tmp_path: Path):
    _write_ui(tmp_path, ".article-copy { text-align: justify; line-height: 1.65; }")
    report = lint_implementation(tmp_path)
    assert "DS107" in _codes(report)


def test_ds107_allows_left_align(tmp_path: Path):
    _write_ui(tmp_path, ".article-copy { text-align: left; line-height: 1.65; }")
    report = lint_implementation(tmp_path)
    assert "DS107" not in _codes(report)


# ── 회귀: 규칙이 없는 표면은 조용해야 한다 ──


def test_reference_screen_passes_implementation_lint():
    """참조 화면이 게이트를 통과하는 상태로 유지되는지 지킨다.

    규칙만 있고 통과 사례가 없으면 에이전트가 볼 본보기가 없다. 이 프로젝트가
    빨간불이 되면 참조로서의 자격을 잃으므로 테스트로 고정한다.
    """
    project = Path(__file__).resolve().parent.parent / "projects" / "gyeopmal-review-desk"
    report = lint_implementation(project)
    assert report.checked_files, "참조 화면의 구현 파일을 찾지 못했다"
    assert report.issues == [], "\n".join(
        f"[{issue.code}] {issue.path}:{issue.line} {issue.message}" for issue in report.issues
    )


def test_clean_korean_surface_reports_no_base_rule_issues(tmp_path: Path):
    _write_korean_ui(
        tmp_path,
        """
        .description {
          font-family: var(--ds-font-ko);
          color: var(--ds-color-ink);
          background: var(--ds-color-surface);
          line-height: 1.65;
          letter-spacing: -0.01em;
          text-align: left;
          word-break: keep-all;
          overflow-wrap: normal;
        }
        """,
    )
    report = lint_implementation(tmp_path)
    base_rule_codes = {code for code in _codes(report) if code.startswith("DS1")}
    assert base_rule_codes == set()
