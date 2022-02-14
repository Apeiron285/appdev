from Base import *
from datetime import datetime


class Faq:
    count_id = 0

    def __init__(self, question, answer):
        Base.__init__(self, datetime.now())
        self.total = 0
        self.items = {}

        Faq.count_id += 1
        self.__question_id = Faq.count_id
        self.__question = question
        self.__answer = answer

    def get_question_id(self):
        return self.__question_id

    def get_question(self):
        return self.__question

    def get_answer(self):
        return self.__answer

    def set_question_id(self, question_id):
        self.__question_id = question_id

    def set_question(self, question):
        self.__question = question

    def set_answer(self, answer):
        self.__answer = answer
