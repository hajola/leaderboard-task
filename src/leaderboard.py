from collections import Counter
from datetime import datetime, timedelta
from typing import List
from event import Event
from config import Config

#  Only users with at least 15 events in the last 30 days are considered for the leaderboard
leaderboard_fallback_values = {
    'min_number_of_events': 15, 'number_of_days_to_count': 30}


def filter_expired_events(engagement_events: List[Event]) -> List[Event]:
    """
    Removes events that are older than N(default: 30) days.

    Args:
        engagement_events: A list of user events
    Returns:
        Returns a list of user events, with the expired(older than N days) removed.
    """

    number_of_days_to_count = Config.config().getint('DEFAULT',
                                                     'number_of_days_to_count', fallback=leaderboard_fallback_values)
    # First go over the list and filter out events that are older than 30 days
    expiration_date = datetime.now() - timedelta(days=number_of_days_to_count)
    def expiration_date_validator(x): return x.event_date > expiration_date
    valid_engagement_events = list(filter(
        expiration_date_validator, engagement_events))
    return valid_engagement_events


def filter_inactive_users(engagement_events: List[Event]) -> List[Event]:
    """
    Removes events that belong to users, who have engaged less than N amount of times.

    Args:
        engagement_events: A list of user events
    Returns:
        Returns a list of user events, with the event's of inactive users removed
    """

    min_number_of_events = Config.config().getint('DEFAULT',
                                                  'min_number_of_events', fallback=leaderboard_fallback_values)
    user_activity = Counter(
        event.user_id for event in engagement_events)  # user_activity is map of user_id: number_of_actions

    def activity_validator(x): return x[1] >= min_number_of_events
    active_users = dict(filter(activity_validator, user_activity.items()))

    def active_user_validator(x): return x.user_id in active_users
    active_engagement_events = list(
        filter(active_user_validator, engagement_events))
    return active_engagement_events


def get_users_by_words_learnt(engagement_events: List[Event]) -> dict:
    """
    Aggregates the list of events by user_id and 'words_learnt'.

    Args:
        engagement_events: A list of user events
    Returns:
        Returns a dictionary mapping user_ids to the amount of words learnt. For Example:

        {
            1: 23,
            2: 45,
            3: 67
        }

    """
    users = {}  # will show user_id:number_of_words_learnt
    for event in engagement_events:
        if(event.user_id not in users):
            users[event.user_id] = 0

        if(event.action_name == "word_learnt"):
            users[event.user_id] = users[event.user_id] + 1

    return users


def get_30_day_leaderboard_user_ids(engagement_events: List[Event]) -> List[int]:
    """
    Build a leaderboard that ranks users from fastest learning to slowest learning based on how many
    "words_learnt" events they achieved during the previous 30 days.
    Only users with at least 15 actions taken in the last 30 days are considered for the leaderboard.

    Args:
        engagement_events: A list of user events
    Returns:
        A list of user ids, ordered from most words learnt to least words learnt
    """
    unexpired_engagement_events = filter_expired_events(engagement_events)
    active_users_events = filter_inactive_users(
        unexpired_engagement_events)
    words_learnt_by_user = get_users_by_words_learnt(active_users_events)
    leaderboard = {user: number_of_words_learnt for user, number_of_words_learnt in sorted(
        words_learnt_by_user.items(), key=lambda item: item[1], reverse=True)}
    return [*leaderboard]
