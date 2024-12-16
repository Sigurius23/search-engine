from flask import Flask, render_template, request
from crawler import Crawler
from indexer import Indexer
import os

app = Flask(__name__)

# Initialize crawler and indexer
CRAWL_URL = "https://vm009.rz.uos.de/crawl/index.html"
indexer = None

# Update the index directory path
INDEX_DIR = os.path.join(os.path.dirname(__file__), 'index')

def initialize_search_engine():
    global indexer
    print("Initializing search engine...")
    crawler = Crawler(CRAWL_URL)
    print("Starting to crawl website...")
    pages = crawler.crawl()
    print(f"Crawled {len(pages)} pages")
    indexer = Indexer(index_dir=INDEX_DIR)
    print("Building search index...")
    indexer.add_documents(pages)
    print("Search engine ready!")

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Search Engine</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .search-form {{ margin-bottom: 20px; }}
                .search-input {{ padding: 10px; width: 300px; }}
                .search-button {{ padding: 10px 20px; }}
                .result {{ margin-bottom: 20px; }}
                .result-title {{ color: #1a0dab; }}
                .result-url {{ color: #006621; }}
                .result-preview {{ color: #545454; }}
            </style>
        </head>
        <body>
            <h1>Search Engine</h1>
            <form class="search-form" action="/search" method="get" onsubmit="return true;">
                <input type="text" name="q" class="search-input" placeholder="Enter search terms..." required>
                <button type="submit" class="search-button">Search</button>
            </form>
            <div id="status">
                {{"Search engine ready!" if indexer else "Initializing search engine..."}}
            </div>
        </body>
    </html>
    '''

@app.route('/search')
def search():
    try:
        query = request.args.get('q', '')
        print(f"Searching for: {query}")
        
        if not query:
            return home()
        
        if indexer is None:
            print("Error: Indexer not initialized!")
            return "Search engine is not initialized. Please restart the application."
        
        results = indexer.search(query)
        print(f"Found {len(results)} results")
        
        result_html = f'''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Search Results</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .search-form {{ margin-bottom: 20px; }}
                .search-input {{ padding: 10px; width: 300px; }}
                .search-button {{ padding: 10px 20px; }}
                .result {{ margin-bottom: 20px; }}
                .result-title {{ color: #1a0dab; }}
                .result-url {{ color: #006621; }}
                .result-preview {{ color: #545454; }}
                .no-results {{ color: #666; padding: 20px 0; }}
            </style>
        </head>
        <body>
            <h1>Search Engine</h1>
            <form class="search-form" action="/search" method="get">
                <input type="text" name="q" value="{query}" class="search-input">
                <button type="submit" class="search-button">Search</button>
            </form>
            <div class="results">
    '''
        
        for result in results:
            if result['url'] == '#':  # No results case
                result_html += f'''
                <div class="no-results">
                    <h2>{result['title']}</h2>
                    <p>{result['content']}</p>
                    <p>Try searching for terms like: platypus, unicorn, page, egg-laying</p>
                </div>
                '''
            else:  # Normal results
                result_html += f'''
                <div class="result">
                    <div class="result-title"><a href="{result['url']}">{result['title'] or result['url']}</a></div>
                    <div class="result-url">{result['url']}</div>
                    <div class="result-preview">{result['content']}</div>
                </div>
                '''
        
        result_html += '''
            </div>
        </body>
    </html>
    '''
        
        return result_html
    except Exception as e:
        print(f"Error during search: {str(e)}")
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    initialize_search_engine()
    app.run(debug=True) 