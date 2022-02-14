from Base import *
from datetime import datetime


class Feedback:
    count_id = 0

    def __init__(self, name, subject, content):
        Base.__init__(self, datetime.now())
        self.total = 0
        self.items = {}

        Feedback.count_id += 1
        self.__feedback_id = Feedback.count_id
        self.__name = name
        self.__subject = subject
        self.__content = content

    def get_feedback_id(self):
        return self.__feedback_id

    def get_name(self):
        return self.__name

    def get_subject(self):
        return self.__subject

    def get_content(self):
        return self.__content

    def set_feedback_id(self):
        return self.__feedback_id

    def set_name(self, name):
        self.__name = name

    def set_subject(self, subject):
        self.__subject = subject

    def set_content(self, content):
        self.__content = content
