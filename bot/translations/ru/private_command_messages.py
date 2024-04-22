START_MESSAGE = (
    'Смотрящий в пустоту приветствует тебя, {username}! '
    'Я здесь и готов служить.\n'
    'Напиши /help для получения списка команд.'
)

HELP_MESSAGE = (
    'Пока мои возможности ограничены этим:\n'
    'Команды в приватном чате:\n'
    '- /start - запуск бота\n'
    '- /help - список команд\n'
    '- /unban - разбанить забаненного пользователя\n'
    'Команды в чате группы:\n'
    '- /ban - забанить пользователя\n'
    '- /restrict (время ограничения)'
)

ID_UNBAN_MESSAGE = (
    'Введи ID того, кого ты хочешь освободить,'
    ' в формате "ID=ID пользователя".'
    ' Например: ID=123456789.'
    ' Либо введи "Отмена" и мы прекратим эту игру.'
)

FULL_NAME_UNBAN_MESSAGE = (
    'Введи имя того, кого ты хочешь освободить,'
    ' в формате "Имя=Полное Имя".'
    ' Например: Имя=Иван Иванов.'
    ' Имя должно быть полным, то есть таким,'
    ' как оно указано у пользователя в Telegram,'
    ' вместе с фамилией, если она указана, и прочими символами.'
    ' Либо введи "Отмена" и мы прекратим эту игру.'
)

UNBAN_MESSAGE = (
    'Вглядись, {username}!  '
    'Почуствуй ту мерзость, что источают их зловонные души! '
    'Ты всё ещё думаешь, что кто-то из них достоин свободы? '
)

CHOICE_SELECT_MESSAGE = (
    'Ты уверен, что правда хочешь этого, {username}?'
)

CONFIRM_MESSAGE = (
    'Не пожалей о своём выборе, {username}.'
)

CANCEL_MESSAGE = (
    'Отменено.'
)

FINISH_UNBAN_MESSAGE = (
    'Теперь он свободен. '
    'Все его новые грехи теперь на твоей совести, {username}. '
    'Но ты можешь забанить его ещё раз.'
)

INCORRECT_ID_MESSAGE = (
    'Ты ввёл некорректный ID, {username}.'
    ' Попробуй ещё раз, либо введи "Отмена" и мы прекратим.'
)

USER_NOT_FOUND_IN_DB_MESSAGE = (
    'Такого пользователя нет в базе, {username}.'
    ' Попробуй ещё раз, либо введи "Отмена" и мы прекратим.'
)

NO_BANNED_USERS_MESSAGE = (
    'Здесь так пусто, {username}.'
    ' Не повод ли это кого-то сюда добавить?'
)