


from worker import worker


import os 

from dotenv import load_dotenv


load_dotenv()

SEED_URL = os.getenv('SEED_URL', 'https://wikipedia.org')

worker.crawl(SEED_URL)

