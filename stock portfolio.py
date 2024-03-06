import requests
import json

class StockPortfolio:
    def __init__(self, api_key):
        self.portfolio = {}
        self.api_key = api_key

    def add_stock(self, symbol, quantity):
        if symbol in self.portfolio:
            self.portfolio[symbol]['quantity'] += quantity
        else:
            self.portfolio[symbol] = {'quantity': quantity}

    def remove_stock(self, symbol, quantity):
        if symbol in self.portfolio:
            if self.portfolio[symbol]['quantity'] >= quantity:
                self.portfolio[symbol]['quantity'] -= quantity
            else:
                print("Error: Not enough stocks to sell.")
        else:
            print("Error: Stock not found in portfolio.")

    def update_portfolio(self):
        for symbol in self.portfolio:
            data = self.get_stock_data(symbol)
            if data:
                try:
                    current_price = float(data['Global Quote']['05. price'])
                    current_value = current_price * self.portfolio[symbol]['quantity']
                    self.portfolio[symbol]['current_price'] = current_price
                    self.portfolio[symbol]['current_value'] = current_value
                except KeyError:
                    print(f"Error: Unable to get price for {symbol}. Check if the symbol is valid.")

    def get_stock_data(self, symbol):
        base_url = 'https://www.alphavantage.co/query'
        function = 'GLOBAL_QUOTE'
        params = {'function': function, 'symbol': symbol, 'apikey': self.api_key}

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if 'Global Quote' in data:
                return data
            elif 'Note' in data:
                print(f"API Limit Exceeded. Please try again later.")
                return None
            else:
                print(f"Error: Unable to get data for {symbol}.")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def display_portfolio(self):
        print("\nStock Portfolio:")
        for symbol, details in self.portfolio.items():
            print(f"\nSymbol: {symbol}")
            print(f"Quantity: {details['quantity']}")
            if 'current_price' in details:
                print(f"Current Price: {details['current_price']:.2f}")
                print(f"Current Value: {details['current_value']:.2f}")
        print("\n")


if __name__ == "__main__":
    api_key = '3UKIQ1S9BKVL3O95'
    portfolio = StockPortfolio(api_key)

    while True:
        print("\n1. Add Stock\n2. Remove Stock\n3. Display Portfolio\n4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            quantity = int(input("Enter quantity: "))
            portfolio.add_stock(symbol, quantity)

        elif choice == '2':
            symbol = input("Enter stock symbol to sell: ").upper()
            quantity = int(input("Enter quantity to sell: "))
            portfolio.remove_stock(symbol, quantity)

        elif choice == '3':
            portfolio.update_portfolio()
            portfolio.display_portfolio()

        elif choice == '4':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")