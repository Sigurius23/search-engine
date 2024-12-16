from typing import Dict, List, Set
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import shutil

class Indexer:
    def __init__(self, index_dir: str = "index"):
        self.index_dir = index_dir
        self.schema = Schema(
            url=ID(stored=True, unique=True),
            title=TEXT(stored=True),
            content=TEXT(stored=True)
        )
        
        # Create or clear index directory
        if os.path.exists(index_dir):
            shutil.rmtree(index_dir)
        os.makedirs(index_dir)
        
        self.ix = create_in(index_dir, self.schema)
    
    def add_documents(self, pages: Dict[str, dict]) -> None:
        """Add documents to the index."""
        writer = self.ix.writer()
        
        print(f"\nIndexing {len(pages)} pages:")  # Debug print
        for url, data in pages.items():
            print(f"\nIndexing: {url}")  # Debug print
            print(f"Title: {data['title']}")
            print(f"Content length: {len(data['text'])} characters")
            
            writer.add_document(
                url=url,
                title=data['title'],
                content=data['text']
            )
        
        writer.commit()
        print("\nIndexing complete!")
    
    def search(self, query_string: str, limit: int = 10) -> List[dict]:
        """Search the index and return matching documents."""
        print(f"\nSearching for: {query_string}")  # Debug print
        with self.ix.searcher() as searcher:
            # Search in both title and content
            query = QueryParser("content", self.ix.schema).parse(query_string)
            title_query = QueryParser("title", self.ix.schema).parse(query_string)
            
            # Combine the queries with OR
            from whoosh.query import Or
            combined_query = Or([query, title_query])
            
            results = searcher.search(combined_query, limit=limit)
            
            print(f"Found {len(results)} results")  # Debug print
            
            if len(results) == 0:
                return [{
                    'url': '#',
                    'title': 'No Results Found',
                    'content': f'Sorry, no documents were found containing "{query_string}". Try different search terms.'
                }]
            
            return [{
                'url': result['url'],
                'title': result['title'],
                'content': result['content'][:200] + '...'  # Preview text
            } for result in results]

# Test the indexer
if __name__ == "__main__":
    from crawler import Crawler
    
    # Test crawling and indexing
    TEST_URL = "https://vm009.rz.uos.de/crawl/index.html"
    crawler = Crawler(TEST_URL)
    pages = crawler.crawl()
    
    indexer = Indexer()
    indexer.add_documents(pages)
    
    # Test some searches
    test_queries = ["page", "test", "link", "the"]
    for query in test_queries:
        print(f"\nTesting search for '{query}':")
        results = indexer.search(query)
        for result in results:
            print(f"- {result['url']}: {result['title']}") 