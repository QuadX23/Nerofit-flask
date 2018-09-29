from flask import session, render_template, request, flash, g
from flask_login import current_user, login_user, login_required, logout_user

from Other.sqlAlchemy_insert import user_add
from app import app, db, login_manager
from app.models import User, user_info, Training
from tables import Results
from datetime import datetime, timedelta

poll_data = {
    'question': 'Ваш пол?',
    'fields': ['Мужчина', 'Женщина']
}
exp_var_data = {
    'question': 'Был ли опыт похудения?',
    'fields': ['Да, не удачный. Вес вернулся \n', 'Да, удачный. Удалось сохранить достигнутый вес \n',
               'Нет, люблю жирок']
}
eating_var_data = {
    'question': 'Как вы питаетесь?',
    'fields': ['Ем что хочу. Не ограничиваю себя', 'Стараюсь исключать вредные продукты, а в остальном не сильно слежу',
               'Стараюсь придерживаться правильного питания, но получается с переменным успехом',
               'Постоянно пробую новые диеты', 'Веду дневник питания и считаю всё съеденное']
}
training_var_data = {
    'question': 'А как дела с тренировками?',
    'fields': ['Нет опыта тренировок', 'Был опыт, но давно. Более года не тренируюсь',
               'Перодически начинаю тренироваться', 'Регулярно тренируюсь дома', 'Регулярно тренируюсь в зале']
}
activity_data = {
    'question_activity': 'Ваша активность?',
    'fields_activity': ['Низкая', 'Средняя', 'Высокая']
}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['POST'])
def index():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    result = User.query.filter_by(username=POST_USERNAME, password=POST_PASSWORD).first()

    if result:
        print('down town')
        login_user(result)
        session['logged_in'] = True

        USER_ID = User.get_id(current_user)
    else:
        flash('wrong password!')
    return home()


@app.route('/user_online')
@login_required
def hom():
    return 'The cerrent user is' + current_user.username


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        USER_ID = User.get_id(current_user)
        user = User.query.get(USER_ID)
        auth = user.auth
        if auth:
            return home_render()
        else:
            return welcome()


@app.route('/testpage')
def test_page_render():
    return render_template('voronka/walletone.html')


@app.route('/reg', methods=['POST'])
def do_register():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    user_add(POST_USERNAME, POST_PASSWORD)
    return "<h1>Register successful! <a href='/logout'>Logout</a><h1>"


# @app.route('/login', methods=['POST'])
# def do_admin_login():
#     POST_USERNAME = str(request.form['username'])
#     POST_PASSWORD = str(request.form['password'])
#
#     query = db.session.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
#     result = query.first()
#     if result:
#         global USER_ID
#         USER_ID = result.id
#         session ['logged_in'] = True
#     else:
#          flash('wrong password!')
#     return home()
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    return home()


@app.route('/welcome')
def welcome():
    return render_template('pages/start/welcome.html')


@app.route('/test/1', methods=['POST'])
def root():
    return render_template('pages/test/sex.html',data = poll_data)


@app.route('/poll')
def poll():
    USER_ID = User.get_id(current_user)
    vote = request.args.get('sex')
    if (vote == "Мужчина"):
        value = 1
    elif (vote == "Женщина"):
        value = 2
    else:
        value = 3
    user = User.query.get(USER_ID)
    user.gender = value
    print(value)
    db.session.commit()
    return data_render()


@app.route('/activity', methods=['POST'])
def activity_root():
    return render_template('pages/start/activity.html', data=activity_data)


@app.route('/activity')
def activity_poll():
    res = request.args.get('activity')
    if (res == "Низкая"):
        act = 1
    elif (res == "Средняя"):
        act = 2
    else:
        act = 3
    USER_ID = User.get_id(current_user)
    user = User.query.get(USER_ID)
    user.activity = act
    db.session.commit()
    return userinfo_render()


@app.route('/datainfo')
def data_render():
    return render_template('pages/start/data.html')


@app.route('/datainfo', methods=['POST'])
def date():
    text = request.form['date']
    USER_ID = User.get_id(current_user)
    user = User.query.get(USER_ID)
    user.data = text
    db.session.commit()
    return height_render()


