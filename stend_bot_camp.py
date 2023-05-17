import telebot
from telebot import types
import os

bot = telebot.TeleBot('yourToken')
scores={"1": ['Энакин', 'Эрен', 'Элли'],
        "2": ['Галадриэль', 'Музан', 'Танджиро'],
        "3": ['Лютик', 'Санса', 'Фродо'],
        "4": ['Наруто', 'Шерлок', 'Гермиона']}
admin = []                                              #список администраторов
flag = 0

personNames={"1": ['Энакин', 'Эрен', 'Элли'],
        "2": ['Галадриэль', 'Музан', 'Танджиро'],
        "3": ['Лютик', 'Санса', 'Фродо'],
        "4": ['Наруто', 'Шерлок', 'Гермиона']}

@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id, message.chat.first_name)
    with open('users_chat_id.txt', mode = 'a') as f:                    #запись людей, взаимодействующих с ботом
        f.write(str(message.chat.id) + '\n')

    if message.from_user.username in admin:
        markup_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Очки')
        btn2 = types.KeyboardButton('Игроки')
        markup_admin.add(btn1, btn2)
        
        bot.send_message(message.chat.id, 'admin', parse_mode='html', reply_markup=markup_admin)

else:                                                                     #вводный текст (часть 1)                                                      
        markupGreet = types.InlineKeyboardMarkup()
        reply1 = "Приветствую тебя, мой юный друг! Я - Ариадна, волшебная героиня, которая сопровождает будущих взрослых на их пути. Я знаю множество историй и миров, знаю о любимых многими персонажах и черпаю из их жизней то самое ценное, что так пригождается в реальном мире детям и подросткам. Я помогаю создавать целые миры через игру, в которой такие как ты могут лучше понять себя и определить свои цели в жизни. И сейчас я предлагаю тебе пройти одну из таких игр, или даже перформансов, испытать на себе самые яркие моменты взросления, которые только можно представить в таком интересном месте. Мои герои, которых ты видишь рядом с зеркалом, будут сопровождать тебя, так же у тебя будет возможность пройти пути взросления как некоторые из них. Но только в финале ты узнаешь, путь какого персонажа ты прошел. Готов попробовать?" 
        btn1_ready = types.InlineKeyboardButton('Готов/a', callback_data='greet1')
        markupGreet.add(btn1_ready)

        send_pictures(message.chat.id, 'АРИАДНА', reply1, markupGreet)

@bot.callback_query_handler(func=lambda c: c.data.startswith('greet'))
def greetings(callback: types.CallbackQuery):

    if callback.data[-1] == '1':                                #вводный текст (часть 2)
        markupGreet2 = types.InlineKeyboardMarkup()
        btn2_ready = types.InlineKeyboardButton('Понятно! Давай играть', callback_data='greet2')

        reply2 = "Отлично, я рада, что ты готов доверить мне свое время и попробовать повзрослеть. Помимо того, что ты лучше поймешь себя и мир вокруг, ты можешь собрать особые достижения в игре: их получат самые внимательные, общительные, а еще те, кто будет чаще и сильнее похож на одного из моих героев, на каждом из этапов взросления. А некоторые достижения ты откроешь уже сам... Призом для тех, кто соберет 7 и больше достижений, станет мой личный подарок. Если ты хочешь прояснить систему достижений и призов, спроси у девушек в фиолетовых футболках рядом с зеркалом - это мои друзья, они тебе помогут. К ним можно обратиться по любому вопросу об игре в любой момент."

        markupGreet2.add(btn2_ready)
        bot.send_message(callback.from_user.id, reply2, parse_mode='html', reply_markup=markupGreet2)

    elif callback.data[-1] == '2':
        reply3 = "У вросления есть множество путей. Каждый проходит этот этап по-разному, и в разных маршрутах есть свои сходства с моими героями. То, что объединяет их - это место, Торговый Развлекательный Центр. Через него проходят люди разных возрастов, здесь случаются испытания, соблазны, радости и сложности. И мои пути для тебя сегодня лежат через него. Выбери один и начнем свой путь!'\n'- Варианты маршрутов:"


        bot.send_message(callback.from_user.id, reply3,
                         parse_mode='html', reply_markup=create_reply_markup())

