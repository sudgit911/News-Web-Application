import unittest
from app import fetch_articles

class TestFetchArticles(unittest.TestCase):

    def test_fetch_articles_return_list(self):
        # Test that fetch articles function returns a list
        articles = fetch_articles(1)
        self.assertIsInstance(articles, list)
    
    def test_fetch_articles_pagination(self):
        # Test that fetch_articles function handles pagination correctly
        articles_page1 = fetch_articles(1)
        articles_page2 = fetch_articles(2)
        self.assertNotEqual(articles_page1, articles_page2) # Pages should have

    def test_fetch_articles_topic_filtering(self):
        # Test that fetch_articles function handles different topics correctly
        articles_politics = fetch_articles(1, 'politics')
        articles_technology = fetch_articles(1,'technology' )
        self.assertTrue(all(article['title '] for article in articles_politics))
        self.assertTrue(all(article['title '] for article in articles_technology))

    def test_fetch_articles_handles_exceptions(self):
        # Test that fetch_articles function handles exceptions gracefully
        articles = fetch_articles(9999) # Invalid page number
        self.assertEqual(articles, []) # Should return an empty list

if __name__ == '__main__':
    unittest.main()        