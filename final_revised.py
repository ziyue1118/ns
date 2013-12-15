import twitter
import json, ast
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

CONSUMER_KEY = 'FSJDlwyXo3x6cJPFtJ9kA'
CONSUMER_SECRET = 'Y5q51yS8B1iW3E69hU27DHrJ2DqavImjydfzXJ3io'
OAUTH_TOKEN = '700037561-YoppY08nkP8uBdxL9yjNBOlqqNnyD0NFvxRZXBkC'
OAUTH_TOKEN_SECRET = 'JIsVwEgnwmbQ2SJTbfObWnnsB20Q0OmIFOY2zYXj3x8wc'
# CONSUMER_KEY = '9WQ8uPw0E6XjnN5Fpe4wQ'
# CONSUMER_SECRET = 'eqRTSHzkDUe78lKLShsX7YvaecUaonr5xkglyFxEhEc'
# OAUTH_TOKEN = '931200800-vVarLuafor9AAyrQ7Q3RHS0QOJux5WUw67QLLgyk'
# OAUTH_TOKEN_SECRET = 'KSKyxgV6ucWqUvwmuVDYfJbZlenA83AYnVWlx1kBxONSn'


auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

#Collect search results
user_id = '813286'
screen_name = 'BarackObama'
count = 200
index = 0
retweet_id_array = []
search_results = twitter_api.statuses.user_timeline(user_id = user_id, screen_name = screen_name, count = count)
for tweet in search_results:
	while index < count:
		retweet_count = search_results[index]['retweet_count']
		if(retweet_count > 3000):
			retweet_id = search_results[index]['id']
			retweet_id_array.append(retweet_id)
		index += 1

#person information
person = []
person_info = []
for i in range(len(retweet_id_array)):
	get_person = twitter_api.statuses.show.id(id = retweet_id_array[i])
	needed_person_info = {}
	needed_person_info['name'] = get_person['user']['name'];
	needed_person_info['tweet_id'] = get_person['id']
	needed_person_info['create_time'] = get_person['created_at']
	needed_person_info['text'] = get_person['text']
	needed_person_info['profile_pic'] = get_person['user']['profile_image_url']
	needed_person_info['screen_name'] = get_person['user']['screen_name']
	needed_person_info['location'] = get_person['user']['location']
	person.append(needed_person_info)
person_info.append({"BarackObama" : person})

print json.dumps(person_info, indent = 1)
#print ast.literal_eval(json.dumps(person_info))


#get retweeter info
total = []
total_info = {}
#get retweeter_id, location, screen_name, profile_picture
for i in range(len(retweet_id_array)):
	get_retweet = twitter_api.statuses.retweets.id(id = retweet_id_array[i], count = 100)
	for index_retweeter in range(len(get_retweet)):
		needed_tweets_info = {}
		if(get_retweet[index_retweeter]['user']['location'] == ''): continue
		needed_tweets_info['tweet_id'] = get_retweet[index_retweeter]['id']
		needed_tweets_info['create_time'] = get_retweet[index_retweeter]['created_at']
		needed_tweets_info['retweeter_id'] = get_retweet[index_retweeter]['user']['id']
		needed_tweets_info['text'] = get_retweet[index_retweeter]['user']['description']
		needed_tweets_info['profile_pic'] = get_retweet[index_retweeter]['user']['profile_image_url']
		needed_tweets_info['name'] = get_retweet[index_retweeter]['user']['name']
		needed_tweets_info['screen_name'] = get_retweet[index_retweeter]['user']['screen_name']
		needed_tweets_info['location'] = get_retweet[index_retweeter]['user']['location']
		total.append(needed_tweets_info)
	total_info[retweet_id_array[i]] = total
	total = []
# print ast.literal_eval(json.dumps(total_info))
print json.dumps(total_info, indent = 1)