@app.route('/heightinfo')
def height_render():
    return render_template('pages/start/height.html')


@app.route('/heightinfo', methods=['POST'])
def height():
    USER_ID = User.get_id(current_user)
    height = request.form['height']
    user = User.query.get(USER_ID)
    user.height = height
    db.session.commit()
    return activity_root()


@app.route('/userinfo')
def userinfo_render():
    return render_template('pages/start/user_info.html')


@app.route('/userinfo', methods=['POST'])
def userinfo():
    USER_ID = User.get_id(current_user)
    mass = request.form['mass']
    chest = request.form['chest']
    left_hand = request.form['left_hand']
    left_bedro = request.form['left_bedro']
    left_golen = request.form['left_golen']
    waist = request.form['waist']
    buttock = request.form['buttock']
    right_hand = request.form['right_hand']
    right_bedro = request.form['right_bedro']
    right_golen = request.form['right_golen']

    # print('parametrs:', mass,chest,left_hand,left_golen,left_bedro)
    # print('userinfo INFO=', mass)
    user = User.query.get(USER_ID)
    user.massuser = mass
    user.user_info = [
        user_info(mass=mass,
                  chest=chest,
                  left_hand=left_hand,
                  left_bedro=left_bedro,
                  left_golen=left_golen,
                  waist=waist,
                  buttock=buttock,
                  right_hand=right_hand,
                  right_bedro=right_bedro,
                  right_golen=right_golen,
                  user_id_helper=USER_ID)
    ]
    user.auth = True
    db.session.commit()
    return instruction_render()


@app.route('/useraddinfo')
def userinfo_add_render():
    return render_template('pages/start/user_add_info.html')


@app.route('/useradding', methods=['POST'])
def user_add_info():
    USER_ID = User.get_id(current_user)
    mass = request.form['mass']
    chest = request.form['chest']
    left_hand = request.form['left_hand']
    left_bedro = request.form['left_bedro']
    left_golen = request.form['left_golen']
    waist = request.form['waist']
    buttock = request.form['buttock']
    right_hand = request.form['right_hand']
    right_bedro = request.form['right_bedro']
    right_golen = request.form['right_golen']

    # print('parametrs:', mass,chest,left_hand,left_golen,left_bedro)
    # print('userinfo INFO=', mass)
    user = User.query.get(USER_ID)
    user.massuser = mass
    user.user_info = [
        user_info(mass=mass,
                  chest=chest,
                  left_hand=left_hand,
                  left_bedro=left_bedro,
                  left_golen=left_golen,
                  waist=waist,
                  buttock=buttock,
                  right_hand=right_hand,
                  right_bedro=right_bedro,
                  right_golen=right_golen,
                  user_id_helper=USER_ID)
    ]
    db.session.commit()
    return progress_render()


@app.route('/instruction')
def instruction_render():
    return render_template('pages/start/instruction.html')


@app.route('/home')
def home_render():
    USER_ID = User.get_id(current_user)
    user = User.query.get(USER_ID)
    username = user.username
    print(username)
    return render_template('pages/lk/home.html', username=username)


@app.route('/eat', methods=['GET', 'POST'])
def eat_render():
    USER_ID = User.get_id(current_user)
    user = User.query.get(USER_ID)
    if user.massuser is None:
        return render_template('pages/start/gender.html', data=poll_data)
    else:
        kkal_norma = int(calculator())
        belki = int(belki_calc())
        giry = int(giry_calc())
        ugl = int(ugl_cal())
    if user.kkal >= kkal_norma:
        user.kkal = 0
        user.belki = 0
        user.jiry = 0
        user.ugli = 0
        db.session.commit()
    if request.method == 'GET':
        return render_template('pages/lk/eat.html',
                               kkal_norma=kkal_norma,
                               belki=belki,
                               giry=giry,
                               ugl=ugl)
    else:
        kkal_norma = int(calculator())
        belki = int(belki_calc())
        giry = int(giry_calc())
        ugl = int(ugl_cal())
        kkalor = request.form['kkalor']
        jiry = request.form['jiry']
        belok = request.form['belok']
        ugli = request.form['ugli']
        USER_ID = User.get_id(current_user)
        user = User.query.get(USER_ID)

        user.belki += int(belok)
        user.jiry += int(jiry)
        user.kkal += int(kkalor)
        user.ugli += int(ugli)
        db.session.commit()

        kkalor_ost = kkal_norma - user.kkal
        belok_ost = kkal_norma - user.belki
        jiry_ost = kkal_norma - user.jiry
        ugli_ost= kkal_norma - user.ugli

        return render_template('pages/lk/eat.html',
                               kkalor=user.kkal,
                               belok=user.belki,
                               jiry=user.jiry,
                               ugli=user.ugli,
                               kkalor_ost=kkalor_ost,
                               belok_ost=belok_ost,
                               jiry_ost=jiry_ost,
                               ugli_ost=ugli_ost,
                               kkal_norma=kkal_norma,
                               belki=belki,
                               giry=giry,
                               ugl=ugl
                               )


