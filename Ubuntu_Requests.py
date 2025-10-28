import requests
import os
from urllib.parse import urlparse
from hashlib import md5

def is_image(response):
    """Check if the response content type is an image."""
    content_type = response.headers.get("Content-Type", "").lower()
    return content_type.startswith("image/")

def file_already_downloaded(file_hash, hash_store):
    """Check if the file hash already exists (to prevent duplicates)."""
    return file_hash in hash_store

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web")
    print("----------------------------------------------------\n")

    # Allow multiple URLs
    urls = input("Enter one or more image URLs separated by commas:\n").split(",")

    # Directory to save images
    os.makedirs("Fetched_Images", exist_ok=True)

    # File to store downloaded file hashes
    hash_store_file = "Fetched_Images/hashes.txt"
    if os.path.exists(hash_store_file):
        with open(hash_store_file, "r") as f:
            hash_store = set(line.strip() for line in f)
    else:
        hash_store = set()

    for url in urls:
        url = url.strip()
        if not url:
            continue

        print(f"\nFetching from: {url}")
        try:
            # Security precaution: Only allow HTTP or HTTPS URLs
            if not (url.startswith("http://") or url.startswith("https://")):
                print("Skipped: Invalid or unsafe URL scheme.")
                continue

            # Fetch the image with a timeout
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Check for image type via headers
            if not is_image(response):
                print("Skipped: The content is not an image.")
                continue

            # Compute file hash to detect duplicates
            file_hash = md5(response.content).hexdigest()
            if file_already_downloaded(file_hash, hash_store):
                print("Skipped: Duplicate image already downloaded.")
                continue

            # Extract filename from URL or create one
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = f"image_{file_hash[:8]}.jpg"

            filepath = os.path.join("Fetched_Images", filename)

            # Save the image in binary mode
            with open(filepath, "wb") as f:
                f.write(response.content)

            # Add hash to store and save it
            hash_store.add(file_hash)
            with open(hash_store_file, "a") as f:
                f.write(file_hash + "\n")

            print(f"Successfully fetched and saved: {filename}")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection.")
        except requests.exceptions.Timeout:
            print("Request timed out. Try again later.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    print("\nConnection strengthened. Community enriched.")
    print("All downloads completed with respect and care.")

if __name__ == "__main__":
    main()



