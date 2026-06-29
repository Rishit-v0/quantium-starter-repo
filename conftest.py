# conftest.py
import os
from webdriver_manager.chrome import ChromeDriverManager

def pytest_configure(config):
    """Add ChromeDriver to PATH before any tests run."""
    driver_path = ChromeDriverManager().install()
    # driver_path is the full path to chromedriver.exe
    # We need the folder containing it, not the .exe itself
    driver_dir = os.path.dirname(driver_path)
    os.environ["PATH"] = driver_dir + os.pathsep + os.environ["PATH"]