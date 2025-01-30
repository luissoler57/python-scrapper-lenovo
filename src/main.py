"""_summary_

    Raises:
        e: _description_
    """

from lenovo_scrapper.browser.driver import BrowserDriver
from lenovo_scrapper.config import selectors, setting
from lenovo_scrapper.scraper import LenovoWarrantyScraper
from lenovo_scrapper.utils.logger import configure_logger


def main():
    """_summary_

    Raises:
        e: _description_
    """
    logger = configure_logger("main")
    app_setting = setting.Setting()
    driver = None

    try:
        # Initialize the Chrome WebDriver instance
        driver_manager = BrowserDriver(app_setting)
        driver = driver_manager.create_driver()

        # Initialize the Lenovo warranty scraper
        scraper = LenovoWarrantyScraper(
            driver=driver,
            settings=app_setting,
            selectors=selectors.Selectors(),
        )

        result = scraper.perform_search(serial="PF3DGHLB")
        print(result)

    except Exception as e:
        logger.error("An error occurred: %s", str(e))
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
