import requests


def oauth_reddit():

    base_url = 'https://www.reddit.com/'
    data = {'grant_type': 'password', 'username': '--username--', 'password': '--password--'}
    auth = requests.auth.HTTPBasicAuth('XVuCl7S_k2qMnw', 'Mi0fBsGdLJEk_VjhWDpaOkRchd4')
    r = requests.post(base_url + 'api/v1/access_token', data=data, headers={'user-agent': 'APP-NAME by REDDIT-USERNAME'}, auth=auth)
    d = r.json()
    token = 'bearer ' + d['access_token']
    url_oauth = 'https://oauth.reddit.com'

    headers = {
        'Authorization': token,
        'User-Agent': 'test'
    }

    return url_oauth, headers


def search_subreddit(url_oauth, headers, what_you_search, limit_number):

    url = f'{url_oauth}/search.json?q={what_you_search}&limit={limit_number}&sort=relevance'
    response = requests.get(url, headers=headers)

    return response.json()
