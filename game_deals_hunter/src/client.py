import requests

class CheapSharkClient:
    """
    Client to interact with the CheapShark API.
    """
    def __init__(self):
        self.base_url = "https://www.cheapshark.com/api/1.0/"
        
    def get_deals(self, store_id=1, upper_price=50, metacritic=80, page_size=60):
        """
        Fetches game deals based on filters.
        
        Args:
            store_id (int): ID of the store (1 = Steam).
            upper_price (int): Maximum price in USD.
            metacritic (int): Minimum Metacritic score.
            page_size (int): Number of results to return.
            
        Returns:
            list: A list of dictionaries containing deal data.
        """
        endpoint = f"{self.base_url}/deals"
        
        params = {
            "storeID": store_id,
            "upperPrice": upper_price,
            "metacritic": metacritic,
            "pageSize": page_size,
            "sortBy": "metacritic",
            "onSale": 1  
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error on Conecting to API: {e}")
            return []