from datetime import datetime, timedelta
from random import randint


def check_expire_time(request):
    try:
        expire_time = datetime.strptime(request.session['expire_code_time'], '%Y-%m-%d %H:%M:%S')
    except KeyError:
        expire_time = None

    if expire_time:
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        if (now - expire_time) > timedelta(minutes=2):
            del request.session['code']
            del request.session['expire_code_time']


def set_phone_number_session(request, phone_number):
    request.session['phone_number'] = phone_number
    request.session['code'] = randint(1000, 9999)
    request.session['expire_code_time'] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(request.session['code'])
    print(request.session['expire_code_time'])
