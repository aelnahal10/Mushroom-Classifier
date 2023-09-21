from googleapiclient.discovery import build
from pytube import YouTube

# Setup for scraping
api_key = 'AIzaSyCd5vTBY66sbDamoFC_ZcxfjKVG0bqQqOw'  # Replace with your API key
youtube = build('youtube', 'v3', developerKey=api_key)

# pylint: disable=no-member
def fetch_video_links():
    request = youtube.search().list(
        part='snippet',
        maxResults=25,
        type='video',
        q='shorts AND (redpill|masculinity|goggins|stay hard)',
        order='viewCount',
        relevanceLanguage='en'
    )

    response = request.execute()

    video_list = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_name = item['snippet']['title']
        video_description = item['snippet']['description']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        
        video_list.append({
            'name': video_name,
            'description': video_description,
            'url': video_url
        })

    return video_list

def download_video(video_url, video_name):
    yt = YouTube(video_url)
    video_stream = yt.streams.get_highest_resolution()
    video_path = f"./{video_name}.mp4"  # Save with video name as filename
    print(f"Downloading {yt.title}...")
    video_stream.download(output_path=video_path)
    print(f"{yt.title} Download complete!")

def main():
    video_list = fetch_video_links()
    
    for video in video_list:
        print(f"Name: {video['name']}, Description: {video['description']}, URL: {video['url']}")
        download_video(video['url'], video['name'])

if __name__ == "__main__":
    main()
