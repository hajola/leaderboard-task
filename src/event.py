"""
Event object 
"""

from datetime import datetime, timedelta
from typing import List


class Event(object):

    user_id: int = None   # a number that uniquely identifies a user in our system
    event_date: datetime = None  # the exact date and time that an event was completed at

    # one of the following: "incorrect_answer", "correct_answer", "word_learnt"
    action_name: str = None

    def __init__(self, user_id, event_date,
                 action_name):
        self.user_id = user_id
        self.event_date = event_date
        self.action_name = action_name

    def __repr__(self):
        return "Event ([{0},{1},{2}])".format(self.user_id, self.event_date, self.action_name)
