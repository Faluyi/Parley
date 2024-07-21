import praw
import requests
from properties import *
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self) -> None:
        # Initialize the Reddit instance
        self.reddit = praw.Reddit(
            client_id=parley_client_id,
            client_secret=parley_client_secret,
            user_agent='u/AmbassadorFull7304'
        )
    
    def scrape_blog(self, urls: list) -> dict:
        blog_content = {}
        
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract the title
                title_element = soup.find('h1')
                title = title_element.text if title_element else "No Title"
                blog_content[title] = ""
                
                # Extract the article content
                content = soup.find('div')
                if content:
                    paragraphs = content.find_all('p')
                    for para in paragraphs:
                        blog_content[title] += para.text
                else:
                    blog_content[title] = "No content found"
            else:
                print(f"Failed to retrieve URL: {url}")
                blog_content[url] = "Failed to retrieve content"
                
        return blog_content
    
    
    def scrape_subreddit(self, subreddits: list) -> dict:
        content = {}
        
        for sub in subreddits:
            # Access the subreddit
            subreddit = self.reddit.subreddit(sub)

            # Search for posts mentioning "b2"
            search_results = subreddit.search('b2', limit=10)

            for post in search_results:
                
                content[post.title] = post.selftext
        
        return content
            
            
    def scrape_and_merge_content(self, blog_urls: list, subreddits: list) -> dict:
        
        merged_content = {"blog_content": "", "subreddit_content": ""}
        
        blog_content = self.scrape_blog(blog_urls)
        subreddit_content = self.scrape_subreddit(subreddits)
        
        for ct in blog_content.values():
            merged_content["blog_content"] += f"\n{ct}"
            
        for ct in subreddit_content.values():
            merged_content["subreddit_content"] += f"\n{ct}"
            
        return merged_content
    
    
def main():
    scraper = Scraper()

    urls = ["https://www.backblaze.com/blog/ai-video-understanding-in-your-apps-with-twelve-labs-and-backblaze/", "https://www.backblaze.com/blog/announcing-event-notifications/"]
    subreddits = ['backblaze']
    scraped_content = scraper.scrape_blog(urls)
    scraped_subreddit_content = scraper.scrape_subreddit(subreddits)
    
    for ct in scraped_content:
        print("\n\n", ct, "\n", scraped_content[ct])
        
    for ct in scraped_subreddit_content:
        print("\n\n Subreddit Contents \n",)
        print("\n\n", ct, "\n", scraped_subreddit_content[ct])
        
    merged_content = scraper.scrape_and_merge_content(urls, subreddits)
    print("\n\nMerged Content \n", merged_content)


if __name__ == '__main__':
    main()