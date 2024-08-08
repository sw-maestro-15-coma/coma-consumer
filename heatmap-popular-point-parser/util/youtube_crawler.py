from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from ..domain.youtube_heatmap import YoutubeHeatmap


class YoutubeCrawler:
    driver: WebDriver

    def __init__(self):
        self.driver = self.__create_selenium_driver()

    def get_most_replayed_heatmap(self, video_url: str) -> YoutubeHeatmap:
        try:
            self.driver.get(video_url)
            self.__wait_for_ad()
            self.__wait_for_video()
            return self.__get_youtube_heatmap()
        except Exception as e:
            raise Exception("Failed to get heatmap" + e)
        finally:
            self.driver.quit()

    def __create_selenium_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")

        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def __wait_for_ad(self):
        try:
            skip_ad_button = WebDriverWait(self.driver, 15).until(
                ec.element_to_be_clickable(("class name", "ytp-ad-skip-button"))
            )
            skip_ad_button.click()
        except:
            pass

    def __wait_for_video(self):
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(("css selector", "video"))
        )

    def __get_youtube_heatmap(self) -> YoutubeHeatmap:
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        return YoutubeHeatmap(
            svgs=self.__get_chapter_svgs(soup),
            chapter_widths=self.__get_video_chapter_widths(soup),
            video_length=self.__get_video_length(soup),
        )

    def __get_video_length(self, soup: BeautifulSoup) -> int:
        video_length = soup.select(".ytp-time-duration")[0].contents[0]
        splitted_time = video_length.split(":")

        return sum(
            int(time) * (60 ** (len(splitted_time) - 1 - index))
            for index, time in enumerate(splitted_time)
        )

    def __get_chapter_svgs(self, soup: BeautifulSoup) -> list[str]:
        return [
            chapter.get("d")
            for chapter in soup.select(".ytp-heat-map-svg > defs > clipPath > path")
        ]

    def __get_video_chapter_widths(self, soup: BeautifulSoup) -> list[int]:
        return [
            int(chapter.get("style").split("width: ")[1].split("px")[0])
            for chapter in soup.select(".ytp-chapter-hover-container")
        ]
