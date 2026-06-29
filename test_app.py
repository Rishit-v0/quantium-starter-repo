import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app import app


# ── Shared browser setup ──────────────────────────────────────────────────────
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()


# ── Test 1: Header is present ─────────────────────────────────────────────────
def test_header_present(dash_duo):
    """Verify the H1 header renders on the page."""
    dash_duo.start_server(app)

    dash_duo.wait_for_element("h1", timeout=10)
    header = dash_duo.find_element("h1")

    assert header is not None, "Header <h1> element was not found on the page"
    assert "Soul Foods" in header.text, (
        f"Header text did not contain 'Soul Foods'. Got: '{header.text}'"
    )


# ── Test 2: Visualisation (chart) is present ──────────────────────────────────
def test_chart_present(dash_duo):
    """Verify the Plotly line chart renders on the page."""
    dash_duo.start_server(app)

    # Wait for the Graph container to appear
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)

    # Plotly renders the actual SVG chart inside a .js-plotly-plot div
    # Wait for that inner element to confirm the chart has fully rendered
    dash_duo.wait_for_element("#sales-line-chart .js-plotly-plot", timeout=15)
    chart = dash_duo.find_element("#sales-line-chart .js-plotly-plot")

    assert chart is not None, "Plotly chart (.js-plotly-plot) was not found inside #sales-line-chart"


# ── Test 3: Region picker is present ─────────────────────────────────────────
def test_region_picker_present(dash_duo):
    """Verify the region radio button filter renders with all five options."""
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#region-filter", timeout=10)
    region_picker = dash_duo.find_element("#region-filter")

    assert region_picker is not None, (
        "Region picker element #region-filter was not found"
    )
    assert region_picker.is_displayed(), (
        "Region picker was found but is not visible"
    )

    picker_text = region_picker.text.lower()
    for region in ["all", "north", "east", "south", "west"]:
        assert region in picker_text, (
            f"Expected region option '{region}' not found. Got: '{picker_text}'"
        )