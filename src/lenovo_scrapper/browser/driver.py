import os
import tempfile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BrowserDriver:
    """Class to manage Chrome WebDriver instance with custom settings."""

    def __init__(self, settings):
        self.setting = settings
        self.driver = None

    def create_driver(self, headless: bool = True):
        """Create and configure a new Chrome WebDriver instance.

        Args:
            headless (bool, optional): Run browser in headless mode. Defaults to True.

        Returns:
            webdriver.Chrome: Configured Chrome WebDriver instance.
        """
        options = Options()
        options.add_argument(f"user-agent={self.setting.USER_AGENT}")

        # Set the Chrome browser options
        for option in self.setting.CHROME_OPTIONS:
            if headless and "headless" in option:
                options.add_argument(option)
            options.add_argument(option)

        user_data_dir = os.path.join(tempfile.gettempdir(), "chrome-data")
        os.makedirs(user_data_dir, exist_ok=True)
        options.add_argument(f"user-data-dir={user_data_dir}")

        # Create the Chrome browser driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )

        return self.driver
