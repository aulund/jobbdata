import json

class DataManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"{self.data_file} not found. Initializing empty data.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {self.data_file}: {e}")
            return {}

    def save_data(self):
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.data, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def update_data(self, key, value):
        self.data[key] = value
        self.save_data()

# Example usage
# data_manager = DataManager('data.json')
# data_manager.update_data('key', 'value')
