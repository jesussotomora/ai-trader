import os
import pytest
from src.data.news_scraper import NewsScraperService, ArticleData

def test_article_caching(tmp_path):
    db_path = str(tmp_path / "test_news.db")
    scraper = NewsScraperService(db_path=db_path)
    
    mock_url = "https://example.com/test-news-article"
    mock_article = ArticleData(
        url=mock_url,
        title="Test Financial News",
        full_text="Apple reports record Q3 earnings with strong iPhone sales.",
        summary="Apple reports record Q3 earnings.",
        keywords=["Apple", "earnings", "iPhone"]
    )
    
    scraper.cache_article(mock_article)
    cached = scraper.get_cached_article(mock_url)
    
    assert cached is not None
    assert cached.title == "Test Financial News"
    assert "Apple" in cached.keywords
