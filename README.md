# Search Engine

A web-based search engine built with Python, Flask, and Whoosh that crawls and indexes web content.

## Features

- Web crawler that follows links within a domain
- Full-text search indexing using Whoosh
- Simple web interface for searching
- Preview of search results with titles and content snippets

## Installation

1. Clone the repository:   ```bash
   git clone https://github.com/Sigurius23/search-engine.git
   cd search-engine   ```

2. Create a virtual environment and install dependencies:   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt   ```

3. Run the application:   ```bash
   python app.py   ```

## Usage

1. The application will start crawling the test website automatically
2. Access the search interface at `http://localhost:5000`
3. Enter search terms and click "Search"

## Deployment

For deployment on university servers:
1. Connect via SSH (requires university VPN)
2. Place files in `~/public_html/search_engine/`
3. Access at `http://vmXXX.rz.uni-osnabrueck.de/uXXX/search_engine/search.wsgi`