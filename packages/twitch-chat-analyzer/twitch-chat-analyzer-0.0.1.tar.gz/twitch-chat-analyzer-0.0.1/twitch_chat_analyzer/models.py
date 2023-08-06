'''Dataclass models'''


class Comment:
  def __init__(self, comment_json):
    self.comment = comment_json
    self.commenter = comment_json['commenter']
    self.message = comment_json['message']

  @property
  def offset(self):
    return self.comment['content_offset_seconds']

  @property
  def name(self) -> str:
    return self.commenter['name']
  
  @property
  def display_name(self) -> str:
    return self.commenter['display_name']

  @property
  def body(self) -> str:
    return self.message['body']

  @property
  def text_body(self) -> str:
    return self._GetTextBody(self.message['fragments'])

  @property
  def bits(self) -> int:
    return self.message.get('bits_spent', 0)

  def IsSubscription(self) -> bool:
    msg_id = self.message.get('user_notice_params', {}).get('msg_id')
    return msg_id in ('sub', 'resub')

  def _GetTextBody(fragments):
    texts = []
    for fragment in fragments:
      if 'emoticon' not in fragment:
        texts.append(fragment['text'].strip())

    return ' '.join(texts)