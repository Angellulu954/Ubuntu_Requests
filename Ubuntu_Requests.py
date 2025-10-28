import os
import requests
from urllib.parse import urlparse
from datetime import datetime

def fetch_image():
    # Ask user for the image URL
    url = input("Enter the image URL to fetch: ").strip()

    # Directory to store fetched images
    folder_name = "Fetched_Images"
    os.makedirs(folder_name, exist_ok=True)

    try:
        # Connect to the web and fetch the image
        print("Connecting to the web community...")
        response = requests.get(url, timeout=10)

        # Raise exception for HTTP errors
        response.raise_for_status()

        # Extract filename or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # If no filename, create one using timestamp
        if not filename:
            filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

        # Full path to save image
        file_path = os.path.join(folder_name, filename)

        # Save image in binary mode
        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"Image successfully fetched and saved as: {file_path}")

    except requests.exceptions.MissingSchema:
        print("Invalid URL. Please include 'http://' or 'https://'.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError:
        print("Connection Error. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("The request timed out. Try again later.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_image()


