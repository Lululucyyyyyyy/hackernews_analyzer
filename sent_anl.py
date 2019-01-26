import requests
import os
import csv
import time

x = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
y = os.path.realpath('/Users/wenmo/Development/polyglot/cohort-1/data/goodwords.txt')
z = os.path.realpath('/Users/wenmo/Development/polyglot/cohort-1/data/badwords.txt')

tweets = set()
goodwords = set()
badwords = set()

#create sets for words
def wordlists(path, set):
    with open(path, "r") as g:
        line = g.readlines()[35:]
        for word in line:
            words = word.split(',')
            for i in words:
                temp = i
                temp = temp.strip(' ')
                temp = temp.strip('\n')
                set.add(temp)

def display(set):
    for word in set:
        print (word)

wordlists(y, goodwords)
wordlists(z, badwords)

story2 = []

class TweetAnalyzer:
    def __init__(self, goodwords_list, badwords_list, story2):
        self.goodwords = goodwords_list
        self.badwords = badwords_list
        self.story2 = story2
        self.comments = self.get_comments(x, story2)
        self.gnum = 0
        self.bnum = 0

    def get_comments(self, url, story2):
        new_response = requests.get(url)
        top_five_ids = new_response.json()[:100]

        comments = {}
        for top_id in top_five_ids:
            curr_story_api_url = (url)
            curr_story = requests.get(curr_story_api_url)
            story2.append(curr_story.json())
            
        for story in story2:
            comment_ids = story['kids']
            title = story['title']
            comments[title] = [] 
            for comment_id in comment_ids:
                curr_id = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(comment_id)
                curr_comment = requests.get(curr_id).json()['text']
                comments[title].append(curr_comment)
        return comments
    
    def analyze_all_comments(self):
        for comment in self.comments:
            for words in comment:
                words = comment.split(' ')
                for word in words:
                    if word in self.goodwords:
                        self.gnum += 1
                    if word in self.badwords:
                        self.bnum += 1
            comment_sentiment_pos = gnum / len(comment)
            comment_sentiment_neg = gnum / len(comment)
            print(comment +  "{0:.0%}".format(comment_sentiment_pos) + "{0:.0%}".format(comment_sentiment_neg))


    def input_tweet(self):
        wordnum = 0
        bnum = 0
        gnum = 0
        mytweet = input("the tweet is: ")
        for word in mytweet.split():
            if word in self.badwords:
                bnum += 1
            if word in self.goodwords:
                gnum += 1
            wordnum += 1
        tweet_sentiment = (gnum - bnum) / wordnum 

        return "{0:.0%}".format(tweet_sentiment)

if __name__ == "__main__":
    a1 = TweetAnalyzer(goodwords, badwords, story2)
    #print("Tweet Sentiment: " + str(a1.input_tweet()))
    a1.analyze_all_comments()





