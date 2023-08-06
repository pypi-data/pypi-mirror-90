import datetime


class PhaseTracker:
    def __init__(self, init_phase, initial_time=None, history_on=False):
        self.__initial_time = initial_time if initial_time else datetime.date.min
        self.__indices = {}
        self.__history = []
        self.__timespans = []
        self.__last_time = self.__initial_time
        self.__last_phase = init_phase
        self.__history_on = history_on
        self.__all_phase = []
        self.__last_phase_index = None
        if history_on:
            self.__history.append((self.__last_time, self.__last_phase_index))

    @property
    def last_time(self):
        return self.__last_time

    @property
    def all_phase(self):
        return self.__all_phase

    @property
    def last_phase(self):
        return self.__all_phase[self.__last_phase_index]

    @last_phase.setter
    def last_phase(self, value):
        self.__last_phase_index = self.__get_phase_index(value)
    
    @property
    def history(self):
        return self.__history
    
    @property
    def history_on(self):
        return self.__history_on

    @property
    def timespans(self):
        return self.__timespans

    def __get_phase_index(self, phase):
        if phase not in self.__indices.keys():
            self.__indices[phase] = len(self.__all_phase)
            self.__all_phase.append(phase)
            self.__timespans.append(datetime.timedelta())
        return self.__indices[phase]

    def update_phase(self, phase, clock_time):
        duration = clock_time - self.last_time
        self.__timespans[self.__last_phase_index] = duration
        if self.__history_on:
            self.__history.append((self.__last_time, self.__get_phase_index(phase)))
        self.__last_phase = phase
        self.__last_time = clock_time

    def warm_up(self, clock_time):
        self.__initial_time = clock_time
        self.__last_time = clock_time
        if self.__history_on:
            self.__history.append((self.__last_time, self.__last_phase_index))
        self.__timespans = [datetime.timedelta() for x in self.__timespans]
    
    def get_proportion(self, phase, clock_time):
        if phase not in self.__indices.keys():
            return 0
        timespan = self.__timespans[self.__indices[phase]].hours()
        if phase == self.last_phase:
            timespan += (clock_time - self.__last_time).hours()
        sum_time = (clock_time - self.__initial_time).hours()
        return timespan / sum_time
