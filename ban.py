from datetime import datetime as dt, timedelta as td
from data import db_session


class Ban:
    def __init__(self):
        self.bans = {}
        self.warning = {}
        self.hour = 0.0
        self.minute = 0.0
        self.second = 0.0
        self.currently_banned = {}

    def ban_check(self, user_id):
        if str(user_id) in self.warning.keys() and self.warning[str(user_id)] >= 15:
            if str(user_id) not in self.bans:
                self.bans[str(user_id)] = 0
            self.warning[str(user_id)] = 0
            if self.bans[str(user_id)] == 0:
                jail_time = 0.5
            elif self.bans[str(user_id)] == 1:
                jail_time = 1
            elif self.bans[str(user_id)] == 2:
                jail_time = 5
            elif self.bans[str(user_id)] == 3:
                jail_time = 24
            elif self.bans[str(user_id)] == 4:
                jail_time = 24 * 3
            elif self.bans[str(user_id)] >= 5:
                jail_time = 24 * 7
            # banning process
            self.currently_banned[str(user_id)] = [dt.now(), str(user_id), dt.now() + td(hours=jail_time)]

    def checks(self, user_id):
        hour, minute, second = float((str(dt.now()).split()[1].split(':'))[0]),\
                               float((str(dt.now()).split()[1].split(':'))[1]),\
                               float((str(dt.now()).split()[1].split(':'))[2])
        if (abs(hour - self.hour) == 0) and (abs(minute - self.minute) == 0) and (abs(second - self.second) <= 1.3):
            self.hour = hour
            self.minute = minute
            self.second = second
            if str(user_id) in self.warning.keys():
                self.warning[str(user_id)] += 1
            else:
                self.warning[str(user_id)] = 1
        elif abs(second - self.second) > 2.5:
            self.hour = hour
            self.minute = minute
            self.second = second