###############################HELP FUNCTIONS##########################################

def create_reply_markup():                                                         #создание стсартовой клавиатуры
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Бытовые дилеммы')
        btn2 = types.KeyboardButton('Маршрут Смелость и любопытство')
        btn3 = types.KeyboardButton('Маршрут Звук и мир')
        btn4 = types.KeyboardButton('Фотографический маршрут')
        markup.add(btn1, btn2)
        markup.add(btn3, btn4)

        return markup

def max_scores(scores, name):                                           #подсчёт максимума набираемых очков
    max_value = max(scores[name])
    max_index = scores[name].index(max_value)

    return max_index
##################################################___FILE READERS___######################################################
        
@bot.message_handler(content_types=['photo', 'video'])
def photo_collector(message):                                                                      #обработка присланных пользователем фотографий
    name = str(message.chat.first_name) + str(message.chat.last_name)
    
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    else:
        file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    previousDirectory = os.getcwd()
    
    try:
        os.makedirs('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+name)
        os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+name)
    except FileExistsError:
        os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+name)

    if message.content_type == 'photo':
        src = os.getcwd() +'/'+ name + message.photo[1].file_id[30:36]+'.jpg'

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

    else:
        src = os.getcwd() +'/'+ name + message.video.file_id[30:36]+'.mp4'

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    os.chdir(previousDirectory)
    bot.reply_to(message, "Отлично, не забудь нажать кнопку!")

def get_free_answers(message):                                                                          #обработка ответов пользователя на свободные вопросы
    name = str(message.chat.first_name) + str(message.chat.last_name)
    previousDirectory = os.getcwd()
   
    try:
        os.makedirs('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+name)
        os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+name)
    except FileExistsError:
        os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+name)

    src = os.getcwd() +'/'+ name + str(message.id)+'.txt'
    with open(src, 'w') as new_file:
            new_file.write(message.text)

    os.chdir(previousDirectory)
    bot.reply_to(message, "Не забудь нажать кнопку выше!")

def send_audio (chat_id, type_of_file, name_of_file):                                                   #отправка ботом аудио

    previousDirectory = os.getcwd()
    os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/Маршрут 3/materials')

    if type_of_file == 'audio':
        audio = open (f'{os.getcwd()}/'+name_of_file+'.mp3', mode='rb')
        bot.send_audio(chat_id, audio)
    else:
        photo = open (f'{os.getcwd()}/'+name_of_file+'.jpg', mode='rb')
        bot.send_photo(chat_id, photo)
    os.chdir(previousDirectory)

def send_pictures(chat_id, name_of_file, text, markup=None):                                    #отправка ботом фотографий
    previousDirectory = os.getcwd()
    os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/personagePhotos')

    photo = open (f'{os.getcwd()}/'+name_of_file+'.png', mode='rb')
    if markup == None:
        bot.send_photo(chat_id, photo, caption = text)
    else:
        bot.send_photo(chat_id, photo, caption = text, reply_markup=markup)
    os.chdir(previousDirectory)

##########################################____MARSHRUTY____##########################################################################
def marshrut (message):                                                                         #переключение на директорию с нужным маршрутом
    match (message.text):
        case 'Бытовые дилеммы':
            marshrutNumber = '1'
        case 'Маршрут Смелость и любопытство':
            marshrutNumber = '2'
        case 'Маршрут Звук и мир':
            marshrutNumber = '3'
        case 'Фотографический маршрут':
            marshrutNumber = '4'
            
    os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/Маршрут ' + marshrutNumber)
    scores[str(message.chat.first_name) + str(message.chat.last_name) + marshrutNumber] = [0, 0, 0]
    segment(message.chat, 1, 1, int(marshrutNumber))
    
