import datetime

from django.utils import timezone
from django.conf import settings


class MessageScheduled(object):

    TYPE_MESSAGES = ('CALL', 'SMS')
    GOALS = ('R', 'M')

    def __init__(self, type_message, goal, order, date=None, add_days=0):
        self.date = date
        self.type_message = type_message
        self.goal = goal
        self.order = order
        self.add_days = add_days

    def toogle_type_message(self):
        if self.type_message == self.TYPE_MESSAGES[0]:
            self.type_message = self.TYPE_MESSAGES[1]
        else:
            self.type_message = self.TYPE_MESSAGES[0]
        return self.type_message

    def next_order(self):
        if self.goal == self.GOALS[0]:  # R
            if self.order != 2:
                self.order = self.order + 1
            else:
                self.order = 1
        if self.goal == self.GOALS[1]:  # M
            if self.order != 6:
                self.order = self.order + 1
            else:
                self.order = 1
        return self.order

    def __repr__(self):
        return str({
            "date":  self.date,
            "type_message": self.type_message,
            "goal": self.goal,
            "order": self.order,
            "add_days":  self.add_days,
        })


class Schedule(object):

    def __init__(self, date=timezone.now()):
        self.date = date

    def schedule(self):
        for message in self.messages_controller(self.date):
            yield message

    def normalize_init_date(self, date=timezone.now()):
        LAUNCH_TIME = datetime.time(10, 0, 0, 0)
        if date.weekday() == 0:  # Monday.
            if date.time() < LAUNCH_TIME:
                return date.date()
        days_remaining = 7 - date.weekday()
        return datetime.timedelta(days=days_remaining) + date.date()

    def messages_controller(self, init_date, max_days=360):
        """
            Returns sequence of schedule messages starting on Monday, day 0.
        """
        date = self.normalize_init_date(init_date)
        message_reminder = MessageScheduled(
            type_message='SMS',
            goal='R',
            order=1,
            date=date,
            add_days=0,
        )
        yield message_reminder
        num = 1
        # Send messages the first 2 weeks: +1 +1 +1 +1 +3.
        # From Monday to Friday.
        for j in xrange(2):
            for i in xrange(4):
                message_reminder.next_order()
                if i == 2:
                    message_reminder.toogle_type_message()
                message_reminder.add_days = 1
                date += datetime.timedelta(days=1)
                message_reminder.date = date
                yield message_reminder
                num = num + 1
            message_reminder.next_order()
            message_reminder.add_days = 3
            date += datetime.timedelta(days=3)
            message_reminder.date = date
            yield message_reminder
            num = num + 3  # Monday.

        # Send messages the rest of the year: +3 +4.
        # Monday and Thursday.
        date += datetime.timedelta(days=3)
        message_motivational = MessageScheduled(
            type_message='CALL',
            goal='M',
            order=1,
            date=date,
            add_days=3,
        )
        yield message_motivational
        num = num + 3  # Thursday.

        while num <= max_days:
            # Reminder message send on Monday.
            message_reminder.next_order()
            if message_reminder.order % 2:
                message_reminder.toogle_type_message()
            message_reminder.add_days = 4
            date += datetime.timedelta(days=4)
            message_reminder.date = date
            yield message_reminder

            num = num + 4
            # Motivational message send on Thursday.
            message_motivational.next_order()
            if message_motivational.order % 2:
                message_motivational.toogle_type_message()
            message_motivational.add_days = 3
            date += datetime.timedelta(days=3)
            message_motivational.date = date
            yield message_motivational
            num = num + 3
