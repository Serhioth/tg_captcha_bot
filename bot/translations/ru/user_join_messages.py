from bot.core.config import settings

USER_JOIN_MESSAGE = (
    'Приветствуем тебя, {username}! '
    'Пожалуйста, докажи свою принадлежность к людям. '
    'Нажми на кнопку с символом - "{symbol}".\n'
    f'У тебя есть {settings.captcha_answer_timeout} секунд, чтобы подумать. '
    'Выбирай мудро!'
)