def segment(chat, taskNumber, segmentNumber, marshrutNumber):                                   #обработчик сегментов. в данной функции отслеживается процесс прохождения пользователем квеста
    global flag
    marshrutNumber = str(marshrutNumber)
    print(chat.first_name, ' ', marshrutNumber, ' ', os.getcwd(), ' segment')
    
    chat_id = chat.id
    markupReady = types.InlineKeyboardMarkup()
    btn1_ready = types.InlineKeyboardButton('Готово', callback_data=f'ready{marshrutNumber}{segmentNumber}{taskNumber}')
    markupReady.add(btn1_ready)
    name = str(chat.first_name) + str(chat.last_name) + str(marshrutNumber)

    if taskNumber != 4 and segmentNumber != 5:                                                                  #специальные условия для некоторых маршрутов (задано спецификой маршрута)
        os.chdir(f'C:/Users/smesh/Desktop/proga/python/bot/stend/Маршрут {marshrutNumber}/segment{segmentNumber}')
        with open(f'Intro{taskNumber}.txt', mode = 'r', encoding='utf-8') as f:
            intro = f.read()

        if marshrutNumber == '2' and taskNumber == 1 and flag == 0:
            with open('preIntro.txt', mode = 'r', encoding='utf-8') as f:
                preIntro = f.read()
                
            markupPreReady = types.InlineKeyboardMarkup()
            btn1_preready = types.InlineKeyboardButton('Я на месте', callback_data=f'free2{marshrutNumber}{segmentNumber}{taskNumber}')
            markupPreReady.add(btn1_preready)

            bot.send_message(chat_id, preIntro, parse_mode='html', reply_markup=markupPreReady)
            
        elif marshrutNumber == "3" and segmentNumber == 1 and taskNumber == 2:
            send_audio(chat_id, 'audio', 'Знаки зодиака')
            bot.send_message(chat_id, intro, parse_mode='html', reply_markup=markupReady)
        elif marshrutNumber == "3" and segmentNumber == 3 and taskNumber == 2:
            send_audio(chat_id, 'audio', 'Море')
            bot.send_message(chat_id, intro, parse_mode='html', reply_markup=markupReady)
        elif marshrutNumber == "3" and segmentNumber == 3 and taskNumber == 3:
            send_audio(chat_id, 'audio', 'Дорога на работу')
            send_audio(chat_id, 'photo', 'Дорога на работу. Маршрут')
            bot.send_message(chat_id, intro, parse_mode='html', reply_markup=markupReady)

        else:
            bot.send_message(chat_id, intro, parse_mode='html', reply_markup=markupReady)
                
    elif taskNumber == 4:                                                               #переход на следующий сегмент
        flag = 0
        finalPers = max_scores(scores, name)
        try:
            print(os.getcwd())
            with open (f'{os.getcwd()}/final{finalPers}.txt', mode = 'r', encoding='utf-8') as f:
                send_pictures(chat_id, personNames[marshrutNumber][finalPers].upper(), f.read())
        except:
            pass
        
        os.chdir(f'C:/Users/smesh/Desktop/proga/python/bot/stend/Маршрут {marshrutNumber}')
        segment (chat, 1, segmentNumber+1, marshrutNumber)
    else:                                                                       #финал маршрута
        finalMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Ещё бы один маршрутик пройти')
        btn2 = types.KeyboardButton('Узнать свой путь')

        finalMarkup.add(btn1, btn2)
        
        bot.send_message(chat_id, 'Вот ты и повзрослел. Разные этапы этого пути ты прошел по-своему, но это было схоже с некоторыми моими героями. Сейчас ты можешь выбрать: закончить игру и узнать героя, на чей путь был похож твой больше всего или пройти еще один из моих маршрутов, если среди них остались непройденные тобой. Внутри них все еще есть достижения, которые можно собрать и получить мой подарок! Выбирай мудро.\n\n - Пройти еще один маршрут\n- Узнать чей путь я прошел'
                         , parse_mode='html', reply_markup=finalMarkup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('ready'))
