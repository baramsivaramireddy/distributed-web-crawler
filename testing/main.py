

from bs4 import BeautifulSoup




#     all_links = set([worker.remove_params(link.get('href')) for link in soup.find_all('a')     if link.get('href') and worker.is_valid_url(link.get('href'))
# ])
 
from urllib.parse import urlparse,urlunparse ,urljoin
def is_valid_url(url):
       
       
        global target_domain
        
        
        absolute_url = urljoin(f"http://{'example.com'}", url)
        parsed = urlparse(absolute_url)
        return all([
            parsed.scheme in ["http", "https"],
            parsed.netloc == 'example.com'
        ])


html_doc = """
<html>
  <body>
    <!-- Absolute URLs -->
    <a href="https://example.com/page1?utm_source=ads">Example Page 1</a>
    <a href="http://example.org/page2?ref=123">Example Page 2</a>

    <!-- Relative URLs -->
    <a href="/about?session=abc">About Us</a>
    <a href="contact">Contact</a>

    <!-- Invalid URLs -->
    <a href="javascript:void(0)">Click Me</a>
    <a>No href here</a>
  </body>
</html>
"""
soup = BeautifulSoup(html_doc, "html.parser")

def process_url(allLinks):
    
    all_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and is_valid_url(href):
            parsed = urlparse(href)
            if not parsed.scheme and not parsed.netloc:  
                # relative → join with domain
                full_url = urljoin(BASE_URL, href)
            else:
                # absolute → keep as is
                full_url = href
            all_links.append(full_url)
