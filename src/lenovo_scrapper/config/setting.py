class Setting:
    """Configuration settings for the Lenovo scraper application.

    This class contains all the necessary configuration parameters including
    URLs, timeouts, user agent strings, and Chrome browser options.
    """

    BASE_URL = "https://support.lenovo.com/us/en/parts-lookup"
    DEFAULT_TIMEOUT = 1
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    CHROME_OPTIONS = ["--no-sandbox", "--disable-dev-shm-usage", "--headless=new"]

    @classmethod
    def get_chrome_options(cls):
        """Return the list of Chrome options."""
        return cls.CHROME_OPTIONS

    @classmethod
    def get_user_agent(cls):
        """Return the user agent string."""
        return cls.USER_AGENT
