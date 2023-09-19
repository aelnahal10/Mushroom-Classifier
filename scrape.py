from googleapiclient.discovery import build

# Initialize the YouTube API client
api_key = 'Your_API_Key'
youtube = build('youtube', 'v3', developerKey=api_key)


# pylint: disable=no-member
request = youtube.search().list(
    part='snippet',
    maxResults=25,
    type='video',
    q='shorts',  # Query
)

response = request.execute()

# Create a list to store video URLs and names
video_list = []

# Loop through the search results and populate the list
for item in response['items']:
    video_id = item['id']['videoId']
    video_name = item['snippet']['title']
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    
    video_list.append({
        'name': video_name,
        'url': video_url
    })

# Print the list of video URLs and names
for video in video_list:
    print(f"Name: {video['name']}, URL: {video['url']}")