def pre_task(callback_query: types.CallbackQuery):                                      #вывод задания и вариантов ответа
   
    taskNumber = callback_query.data[-1]
    segmentNumber = callback_query.data[-2]
    marshrutNumber = callback_query.data[-3]
    
    os.chdir(f'C:/Users/smesh/Desktop/proga/python/bot/stend/Маршрут {marshrutNumber}/segment{segmentNumber}')
        
    with open(f'Task{taskNumber}.txt', mode = 'r', encoding='utf-8') as f:
        task = f.read()
        
    markupSegment1 = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Вариант 1', callback_data=f'choice{marshrutNumber}{segmentNumber}{taskNumber}1')
    btn2 = types.InlineKeyboardButton('Вариант 2', callback_data=f'choice{marshrutNumber}{segmentNumber}{taskNumber}2')
    btn3 = types.InlineKeyboardButton('Вариант 3', callback_data=f'choice{marshrutNumber}{segmentNumber}{taskNumber}3')
    markupSegment1.add(btn1, btn2, btn3)
        
    if marshrutNumber == '3' and segmentNumber == '1' and taskNumber == '3':
        btn4 = types.InlineKeyboardButton('Вариант 4', callback_data=f'choice{marshrutNumber}{segmentNumber}{taskNumber}1')
        btn5 = types.InlineKeyboardButton('Вариант 5', callback_data=f'choice{marshrutNumber}{segmentNumber}{taskNumber}3')
        btn6 = types.InlineKeyboardButton('Вариант 6', callback_data=f'choice{marshrutNumber}{segmentNumber}{taskNumber}2')
        markupSegment1.add(btn4, btn5, btn6)

    print(callback_query.from_user.first_name, ' ', marshrutNumber, ' ', os.getcwd(), ' pre_task')

    with open(os.getcwd()+ '/personageDistribution.txt', mode = 'r') as f:
        distr = [line for line in f]

    if distr[int(taskNumber)-1][0] !='-':
        bot.send_message(callback_query.from_user.id, task, parse_mode='html',
                             reply_markup=markupSegment1)
    else:
        markupReady = types.InlineKeyboardMarkup()
        btn1_ready = types.InlineKeyboardButton('Готово', callback_data=f'free_ready{marshrutNumber}{segmentNumber}{taskNumber}')
        markupReady.add(btn1_ready)

        bot.send_message(callback_query.from_user.id, task, parse_mode='html',
                             reply_markup=markupReady)

        

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('free'))
def free_ready_reaction(callback_query: types.CallbackQuery):
    global flag

    taskNumber = int(callback_query.data[-1])
    segmentNumber = int(callback_query.data[-2])
    marshrutNumber = callback_query.data[-3]
    
    if callback_query.data[-4] != '2':
        segment(callback_query.from_user, taskNumber+1, segmentNumber, marshrutNumber)
    else:
        flag = 1
        segment(callback_query.from_user, taskNumber, segmentNumber, marshrutNumber)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('choice'))
def process_callback(callback_query: types.CallbackQuery):
    taskNumber = callback_query.data[-2]
    segmentNumber = callback_query.data[-3]
    marshrutNumber = callback_query.data[-4]

    os.chdir(f'C:/Users/smesh/Desktop/proga/python/bot/stend/Маршрут {marshrutNumber}/segment{segmentNumber}')
    
    print(callback_query.from_user.first_name, ' ', marshrutNumber, ' ', os.getcwd(), ' process_callback')
    
    task(callback_query, int(taskNumber), int(segmentNumber), int(callback_query.data[-4]))

