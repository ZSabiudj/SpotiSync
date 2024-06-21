import requests
import os

def download_and_save_mp3(id, filename="audio.mp3", path=".", skip=False):
    """Downloads the audio from the given ID and saves it as an MP3 file to the specified path.

    Args:
        id (str): The Spotify ID of the track.
        filename (str, optional): The desired filename for the saved MP3. Defaults to "audio.mp3".
        path (str, optional): The path where the file should be saved. Defaults to the current directory (".).
        skip (bool, optional): Whether to raise an error if any occur or not. Defaults to False.
    """

    url = f"https://yank.g3v.co.uk/track/{id}"
    hasfailed=False

    # Create the path if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)
    
    # Create the full path including filename and check if it already exists
    full_path = os.path.join(path, filename)
    if os.path.exists(full_path):
        if skip==False:
            raise ValueError(f"File already exists: {full_path}")
        else:
            print(f"File already exists: {full_path}")
            hasfailed=True
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for non-200 status codes
    except requests.exceptions.RequestException as e:
        if skip==True:
            print(f"Error downloading audio: {e}")
            hasfailed=True
            
        else:    
            raise ValueError(f"Error downloading audio: {e}")

    # Check content type before saving
    if response.headers.get('content-type', '').lower() != 'audio/mpeg':
        if skip==True:
            print("Downloaded content is not an MP3 file.")
            hasfailed=True
        else:
            raise ValueError("Downloaded content is not an MP3 file.")

    
    if not os.path.exists(full_path):
        with open(full_path, "wb") as f:
            for chunk in response.iter_content(1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        print(f"Audio downloaded and saved as: {filename}")
    else:
        if skip==False:
            raise ValueError(f"File already exists: {full_path}")
        else:
            print(f"File already exists: {full_path}")
            hasfailed=True
        
    return hasfailed

if __name__ == "__main__":
    
    id = input("Enter the Spotify ID: ")
    
    download_path = input("Enter the download path (optional, defaults to current directory): ") or "."

    download_and_save_mp3(id, filename="audio.mp3", path=download_path)
