"""Test DuckDuckGo search"""
from duckduckgo_search import DDGS

# Test various queries
queries = [
    'pompe funebre timisoara',
    'servicii funerare timisoara',
    'casa funerara timisoara',
    'inmormantari timisoara',
]

ddgs = DDGS()

for query in queries:
    print(f"\n=== Query: {query} ===")
    try:
        results = list(ddgs.text(query, max_results=15))
        print(f"Found {len(results)} results:")
        for r in results:
            url = r.get('href', '')
            title = r.get('title', '')[:50]
            if '.ro' in url or 'timis' in url.lower():
                print(f"  ✓ {url}")
            else:
                print(f"    {url}")
    except Exception as e:
        print(f"Error: {e}")