def task(callback_query, taskNumber, segmentNumber, marshrutNumber):                            #реализация выборов в задании
    global scores

    choiceNumber = callback_query.data[-1]
    bot.edit_message_reply_markup(callback_query.from_user.id,
                                  message_id = callback_query.message.id,
                                  reply_markup = '')
    os.chdir(f'C:/Users/smesh/Desktop/proga/python/bot/stend/Маршрут {marshrutNumber}/segment{segmentNumber}')

    name = str(callback_query.from_user.first_name) + str(callback_query.from_user.last_name) + str(marshrutNumber)
    currentDirectory = os.getcwd()

    print(callback_query.from_user.first_name, ' ', marshrutNumber, ' ', currentDirectory, ' task')

    with open(currentDirectory+ '/personageDistribution.txt', mode = 'r') as f:
        distr = [line for line in f]
        
        
    match (choiceNumber):
        case '1':           
            try:
                scores[name][int(distr[taskNumber-1][0])]+=1
                bot.send_message(callback_query.from_user.id,'Выбор сделан')
                title = str(callback_query.from_user.first_name) + str(callback_query.from_user.last_name)
                try:
                    os.makedirs('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+title)
                    os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+title)
            
                except FileExistsError:
                    os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+title)
            
            
                with open (f'{os.getcwd()}/choices_answers.txt', mode='a') as f:
                    f.write(f'Маршрут {marshrutNumber}, Сегмент {segmentNumber}, Задание {taskNumber}, Выбор 1, {personNames[str(marshrutNumber)][0]}'+'\n')
            except:
                pass

        case '2':
            try:
                scores[name][int(distr[taskNumber-1][1])]+=1
                bot.send_message(callback_query.from_user.id,'Выбор сделан')
                title = str(callback_query.from_user.first_name) + str(callback_query.from_user.last_name)
                try:
                    os.makedirs('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+title)
                    os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+title)
            
                except FileExistsError:
                    os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+title)
            
            
                with open (f'{os.getcwd()}/choices_answers.txt', mode='a') as f:
                    f.write(f'Маршрут {marshrutNumber}, Сегмент {segmentNumber}, Задание {taskNumber}, Выбор 2, {personNames[str(marshrutNumber)][1]}'+'\n')
            except:
                pass
           

        case '3':
            try:
                scores[name][int(distr[taskNumber-1][2])]+=1
                bot.send_message(callback_query.from_user.id,'Выбор сделан')
                title = str(callback_query.from_user.first_name) + str(callback_query.from_user.last_name)
                try:
                    os.makedirs('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+title)
                    os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+title)
            
                except FileExistsError:
                    os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/'+title)
            
            
                with open (f'{os.getcwd()}/choices_answers.txt', mode='a') as f:
                    f.write(f'Маршрут {marshrutNumber}, Сегмент {segmentNumber}, Задание {taskNumber}, Выбор 3, {personNames[str(marshrutNumber)][2]}'+'\n')
            except:
                pass


    try:
        with open(currentDirectory+ f'/Perehod{taskNumber}.txt', mode = 'r', encoding='utf-8') as f:
            bot.send_message(callback_query.from_user.id,f.read())
    except:
        pass

    if taskNumber == 3 and marshrutNumber == 3:
        try:
            with open(currentDirectory+ '/semiFinal.txt', mode = 'r', encoding='utf-8') as f:
                send_audio(callback_query.from_user.id, 'audio', 'Переход')
                bot.send_message(callback_query.from_user.id,f.read())
        except:
            pass
    os.chdir(currentDirectory)    
    print('запись в словарь/файл ', scores)
    segment(callback_query.from_user, taskNumber+1, segmentNumber, callback_query.data[-4])


#############################################################################################################################
#######################______ADMIN BLOCK_________###########################################################################################
def adminScores(message):                               #демонстрация очков для администратора
    global scores
    if message.from_user.username in admin:
        output=" "
        for key, value in scores.items():
            output += f'<b>{key}</b> {str(value)}\n'

        bot.send_message(message.chat.id, output, parse_mode='html')


