import pytube
from googleapiclient.discovery import build
from pytube import YouTube
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY')

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



def sanitize_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename


def download_video(video_url, video_name):
    # Sanitize and add .mp4 extension to the video name
    video_name = sanitize_filename(video_name) + ".mp4"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_folder = os.path.join(script_dir, "downloaded_videos")
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    yt = YouTube(video_url)
    video_stream = yt.streams.get_highest_resolution()

    # Save the video to the defined folder
    video_stream.download(output_path=save_folder, filename=video_name)


def main():
    video_list = fetch_video_links()  # Assuming you've already defined this function

    for video in video_list:
        print(f"Name: {video['name']}, URL: {video['url']}")
        try:
            download_video(video['url'], video['name'])
            print(f"Downloaded: {video['name']}")
        except pytube.exceptions.AgeRestrictedError:
            print(f"Skipped {video['name']} due to age restriction.")
        except Exception as e:
            print(f"Error downloading {video['name']}: {e}")


if __name__ == "__main__":
    main()
