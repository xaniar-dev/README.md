import requests

def download_file(url, save_path):
    print(f"Downloading: {url}")

    response = requests.get(url, stream=True)

    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    print("Download completed.")
