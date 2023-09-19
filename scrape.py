from googleapiclient.discovery import build

api_key = 'AIzaSyCd5vTBY66sbDamoFC_ZcxfjKVG0bqQqOw'
youtube = build('youtube', 'v3', developerKey=api_key)


# pylint: disable=no-member
request = youtube.search().list(
    part='snippet',
    maxResults=25,
    type='video',
    q='shorts',  # Query
)

response = request.execute()
video_list = []
for item in response['items']:
    video_id = item['id']['videoId']
    video_name = item['snippet']['title']
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    
    video_list.append({
        'name': video_name,
        'url': video_url
    })

for video in video_list:
    print(f"Name: {video['name']}, URL: {video['url']}")