@app.route('/eatadd', methods=['POST'])
def eat_add():
    return render_template('pages/lk/eat_add.html')


@app.route('/train')
def train_render():
    USER_ID = User.get_id(current_user)
    user = User.query.get(USER_ID)
    exer_1 = ''
    exer_2 = ''
    exer_3 = ''
    exer_4 = ''
    exer_5 = ''
    exer_6 = ''

    url_1 = ''
    url_2 = ''
    url_3 = ''
    url_4 = ''
    url_5 = ''
    url_6 = ''

    day_key = user.train

    day_of_train = {
        1: '1 DAY',
        2: '2 DAY',
        3: '3 DAY',
        4: '4 DAY',
        5: '5 DAY',
        6: '5 DAY'
    }

    if day_key in day_of_train:
        day = day_of_train[day_key]

    if day_key == 1:
        exer_1 = 'Разминка'
        exer_2 = 'Приседания '
        exer_3 = 'Скручивания '
        exer_4 = 'Лодочка '
        url_1 = 'c2u6aa64j80'
        url_2 = 'OhhXifdyhxs'
        url_3 = 'Sz0naPQqnPY'
        url_4 = 'XpnZE9JzRto'
    if day_key == 2:
        exer_1 = 'Выходной'
    if day_key == 3:
        exer_1 = 'Разминка'
        exer_2 = 'Выпады поочерёдно на каждую ногу'
        exer_3 = 'Ситап'
        exer_4 = 'Подъём корпуса лёжа на животе '
        url_1 = 'c2u6aa64j80'
        url_2 = 'pclYaTqMZI4'
        url_3 = 'W-ZBcZnuQqM'
        url_4 = '5eLxwsNCn1Y'
    if day_key == 4:
        exer_1 = 'Выходной'
    if day_key == 5:
        exer_1 = 'Приседания'
        exer_2 = 'Ягодичный мостик'
        exer_3 = 'Отжимания с колен'
        exer_4 = 'Скалолаз '
        exer_5 = 'Планка'
        url_1 = 'c2u6aa64j80'
        url_2 = 'UsJMO-wLf0Y'
        url_3 = 'LecVKn8Q-MM'
        url_4 = 'Sz0naPQqnPY'
        url_5 = 'XpnZE9JzRto'
    if day_key == 5:
        exer_1 = 'Выходной'

    a = datetime.now()
    b = timedelta(days=1)
    c = datetime(2018, 10, 10, 0, 0, 0)
    str(a)
    tomorrow_data = a + b
    now_data = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    current_data = datetime.strftime(tomorrow_data, "%Y-%m-%d %H:%M:%S")
    time_now = datetime.strftime(datetime.now(), "%H:%M:%S")
    time_zero = datetime.strftime(c, "%H:%M:%S")

    return render_template('pages/lk/train.html',
                           day=day,
                           exer_1=exer_1, exer_2=exer_2, exer_3=exer_3,
                           exer_4=exer_4, exer_5=exer_5, exer_6=exer_6,
                           url_1=url_1, url_2=url_2, url_3=url_3,
                           url_4=url_4, url_5=url_5, url_6=url_6)


@app.route('/home', methods=['POST'])
def start_home():
    USER_ID = User.get_id(current_user)
    user = User.query.get(USER_ID)
    username = user.username
    print(username)
    return render_template('pages/lk/home.html', username=username)


