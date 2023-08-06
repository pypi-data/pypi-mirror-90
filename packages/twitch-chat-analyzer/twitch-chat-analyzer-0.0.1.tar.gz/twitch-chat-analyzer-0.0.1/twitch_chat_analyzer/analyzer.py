
import json
import collections
from matplotlib import pyplot as plt
import math
import os
import pandas as pd

from twitch_chat_analyzer import kraken
from twitch_chat_analyzer import downloader


COLUMNS = ['offset', 'username', 'display_name', 'body', 'bits', 'subscription']


def FromFile(filepath):
  with open(filepath, 'r', encoding='utf8') as f:
    try:
      data_json = json.load(f)
      return ChatAnalyzer(data_json['video'], data_json['comments'])
    except Exception as e:
      print('Cannot load the file', filepath, '. Reason:', e)


def FromVideoId(video_id):
  # First check if the chat log was already downloaded
  client = kraken.TwitchClient()
  username = client.GetUsernameFromVideo(video_id)
  path = 'chatlogs/{username}/{video_id}.json'.format(username=username, video_id=video_id)
  if os.path.exists(path):
    return FromFile(path)
  
  data_json = downloader.downloadChat(video_id)
  return ChatAnalyzer(data_json['video'], data_json['comments'])


class ChatAnalyzer:
  def __init__(self, video_json, comments_json):
    self.video = video_json

    comments = [Comment(comment_json) for comment_json in comments_json]
    self.original_comments = comments
    self.comments = comments

  def ChatPerMinute(self, minute: int = 5):
    chat_counts = self._CountChatsByMinutes(minute)
    x = [str(index * minute) for index in range(len(chat_counts))]

    plt.bar(x, chat_counts, color='pink')
    plt.show()

  def TopEmotes(self, top=10):
    emote_dict = self._CountEmotes()
    emote_list = list(emote_dict.items())
    print(emote_list)
    emote_list = sorted(emote_list, key=lambda item: (-item[1], item[0]))
    emote_list = emote_list[:top]

    names, counts = zip(*emote_list)
    print(names)
    print(counts)
    plt.xticks(rotation=45, ha='right')
    plt.bar(names, counts, color='#333333')
    plt.show()

  def ToDataFrame(self):
    comments = []
    for comment in self.comments:
      comments.append([
        comment.offset,
        comment.name,
        comment.display_name,
        comment.body,
        comment.bits,
        comment.IsSubscription()
      ])

    return pd.DataFrame(comments, columns=COLUMNS)

  def _CountChatsByMinutes(self, minute: int):
    total_seconds = minute * 60
    total_slots = int(math.ceil(self.video['length'] / total_seconds))
    counts = [0] * total_slots
    for comment in self.comments:
      index = int(comment.content_offset_seconds / total_seconds)
      counts[index] += 1

    return counts

  def _CountEmotes(self):
    emote_dict = collections.defaultdict(int)
    for comment in self.comments:
      fragments = comment.message['fragments']
      for fragment in fragments:
        if 'emoticon' in fragment:
          emote_dict[fragment['text']] += 1
    
    return emote_dict

def _GetTextBody(fragments):
  texts = []
  for fragment in fragments:
    if 'emoticon' not in fragment:
      texts.append(fragment['text'].strip())

  return ' '.join(texts)




