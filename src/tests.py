from datetime import datetime, timedelta
import unittest
from random import randrange

from leaderboard import get_30_day_leaderboard_user_ids, get_users_by_words_learnt, filter_inactive_users, filter_expired_events
from event import Event


def make_event(event_date: datetime = None, action_name: str = None, user_id: int = None):
    """
    Creates an event with provided attributes, if attributes are not provided, random ones are generated.

    Args:
        event_date (optional): Event completion time
        action_name (optional): One of the following: "incorrect_answer", "correct_answer", "word_learnt"
        user_id (optional):
    Returns:
       An event object.
    """
    # Creates an event with provided details, if details are not provided, random ones are generated.
    if event_date is None:
        event_date = datetime.now()-timedelta(days=randrange(0, 60, 1))
    if action_name is None:
        action_names = ["incorrect_answer",
                        "correct_answer", "word_learnt"]
        action_name = action_names[randrange(0, 2)]
    return Event(user_id if user_id else randrange(0, 1000, 1), event_date, action_name)


def make_multiple_events(event_date: datetime = None, action_name: str = None, user_id: int = None, amount: int = 1):
    """
    Products a list of desirable events. If attributes details aren't given, random ones are generated.
    Unless any attributes are given, the attributes are likely to vary in the returned Events.

    Args:
        event_date (optional): Event completion time
        action_name (optional): One of the following: "incorrect_answer", "correct_answer", "word_learnt"
        user_id (optional):
        amount (optional): The number of event objects to return.
    Returns:
       A list of event objects.
    """
    events = []
    for _ in range(amount):
        events.append(make_event(event_date=event_date,
                                 action_name=action_name, user_id=user_id))
    return events


class EventTests(unittest.TestCase):

    def test_make_event(self):
        self.assertIsInstance(make_event(), Event)

    def test_make_multiple_events(self):
        self.assertTrue(len(make_multiple_events(amount=10)), 10)

    def test_make_multiple_events_instance(self):
        self.assertIsInstance(make_multiple_events(amount=10)[0], Event)


class LeaderboardTests(unittest.TestCase):

    def test_filter_expired_events(self):
        expired = datetime.now() - timedelta(days=30)
        fresh = datetime.now()
        events = [make_event(fresh),  make_event(fresh),  make_event(expired),
                  make_event(expired)]
        self.assertEqual(len(filter_expired_events(events)), 2)

    def test_filter_expired_events_no_unexpired_events(self):
        expired = datetime.now() - timedelta(days=30)
        events = [make_event(expired),  make_event(expired),  make_event(expired),
                  make_event(expired)]
        self.assertEqual(len(filter_expired_events(events)), 0)

    def test_filter_expired_events_no_expired_events(self):
        fresh = datetime.now()
        events = [make_event(fresh),  make_event(fresh),  make_event(fresh),
                  make_event(fresh)]
        self.assertEqual(len(filter_expired_events(events)), 4)

    def test_filter_inactive_users(self):
        events = []
        events += (make_multiple_events(user_id=30, amount=30))
        events += (make_multiple_events(user_id=20, amount=20))
        events += (make_multiple_events(user_id=10, amount=10))
        self.assertEqual(len(filter_inactive_users(events)), 50)

    def test_filter_inactive_users_no_active_users(self):
        events = []
        events += (make_multiple_events(user_id=10, amount=10))
        self.assertEqual(len(filter_inactive_users(events)), 0)

    def test_get_users_by_words_learnt(self):
        events = []
        events += (make_multiple_events(user_id=10,
                                        amount=90, action_name="word_learnt"))
        events += (make_multiple_events(user_id=10,
                                        amount=20, action_name="incorrect_answer"))
        events += (make_multiple_events(user_id=10,
                                        amount=20, action_name="correct_answer"))

        events += (make_multiple_events(user_id=20,
                                        amount=90, action_name="word_learnt"))
        events += (make_multiple_events(user_id=20,
                                        amount=20, action_name="incorrect_answer"))
        events += (make_multiple_events(user_id=20,
                                        amount=20, action_name="correct_answer"))
        self.assertEqual(get_users_by_words_learnt(events)[10], 90)

    def test_get_30_day_leaderboard_user_ids(self):
        events = []
        events += (make_multiple_events(amount=10000))

        self.assertIsNotNone(len(get_30_day_leaderboard_user_ids(events)))

    def test_get_30_day_leaderboard_user_ids_no_events(self):
        events = []
        events += (make_multiple_events(amount=0))

        self.assertListEqual(get_30_day_leaderboard_user_ids(events), [])

    def test_get_30_day_leaderboard_user_ids_test_for_ranking(self):
        fresh = datetime.now()
        events = []
        events += (make_multiple_events(event_date=fresh,
                                        user_id=1, amount=100, action_name="word_learnt"))
        events += (make_multiple_events(event_date=fresh, user_id=1,
                                        amount=100, action_name="correct_answer"))
        events += (make_multiple_events(event_date=fresh, user_id=2,
                                        amount=999, action_name="correct_answer"))
        events += (make_multiple_events(event_date=fresh, user_id=3,
                                        amount=50, action_name="word_learnt"))

        self.assertListEqual(
            get_30_day_leaderboard_user_ids(events), [1, 3, 2])


if __name__ == '__main__':
    unittest.main()
