"""
Example script demonstrating usage of the Perplexity API client.
"""

from perplexity_client import PerplexityClient, search_person


def example_basic_search():
    """Basic search example."""
    print("=== Basic Search Example ===\n")
    
    # Initialize client
    client = PerplexityClient()
    
    # Search for a person
    name = "John Smith"
    location = "San Francisco, CA"
    
    print(f"Searching for: {name} in {location}")
    response = client.search(name, location)
    
    # Parse and print results
    result = client.parse_response(response)
    print(f"Results:\n{result}\n")


def example_multiple_searches():
    """Example with multiple searches."""
    print("=== Multiple Searches Example ===\n")
    
    searches = [
        {"name": "Jane Doe", "location": "New York, NY"},
        {"name": "Michael Johnson", "location": "Austin, TX"},
        {"name": "Sarah Williams", "location": None},  # Search without location
    ]
    
    for search in searches:
        name = search["name"]
        location = search["location"]
        
        print(f"Searching for: {name}", end="")
        if location:
            print(f" in {location}")
        else:
            print(" (no location specified)")
        
        result = search_person(name, location)
        if result:
            print(f"Found: {result[:200]}...\n")
        else:
            print("No results found\n")


def example_with_citations():
    """Example with citations."""
    print("=== Search with Citations Example ===\n")
    
    client = PerplexityClient()
    
    name = "Alice Brown"
    location = "Boston, MA"
    
    response = client.search_with_details(name, location, return_citations=True)
    result = client.parse_response(response)
    
    print(f"Results for {name} in {location}:")
    print(result)
    
    # Check for citations in response
    if "citations" in response:
        print("\nCitations:")
        for citation in response["citations"]:
            print(f"- {citation}")


if __name__ == "__main__":
    print("Perplexity API Client Examples\n")
    print("Before running these examples, make sure to set the PERPLEXITY_API_KEY environment variable.\n")
    
    try:
        # Uncomment the example you want to run:
        example_basic_search()
        # example_multiple_searches()
        # example_with_citations()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set your Perplexity API key:")
        print("export PERPLEXITY_API_KEY='your-api-key-here'")
