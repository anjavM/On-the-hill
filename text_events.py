import timers_and_counters
from random import randint

"""Module for text-based/CYOA events"""


class TextEventPrototype:
    def __init__(self):
        self.title = "Test event"
        self.description = "Something happens"
        self._actions = {'OK': lambda state: None}
        self.should_be_activated   = lambda state: True
        self.should_be_deactivated = lambda state: False

    def get_actions(self):
        ret = []
        for action in self._actions:
            ret.append(action)
        return ret

    def perform_action(self, action, state):
        return self._actions[action](state)


class BasicEvent(TextEventPrototype):
    def __init__(self, name, description, actions):
        super(BasicEvent, self).__init__()
        self.title = name
        self.description = description
        self.actions = actions


class UnlockableEvent(BasicEvent):
    def __init__(self, name, description, actions, unlock_predicate):
        super(UnlockableEvent, self).__init__(name, description, actions)
        self.should_be_activated = unlock_predicate


class ConditionalEvent(BasicEvent):
    def __init__(self, name, description, actions, condition):
        super(ConditionalEvent, self).__init__(name, description, actions)
        self.should_be_activated = condition
        self.should_be_deactivated = lambda state: not condition(state)

def get_basic_random_events():
    return [TextEventPrototype(), TextEventPrototype(), TextEventPrototype()]


# a bunch of horrible functions (should have been lambdas) that will be useful for data-driven object creation

#horrible mutators
def spawn_immediately(state, event):
    state._event_queue.append(event)


def add_active_event(state, event):
    state._event_active_deck.append(event)


def add_inactive_event(state, event):
    state._event_inacrive_deck.append(event)


def spawn_after_n_turns(state, event, n):
    state.timers.append(timers_and_counters.BasicEventTimer(n, event))


def spawn_next_season(state, event, season):  # winter = 0, spring = 1, summer = 2, autumn = 3
    current_month = (state.turn % 12) + 1
    if season == 0:
        season_start = 12
    else:
        season_start = season*3
    to_season_start = (season_start - current_month % 12) + 1
    # return (to_season_start + randint(0, 2)) % 12
    spawn_after_n_turns(state, event, (to_season_start + randint(0, 2)) % 12)


def modify_state(state, attributes):
    for attr in attributes:
        setattr(state, attr, getattr(state, attr) + attributes[attr])


#horrible predicates
def counter_equal(state, counter_key, value):
    return _counter_predicate(state, counter_key, value, lambda x, y: x == y)


def counter_greater(state, counter_key, value):
    return _counter_predicate(state, counter_key, value, lambda x, y: x > y)


def counter_lower(state, counter_key, value):
    return _counter_predicate(state, counter_key, value, lambda x, y: x < y)


def attr_equal(state, attr, value):
    return _attribute_predicate(state, attr, value, lambda x, y: x == y)


def attr_greater(state, attr, value):
    return _attribute_predicate(state, attr, value, lambda x, y: x > y)


def counter_lower(state, atr, value):
    return _attribute_predicate(state, attr, value, lambda x, y: x < y)


def _counter_predicate(state, counter_key, value, func):
    if func(state.counter.get_count(counter_key), value):
        return True
    return False


def _attribute_predicate(state, attr, value, func)
    if func(getattr(state, attr), value):
        return True
    return False
