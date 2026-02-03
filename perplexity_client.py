"""
Perplexity API client for searching people by name and location.
"""

import requests
import json
import os
from typing import Optional, Dict, Any


class PerplexityClient:
    """Client for interacting with Perplexity API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Perplexity API client.
        
        Args:
            api_key: Perplexity API key. If not provided, will try to read from
                     PERPLEXITY_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not provided. Set PERPLEXITY_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def search(
        self,
        name: str,
        location: Optional[str] = None,
        additional_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for a person using name and location.
        
        Args:
            name: Person's name to search for
            location: Optional location (city, state, country, etc.)
            additional_params: Additional parameters for the API request
            
        Returns:
            API response as dictionary
        """
        # Build search query
        query = "Professional profile which shows current designation and company name of" + name
        if location:
            query += f" working at  {location}"
        
        # Prepare request payload
        payload = {
            "model": "sonar",
            "messages": [
                {
                    "role": "user",
                    "content": f"Search for information about {query}"
                }
            ]
        }
        
        # Add additional parameters if provided
        if additional_params:
            payload.update(additional_params)
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to Perplexity API: {e}")
            raise
    
    def search_with_details(
        self,
        name: str,
        location: Optional[str] = None,
        return_citations: bool = True
    ) -> Dict[str, Any]:
        """
        Search for a person with additional context and citations.
        
        Args:
            name: Person's name to search for
            location: Optional location (city, state, country, etc.)
            return_citations: Whether to include citations in response
            
        Returns:
            API response with search results and citations
        """
        params = {}
        if return_citations:
            params["return_citations"] = True
        
        return self.search(name, location, params)
    
    def parse_response(self, response: Dict[str, Any]) -> str:
        """
        Parse the API response and extract the answer.
        
        Args:
            response: API response dictionary
            
        Returns:
            Extracted answer text
        """
        try:
            # Extract content from the response
            if "choices" in response and len(response["choices"]) > 0:
                choice = response["choices"][0]
                if "message" in choice:
                    return choice["message"].get("content", "")
            return ""
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error parsing response: {e}")
            return ""


def search_person(name: str, location: Optional[str] = None, api_key: Optional[str] = None) -> str:
    """
    Convenience function to search for a person.
    
    Args:
        name: Person's name
        location: Optional location
        api_key: Optional API key (defaults to PERPLEXITY_API_KEY env var)
        
    Returns:
        Search results as string
    """
    try:
        client = PerplexityClient(api_key)
        response = client.search(name, location)
        return client.parse_response(response)
    except Exception as e:
        print(f"Search failed: {e}")
        return ""


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python perplexity_client.py <name> [location]")
        print("\nExample: python perplexity_client.py 'John Doe' 'New York, USA'")
        sys.exit(1)
    
    name = sys.argv[1]
    location = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"Searching for: {name}", end="")
    if location:
        print(f" in {location}")
    else:
        print()
    print("-" * 50)
    
    result = search_person(name, location, api_key='YOUR_API_KEY_HERE')
    print(result)