@app.route('/progress')
def progress_render():
    # query = db_session.query(user_info)
    USER_ID = User.get_id(current_user)
    results = user_info.query.filter(user_info.user_id_helper == USER_ID)
    # results = query.all()
    print('Hueg', results)
    table = Results(results, classes=['yellowTable'])
    table.border = True

    return render_template('pages/lk/progress.html', table=table)


@app.route('/progress', methods=['POST'])
def progress_btn():
    return userinfo_add_render()


@app.route('/testpopup')
def popup_render():
    return render_template('another/test.html')


# @app.route("/logout")
# def logout():
#     session['logged_in'] = False
#     return home()

@app.route('/article')
def article_render():
    return render_template('another/article.html')


@app.route('/video')
def video_main_render():
    return render_template('video/video_main.html')

@app.route('/video/1', methods=['GET', 'POST'])
def video_1_render():
    return render_template('video/1_video.html')

@app.route('/video/2', methods=['GET', 'POST'])
def video_2_render():
    return render_template('video/2_video.html')

@app.route('/video/3', methods=['GET', 'POST'])
def video_3_render():
    return render_template('video/3_video.html')

@app.route('/video/4', methods=['GET', 'POST'])
def video_4_render():
    return render_template('video/4_video.html')


def calculator():
    USER_ID = User.get_id(current_user)
    user = User.query.get(USER_ID)
    print('metatag usera', user.username)
    mass = int(user.massuser)
    gender = int(user.gender)

    r = r_calc()
    l = l_calc()

    m = mass

    if (gender == 1):
        Dn = (6.83 * m + 7 * (m * 26.67 * r * (1 + l))) * 0.13
        return Dn
    elif (gender == 2):
        Dn = (5.94 * m + 7 * (m * 24.44 * r * (1 + l))) * 0.13
        return Dn
    else:
        return


def belki_calc():
    Dn = calculator()
    return 0.075 * Dn


def giry_calc():
    Dn = calculator()
    return 0.04 * Dn


def ugl_cal():
    Dn = calculator()
    return 0.088 * Dn


def r_calc():
    USER_ID = User.get_id(current_user)
    user = User.query.get(USER_ID)
    age = int(user.data)
    r = 1
    if age <= 25:
        r = 1
    elif 25 < age <= 35:
        r = 0.95
    elif 35 < age <= 45:
        r = 0.9
    elif 45 < age <= 55:
        r = 0.85
    elif age > 55:
        r = 0.8
    return float(r)


def l_calc():
    USER_ID = User.get_id(current_user)
    user = User.query.get(USER_ID)
    activity = 1
    activity = int(user.activity)
    l = 0.06
    if (activity == 1):
        l = 0.05
    elif (activity == 2):
        l = 0.06
    elif (activity == 3):
        l = 0.07
    else:
        l = 0.06
    return float(l)

@app.route('/payment/redirect/98rubles',methods=['GET', 'POST'])
def payment_98():
    return render_template('payment/payment_98.html')



@app.route('/test/start',methods=['GET', 'POST'])
def start_test():
    return render_template('quiz/index.html')

@app.route('/test/sex', methods=['GET', 'POST'])
def sex_test():
    return render_template('quiz/sex.html')

@app.route('/test/age', methods=['GET', 'POST'])
def age_test():
    return render_template('quiz/age.html')

@app.route('/test/experience',methods=['GET', 'POST'])
def experience_test():
    return render_template('quiz/experience.html')

@app.route('/test/feed',methods=['GET', 'POST'])
def feed_test():
    return render_template('quiz/feed.html')

@app.route('/test/training',methods=['GET', 'POST'])
def training_test():
    return render_template('quiz/training.html')

@app.route('/test/submit',methods=['GET', 'POST'])
def submit_test():
    return render_template('quiz/submit.html')

@app.route('/test/final',methods=['GET', 'POST'])
def final_test():
    return render_template('quiz/final.html')



@app.route('/next_day', methods=['POST'])
def success_train_changer():
    USER_ID = User.get_id(current_user)
    user = User.query.get(USER_ID)
    user.train += 1
    if user.train > 6:
        user.train = 1
    db.session.commit()
    return home()
