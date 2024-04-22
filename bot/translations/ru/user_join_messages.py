from bot.core.constants import ANSWER_TIMEOUT

USER_JOIN_MESSAGE = (
    'Приветствуем тебя, {username}! '
    'Пожалуйста, докажи свою принадлежность к людям. '
    'Нажми на кнопку с символом - "{symbol}."\n'
    f'У тебя есть {ANSWER_TIMEOUT} секунд, чтобы подумать. '
    'Выбирай мудро!'
)

USER_CORRECT_ANSWER_MESSAGE = (
    'Добро пожаловать, {username}! '
    'Круг Хранителей приветствует тебя!'
)

USER_INCORRECT_ANSWER_MESSAGE = (
    '{username} не справился с заданием! '
    'Он был клеймлён печатью позора и изгнан!\n'
    'Прощай, {username}.'
)

USER_TIMEOUT_MESSAGE = (
    'Мы ждали ответа, {username}. '
    'К сожалению, он не прозвучал.'
    'Так отправляйся в ту бездну, откуда ты пришёл, {username}.'
)

NON_TARGET_USER_MESSAGE = (
    'Это испытание не для тебя, {username}!'
)
