import pandas as pd

class DataProcessor:
    def process_deals(self, raw_data):
        if not raw_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(raw_data)
        
        
        if 'salePrice' in df.columns:
            df['salePrice'] = pd.to_numeric(df['salePrice'])
        if 'normalPrice' in df.columns:
            df['normalPrice'] = pd.to_numeric(df['normalPrice'])

       
        if 'savings' in df.columns:
            df['savings'] = pd.to_numeric(df['savings']).round(2)
        elif 'salePrice' in df.columns and 'normalPrice' in df.columns:
         
            df['savings'] = ((1 - (df['salePrice'] / df['normalPrice'])) * 100).round(2)
        else:
            df['savings'] = 0.0
            
       
        for col in ['title', 'metacriticScore', 'dealID']:
            if col not in df.columns:
                df[col] = 'N/A'

       
        cols_to_keep = ['title', 'salePrice', 'normalPrice', 'savings', 'metacriticScore', 'dealID']
        df = df[cols_to_keep]
        
        df.columns = ['Game', 'Sale Price (USD)', 'Normal Price (USD)', 'Savings (%)', 'Metacritic Score', 'Link ID']
        
        df['Store URL'] = "https://www.cheapshark.com/redirect?dealID=" + df['Link ID'].astype(str)
        
        df = df.drop(columns=['Link ID'])
        
        return df