import enum
import pickle

from config import data_path, bot_token, admin_id
import time

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, \
    InlineKeyboardMarkup


class CourseType(enum.Enum):
    GENERAL = 'GENERAL'
    BASE = 'BASE'
    MAIN = 'MAIN'
    OPTIONAL = 'OPTIONAL'


class Course:
    def __init__(self, name, unit=3, course_type=CourseType.MAIN):
        self.name = name
        self.id = len(data)
        self.pres = []  # prerequisites
        self.unit = unit
        self.type = course_type

    def add_pre(self, course_id: int):
        self.pres.append(course_id)

    def __eq__(self, string: str):
        return self.name == string

    def __str__(self):
        return self.name


def save_data():
    with open(data_path, 'wb') as file:
        pickle.dump(data, file)


def load_data():
    try:
        file = open(data_path, 'rb')
        data = pickle.load(file)
        file.close()
    except FileNotFoundError:
        data = []

    return data


def new_course(name: str, unit: int = 3, course_type=CourseType.MAIN):
    name = name.replace('ي', 'ی').replace('ك', 'ک')
    data.append(Course(name, unit, course_type))
    save_data()


def get_pres_str(course_id: int):
    result = data[course_id].name + '\n*****'
    for pre_id in data[course_id].pres:
        result += '\n' + data[pre_id].name

    return result


def get_all_pres(course_id: int, result=None):
    if result is None:
        result = []
    for pre_id in data[course_id].pres:
        result.append(pre_id)
        result = get_all_pres(pre_id, result)

    return result


def get_all_pres_str(course_id: int):
    result = data[course_id].name + '\n*****'
    pres = list(set(get_all_pres(course_id)))
    pres.sort()
    for pre_id in pres:
        result += '\n' + data[pre_id].name

    return result


def search_course(name: str):
    result = []
    for i in range(len(data)):
        if name in data[i].name:
            result.append((i, data[i].name))

    return result[:10]


def on_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'] == '/start':
            if admin_id:
                bot.sendMessage(admin_id, 'START [%s](tg://user?id=%d)' % (msg['from']['first_name'], chat_id),
                                'Markdown')


def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    if not query_string:
        return

    if admin_id:
        bot.sendMessage(admin_id, '[%s](tg://user?id=%d)' % (msg['from']['first_name'], from_id), 'Markdown')

    query_string = query_string.replace('ي', 'ی').replace('ك', 'ک')
    articles = [InlineQueryResultArticle(
        id=str(res[0]),
        title=res[1],
        input_message_content=InputTextMessageContent(
            message_text=get_pres_str(res[0])
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='نمایش تمام دروس پیش‌نیاز',
                                                                                 callback_data=str(res[0]))]])
    ) for res in search_course(query_string)]

    if not articles:
        articles = [InlineQueryResultArticle(
            id=str(time.time()),
            title='موردی پیدا نشد!',
            input_message_content=InputTextMessageContent(
                message_text='موردی پیدا نشد!'
            )
        )]

    bot.answerInlineQuery(query_id, articles)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    bot.editMessageText(msg['inline_message_id'], get_all_pres_str(int(query_data)))


bot = telepot.Bot(bot_token)
MessageLoop(bot, {'chat': on_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query}).run_as_thread()

if __name__ == '__main__':
    data = load_data()
    while True:
        time.sleep(30)
