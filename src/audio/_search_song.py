# src/audio/_search_song.py
# For getting audios


# Imports
from naters_utils.functions import MatchCall
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait


# Type definitions
SearchResponse = tuple[list[str], list[str]]


# Definitions
class SearchSong:
    """Holding stuff"""
    
    # Init
    def __init__(self) -> None:
        """Initialize the 'function'"""
        
        # Initialize webdriver
        options = Options()
        options.add_argument("--headless")
        
        self.driver = webdriver.Firefox(options=options)
    
    
    # Call method
    __call__ = MatchCall()
    
    @__call__.case()
    def kevin(self, query: str) -> SearchResponse:
        # Get the music webpage
        self.driver.get("https://incompetech.com/music/royalty-free/music.html")
        
        # Get search bar element
        search_bar_elem = WebDriverWait(self.driver, 5).until(lambda x: x.find_element(By.ID, "incompetechSearchSearchText"))
        
        # Input the query
        search_bar_elem.send_keys(query)
        
        # Get song elements
        song_elems = self.driver.find_elements(By.CLASS_NAME, "search-result-row")
        
        # Get the song names
        song_names = [elem.find_element(By.TAG_NAME, "b").text for elem in song_elems]
        
        # Get the download links
        download_links = []
        
        # Get the download links
        for elem in song_elems:
            # Click the song element
            elem.click()
            
            # Get the download button
            download_button = self.driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div[2]/table/tbody/tr/td[1]/div/div/div[1]/a[1]")
            
            # Return the song link
            download_links.append(download_button.get_attribute('href'))
        
        # Return results
        return song_names, download_links
    
    @__call__.case()
    def ncs(self, query: str) -> SearchResponse:
        # Get the music webpage
        self.driver.get(f"https://ncs.io/music-search?q={query}")
        
        try:
            # Get song elements
            song_elems = WebDriverWait(self.driver, 5).until(lambda x: x.find_elements(By.CLASS_NAME, "tablesorter"))[0].find_elements(By.TAG_NAME, "tr")[1:]
            
        except TimeoutException:
            return [], []
        
        else:
            # Get song names
            song_names = [elem.find_element(By.TAG_NAME, "p").text for elem in song_elems]
            
            # Get download links
            download_links = [elem.find_element(By.TAG_NAME, "a").get_attribute("data-url") for elem in song_elems]
            
            # Return results
            return song_names, download_links
    
    @__call__.case()
    def url(self, query: str) -> SearchResponse:
        # Get the audio source
        try:
            self.driver.get(query)
        except WebDriverException:
            return [], []
        else:
            return [query], [query]

search_song = SearchSong()
