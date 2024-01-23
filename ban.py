from datetime import datetime as dt


class Ban:
    def __init__(self):
        self.bans = 0
        self.currently_banned = False
        self.warning = 0
        self.hour = 0.0
        self.minute = 0.0
        self.second = 0.0

    def ban_check(self):
        if self.warning >= 12:
            print('time to ban')
            self.warning = 0
            self.currently_banned = True  # banning process

    def checks(self):
        print(1)
        hour, minute, second = float((str(dt.now()).split()[1].split(':'))[0]),\
                               float((str(dt.now()).split()[1].split(':'))[1]),\
                               float((str(dt.now()).split()[1].split(':'))[2])
        if (abs(hour - self.hour) == 0) and (abs(minute - self.minute) == 0) and (abs(second - self.second) <= 2.1):
            print('spammer spotted')
            self.hour = hour
            self.minute = minute
            self.second = second
            self.warning += 1
        else:
            self.hour = hour
            self.minute = minute
            self.second = second
