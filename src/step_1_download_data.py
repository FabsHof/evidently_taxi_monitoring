import requests
from tqdm import tqdm
from os import path
import os
from src.utils.logging import log_info, log_error
from dotenv import load_dotenv

load_dotenv()

def download_file(url: str, save_dir: str):
    '''
    Downloads a file from the given URL and saves it to the specified dir.
    Args:
        url (str): The URL of the file to download.
        save_dir (str): The directory where the file will be saved.
    Returns:
        None
    Throws:
        HTTPError: If the HTTP request returned an unsuccessful status code.
    '''
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # make sure the directory exists
    os.makedirs(save_dir, exist_ok=True)
    file_path = path.join(save_dir, path.basename(url))

    with open(file_path, 'wb') as file:
        for chunk in tqdm(response.iter_content(chunk_size=1024),
                          desc=f'Downloading {url}',
                          unit='B',
                          unit_scale=True,
                          unit_divisor=1024,
                          total=int(response.headers.get('content-length', 0))):
            file.write(chunk)

def download_files(urls: list[str], save_dir: str):
    '''
    Downloads multiple files from the given list of URLs.
    Args:
        urls (list[str]): The list of URLs of the files to download.
        save_dir (str): The directory where the files will be saved.
    Returns:
        None
    '''
    for url in urls:
        try:
            download_file(url, save_dir)
            log_info(f'Successfully downloaded {url} to {save_dir}')
        except Exception as e:
            log_error(f'Error downloading {url}: {e}')

if __name__ == '__main__':
    files_to_download = [url.strip() for url in os.getenv('DATASET_URLS', '').split(',')]
    raw_data_dir = os.getenv('RAW_DATA_DIR', 'data/raw')
    print(files_to_download)
    if files_to_download:
        download_files(files_to_download, raw_data_dir)
