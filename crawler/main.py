


from worker import worker


import os 


SEED_URL = os.getenv('SEED_URL', 'https://wikipedia.org')
worker.crawl(SEED_URL)

