import json
import pandas as pd
import requests

subreddit = 'DungeonsAndDragons'
limit = None
timeframe = 'month'  # hour, day, week, month, year, all
keyword = 'game pieces'   # Keyword to search for in the posts

def get_reddit(subreddit, keyword, limit, timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/search.json?q={keyword}&limit={limit}&t={timeframe}&restrict_sr=on'
        response = requests.get(base_url, headers={'User-agent': 'Fine_Ad1208'})
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'An Error Occurred: {e}')
        return None

def get_post_titles(r):
    '''
    Get a List of post titles
    '''
    posts = []
    if r is not None:
        for post in r['data']['children']:
            posts.append(post['data']['title'])
    return posts

def get_results(r):
    '''
    Create a DataFrame Showing Title, Score and Number of Comments.
    '''
    data = []
    if r is not None:
        for post in r['data']['children']:
            post_data = post['data']
            data.append({
                'title': post_data['title'],
                'score': post_data['score'],
                'url': post_data['url'],
                'comments': post_data['num_comments']
            })
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    r = get_reddit(subreddit, keyword, limit, timeframe)
    if r is not None:
        df = get_results(r)
        # Save DataFrame to CSV with only the title, score, and number of comments
        df.to_csv('reddit_posts.csv', index=False)
        print(f"Data saved to reddit_posts.csv")
    else:
        print("Failed to retrieve data")
