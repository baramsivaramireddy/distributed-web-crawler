# Distributed Web Crawler with Task Tracking and Analytics

## Overview
This project is a distributed web crawler that can fetch and store web pages from a given seed URL. 
It supports task tracking, rate limiting, distributed workers, and real-time analytics through a React dashboard. 
The system is fully containerized and can be deployed using Docker Compose.

## Features
- Crawl websites starting from a seed URL
- Store crawled HTML content in PostgreSQL
- Avoid duplicate visits using Redis
- Rate limiting (10 pages per minute)
- Distributed workers with RabbitMQ
- Task tracking with job and task tables
- Real-time monitoring and analytics dashboard
- Dockerized setup for deployment

## Tech Stack
- **Backend:** Python (Selenium, BeautifulSoup, psycopg2)
- **Message Queue:** RabbitMQ
- **Cache/State:** Redis
- **Database:** PostgreSQL
- **Dashboard:** React + Chart.js
- **Deployment:** Docker, Docker Compose

## Project Roadmap
- [x] Stage 1: Crawl single page → store in PostgreSQL
- [x] Stage 2: Recursive crawling
- [x] Stage 3: URL deduplication with Redis (done not with redis)
- [ ] Stage 4: Rate limiting
- [ ] Stage 5: RabbitMQ integration
- [ ] Stage 6: Multiple workers
- [ ] Stage 7: Task tracking
- [ ] Stage 8: Basic dashboard
- [ ] Stage 9: Analytics dashboard
- [ ] Stage 10: Dockerization
- [ ] Stage 11: Cloud deployment

## Setup
```bash
git clone https://github.com/baramsivaramireddy/distributed-web-crawler.git
cd distributed-web-crawler
python -m venv env
source env/bin/activate   #On Windows:env\Scripts\activate
pip install -r requirements.txt