def adminPlayers(message):                                                              #доступ к списку пользователей
    if message.from_user.username in admin:
        previousDirectory = os.getcwd()
        os.chdir('C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers')
        markupPlayers = types.InlineKeyboardMarkup()
        for users in os.listdir():    
            btn = types.InlineKeyboardButton(users, callback_data=f'user{users}')
            markupPlayers.add(btn)
        os.chdir(previousDirectory)  
        bot.send_message(message.chat.id, 'Список игроков', parse_mode='html', reply_markup=markupPlayers)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('user'))
def get_user_data(callback_query: types.CallbackQuery):                                 #доступ к медиафайлам пользователей
    if callback_query.from_user.username in admin:
        
        path = f'C:/Users/smesh/Desktop/proga/python/bot/stend/user_answers/{callback_query.data[4:]}'
        media_group=[]
        text =''
        bot.send_message(callback_query.from_user.id, f'Файлы {callback_query.data[4:]}')
        for item in os.listdir(path):
            if item[-3:] == 'txt':
                with open(path+f'/{item}', mode='r') as f:
                    text+=f.read()+'\n\n'
        for item in os.listdir(path):
            if item[-3:] == 'jpg':
                photo = open (path+f'/{item}', mode='rb')
                media_group.append(types.InputMediaPhoto(photo, caption = text))
                #bot.send_photo(callback_query.from_user.id, photo)
            elif item[-3:] == 'mp4':
                video = open (path+f'/{item}', mode='rb')
                media_group.append(types.InputMediaVideo(video, caption = text))
                #bot.send_video(callback_query.from_user.id, video)
        try:
            for i in range(len(media_group)//10+1):
                if i !=len(media_group):
                    bot.send_media_group(callback_query.from_user.id, media_group[(0+10*i):(10+10*i)])
                else:
                    bot.send_media_group(callback_query.from_user.id, media_group[(0+10*i):len(media_group)])
            bot.send_message(callback_query.from_user.id, text)
        except:
            if text !='':
                bot.send_message(callback_query.from_user.id, text)
            else:
                bot.send_message(callback_query.from_user.id, 'Нет данных')
##########################################################################################################################
        
@bot.message_handler(content_types=['text'])                            #обработка текстовых сообщений
def get_user_text(message):
    emptyKeyboard = types.ReplyKeyboardRemove()

    match (message.text):
        case 'Бытовые дилеммы':
            bot.send_message(message.chat.id, 'Выбран маршрут Бытовые дилеммы', parse_mode='html', reply_markup=emptyKeyboard)
            marshrut(message)
        case 'Маршрут Смелость и любопытство':
            bot.send_message(message.chat.id, 'Выбран маршрут Смелость и любопытство', parse_mode='html', reply_markup=emptyKeyboard)
            marshrut(message)
        case 'Маршрут Звук и мир':
            add_info ='Этот путь будет сопровождаться треком, прежде чем отправлять на точку в маршруте твоего взросления, включай данный трек. А теперь включай трек, отправляйся в Дивный Город, от стенда пройди налево, за реку, продолжай идти вперед, пока не увидишь соотвествующую надпись.'
            bot.send_message(message.chat.id, 'Выбран маршрут 3', parse_mode='html', reply_markup=emptyKeyboard)
            bot.send_message(message.chat.id, add_info, parse_mode='html', reply_markup=emptyKeyboard)
            send_audio(message.chat.id, 'audio', 'Переход')
            marshrut(message)
        case 'Фотографический маршрут':
            bot.send_message(message.chat.id, 'Выбран Фотографический маршрут', parse_mode='html', reply_markup=emptyKeyboard)
            marshrut(message)
        case 'Очки':
            adminScores(message)
        case 'Игроки':
            adminPlayers(message)
        case 'Ещё бы один маршрутик пройти':
            bot.send_message(message.chat.id, 'Тогда выбирай!', parse_mode='html', reply_markup=create_reply_markup())
        case 'Узнать свой путь':
            bot.send_message(message.chat.id, 'Чтобы узнать результаты, отправляйся к началу своего пути!') 
        case _:
            get_free_answers(message)

      
bot.polling(none_stop=True)
