from pathlib import Path

from design_ontology_harness.benchmark_kb import get_benchmark_systems

REPO_ROOT = Path(__file__).resolve().parents[1]


def _seed_urls(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def test_seed_packs_have_no_duplicate_urls():
    professional = _seed_urls(REPO_ROOT / "seeds/professional-design-systems.txt")
    browser_required = _seed_urls(REPO_ROOT / "seeds/browser-required-official-design-systems.txt")
    combined = professional + browser_required

    assert len(professional) == len(set(professional))
    assert len(browser_required) == len(set(browser_required))
    assert len(combined) == len(set(combined))


def test_recent_design_system_candidates_are_crawler_friendly_seeds():
    professional = set(_seed_urls(REPO_ROOT / "seeds/professional-design-systems.txt"))
    browser_required = set(_seed_urls(REPO_ROOT / "seeds/browser-required-official-design-systems.txt"))

    expected = {
        "https://cloudscape.design/",
        "https://paste.twilio.design/",
        "https://garden.zendesk.com/",
        "https://helios.hashicorp.design/",
        "https://f36.contentful.com/",
        "https://nordhealth.design/",
        "https://modus.trimble.com/",
        "https://shopify.dev/docs/api/app-home/web-components",
    }

    assert expected <= professional
    assert "https://polaris-react.shopify.com/" not in browser_required


def test_recent_benchmark_systems_are_available_for_matching():
    systems = {system["id"]: system for system in get_benchmark_systems()}

    for system_id in {
        "aws-cloudscape",
        "zendesk-garden",
        "contentful-forma-36",
        "nord-health",
        "trimble-modus",
        "salesforce-slds2",
    }:
        assert system_id in systems

    assert systems["shopify-polaris"]["url"] == "https://shopify.dev/docs/api/app-home/web-components"
