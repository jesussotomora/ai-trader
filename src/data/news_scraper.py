import json
import sqlite3
from typing import List, Optional
from pydantic import BaseModel
from newspaper import Article


class ArticleData(BaseModel):
    url: str
    title: str
    full_text: str
    summary: str
    keywords: List[str]


class NewsScraperService:
    def __init__(self, db_path: str = "news_cache.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS article_cache (
                    url TEXT PRIMARY KEY,
                    title TEXT,
                    full_text TEXT,
                    summary TEXT,
                    keywords TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def get_cached_article(self, url: str) -> Optional[ArticleData]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT url, title, full_text, summary, keywords FROM article_cache WHERE url = ?", (url,))
            row = cursor.fetchone()
            if row:
                return ArticleData(
                    url=row[0],
                    title=row[1],
                    full_text=row[2],
                    summary=row[3],
                    keywords=json.loads(row[4])
                )
        return None

    def cache_article(self, article: ArticleData):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO article_cache (url, title, full_text, summary, keywords)
                VALUES (?, ?, ?, ?, ?)
            """, (article.url, article.title, article.full_text, article.summary, json.dumps(article.keywords)))
            conn.commit()

    def fetch_and_parse(self, url: str) -> ArticleData:
        cached = self.get_cached_article(url)
        if cached:
            return cached

        art = Article(url)
        art.download()
        art.parse()
        try:
            art.nlp()
            summary = art.summary
            keywords = art.keywords
        except Exception:
            summary = art.text[:300]
            keywords = []

        data = ArticleData(
            url=url,
            title=art.title or "Untitled",
            full_text=art.text or "",
            summary=summary or "",
            keywords=keywords or []
        )
        self.cache_article(data)
        return data
