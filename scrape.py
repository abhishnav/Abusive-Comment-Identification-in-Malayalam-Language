import pandas as pd
from googleapiclient.discovery import build
from IPython.display import FileLink


# Set your API key and video ID
api_key = 'AIzaSyBBIdNaQ-er9G1EX46OeVj96KcNFHk0Zos'
video_id = '4Ek6jvKB8gs'

# Create a YouTube service object
youtube = build('youtube', 'v3', developerKey=api_key)

# Fetch comments from YouTube
comments = []
next_page_token = None

while True:
    # Fetch comments page by page (maxResults specifies the number of comments per page)
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        pageToken=next_page_token,
        maxResults=100  # Change as needed, maximum is 100
    ).execute()

    # Append comments to the list
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
        comments.append(comment)

    # Check if there's another page of comments
    if 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
    else:
        break

# Convert comments list to a DataFrame
df = pd.DataFrame({'Comments': comments})

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file
df.to_csv('youtube_comments1.csv', index=False)

# Save the DataFrame to a CSV file
df.to_csv('youtube_comments1.csv', index=False)

# Provide a download link
FileLink('youtube_comments1.csv')

