import os

from firecrawl import V1FirecrawlApp, V1ScrapeOptions

from dotenv import load_dotenv

class FirecrawlService:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY enviroment variable")
        self.app = V1FirecrawlApp(api_key=api_key)

    def search_companies(self, query: str, num_results: int):
        try:
            result = self.app.search(
                query=query,
                limit=num_results,
                scrape_options=V1ScrapeOptions(
                    formats=["markdown"]
                )
            )
            return result
        except Exception as e:
            print(e)
            return None
        
    def scrape_company_pages(self, url: str):
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"]
            )
            return result
        except Exception as e:
            print(e)
            return None