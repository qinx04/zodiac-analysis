import json
import turtle
import math
import requests
from bs4 import BeautifulSoup


def init_screen(s, w, h, c, d):
    tmp = 20
    s.setup(w+tmp, h+tmp, tmp, tmp)
    s.setworldcoordinates(-w/2+tmp/4, -h/2-tmp/4, w/2+tmp/4, h/2-tmp/4)
    s.title('zodiac')
    s.colormode(255)
    s.bgcolor(c)
    s.delay(d)


def calc_rotation(rot, radius):
    x = radius * math.cos(rot * math.pi / 180)
    y = radius * math.sin(rot * math.pi / 180)

    return x, y


def zodiac_sign(day, month):
    if month == 12:
        astro_sign = 'Sagittarius' if (day < 21) else 'Capricorn'

    elif month == 1:
        astro_sign = 'Capricorn' if (day < 20) else 'Aquarius'

    elif month == 2:
        astro_sign = 'Aquarius' if (day < 19) else 'Pisces'

    elif month == 3:
        astro_sign = 'Pisces' if (day < 20) else 'Aries'

    elif month == 4:
        astro_sign = 'Aries' if (day < 20) else 'Taurus'

    elif month == 5:
        astro_sign = 'Taurus' if (day < 21) else 'Gemini'

    elif month == 6:
        astro_sign = 'Gemini' if (day < 21) else 'Cancer'

    elif month == 7:
        astro_sign = 'Cancer' if (day < 23) else 'Leo'

    elif month == 8:
        astro_sign = 'Leo' if (day < 23) else 'Virgo'

    elif month == 9:
        astro_sign = 'Virgo' if (day < 23) else 'Libra'

    elif month == 10:
        astro_sign = 'Libra' if (day < 23) else 'Scorpio'

    elif month == 11:
        astro_sign = 'Scorpio' if (day < 22) else 'Sagittarius'

    else:
        print('invalid month/day')
        return False

    return astro_sign

# problematic to debug
def break_str_line_by_char(string, limit):
    list_string = []
    i = 0

    while i < len(string):
        # reset segment
        seg = limit

        while i+seg < len(string) and string[i+seg] != ' ':
            seg += 1

        list_string.append(string[i:i+seg+1])
        # move the header
        # previous string stops at i+seg-1
        i = i + seg + 1

    return '\n'.join(list_string)


def break_str_line_by_words(string, n):
    list_string = string.split()
    tmp = []

    for i in range(0,len(list_string)):
        if i >= n and i % n == 0:
            tmp.append('\n')
        tmp.append(list_string[i])

    return ' '.join(tmp)


def query_web(sign):
    url = f'https://www.astrology.com/horoscope/daily/{sign.lower()}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    f = soup.find('span', {'style': 'font-weight: 400'})
    f_string = str(f.string)

    return break_str_line_by_char(f_string, 30)


def user_play(a, b, di):
    try:
        user_month = int(input('your bday month?'))
        user_day = int(input('your bday day?'))
    except ValueError:
        exit()

    user_sign = zodiac_sign(user_day, user_month)

    if not user_sign:
        exit()

    dict_sign = di[user_sign]

    rotation = int(dict_sign['longitude_end'])
    gloss = dict_sign['gloss']
    symbol = dict_sign['unicode_symbol']
    element = dict_sign['element']
    start = dict_sign['approximate_start_date']
    end = dict_sign['approximate_end_date']
    keywords = ', '.join(dict_sign['keywords'])

    web_description = query_web(user_sign)

    x, y = calc_rotation(rotation, 150)
    a.goto(x, y)

    m = x - 10 if x > 0 else x + 10
    n = y + 10
    b.clear()

    b.goto(m, n)
    b.color('white')
    b.write(
        f'{user_sign}\n\n{rotation} degree\n{gloss}\n{symbol}\n{element}\n'
        f'{start} - {end}\n{keywords}',
        font=('Comic Sans MS', 11, 'normal')
        )

    b.goto(-290, -290)
    b.color('blue')
    b.write(web_description, font=('Comic Sans MS', 11, 'normal'))

    #turtle.mainloop()
    #turtle.exitonclick()

    return None


class QT(turtle.Turtle):
    def __init__(self,name,color,pensize,shape,visible):
        turtle.Turtle.__init__(self, visible=visible)
        self.name = name
        self.color(color)
        self.pensize(pensize)
        self.shape(shape)

        if not visible:
            self.penup()


def main():
    # globals
    with open('zodiac.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    dict_west = data['western_zodiac']
    dict_east = data['eastern_zodiac']

    # 1 screen
    sc = turtle.Screen()
    w = 600
    h = 600
    # size = w x h, bgcolor = grey, delay = 3
    init_screen(sc, w, h, (200,200,200), 3)

    # 2 turtle
    a = QT('xq', 'black', 1, 'turtle', True)
    b = QT('mark', 'white', 1, 'classic', False)

    user_play(a, b, dict_west)

    while input('play again? y or n: ') == 'y':
       user_play(a, b, dict_west)
    else:
        exit()


def test():
    print(break_str_line('Follow your heart as the Sagittarius moon aligns with the Nodes of Fate, dear Capricorn, trusting that you can break through barriers that once held you back. Just avoid throwing caution to the wind as Neptune activates, threatening to cloud your judgment. Youll sense a shift this evening when the moon enters your sign, forming a sweet connection to Saturn, lifting your spirits, and sharpening the mind. Take a moment to reflect on your aspirations as the day comes to a close and Mercury crosses over the sun, considering where personal adjustments can be made to maximize success.', 6))


if __name__ == '__main__':
    main()
    #test()
