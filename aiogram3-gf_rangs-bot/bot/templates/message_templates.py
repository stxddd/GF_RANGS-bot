welcome_message = 'Дорогой активист ГФ, мы создали данный бот для упрощения работы с ранговой системой.'
registation_message = 'Начнем с регистрации '
already_register_message = "Ты уже зарегистрирован, выбери что хочешь сделать!"

enter_fullname_message = 'Укажи свое ФИО'
enter_course_number_message = 'На каком ты курсе (отравь число)'
enter_group_name_message = 'В какой ты группе?'

success_registration_message = "🔹 Регистрация успешно завершена! Выбери действие "

register_error = '❌ Ошибка регистрации! Попробуйте позднее'

enter_event_name_message = "Укажите название мероприятия"
enter_role_name_message = "Укажите название роли"

def event_message(roles, event):
    if not roles:
        return "У этого события пока нет ролей."

    message_lines = [f"Роли события «{event.name}»\n"]
    for role in roles:
        message_lines.append(f"• {role.name} — {role.points} балл(ов)")

    message = "\n".join(message_lines) + "\n\n" + "Участники:"
    
    return message

def user_info_message(user, role, event):
    return f"Мероприятие «{event.name}»\n\n{user.fullname}\n{user.course_number} курс\nГруппа {user.group_number}\n\nРоль на мероприятии: {role.name}\nБаллов: {role.points}"
        
    
def are_you_sure_to_delete_user_message(user, event, role):
    return f"Вы уверены что хотите удалить {user.fullname} | {role.name} c этого мероприятия {event.name}?"

def are_you_sure_to_delete_event_message(event):
    return "Вы уверены, что хотите удалить мепроприятие? У всех участников остануться баллы."


ENTER_EVENT_NAME_MESSAGE = "✏ Введите название события:"
EMPTY_EVENT_NAME_MESSAGE = "⚠ Название не может быть пустым. Попробуйте снова:"
EVENT_ADDED_SUCCESS_MESSAGE = "✅ Событие «{name}» успешно добавлено."
EVENT_ADD_ERROR_MESSAGE = "❌ Произошла ошибка при добавлении события. Попробуйте позже."

NO_EVENTS_MESSAGE = "📭 На данный момент нет ни одного мероприятия."
ALL_EVENTS_MESSAGE = "📋 Список всех мероприятий:"

NO_EVENT_FOUND_MESSAGE = "⚠ Указанное мероприятие не найдено."

CONFIRM_DELETE_EVENT_MESSAGE = "❗ Вы уверены, что хотите удалить мероприятие «{name}»?"
EVENT_DELETED_SUCCESS_MESSAGE = "🗑 Мероприятие успешно удалено."
EVENT_DELETE_ERROR_MESSAGE = "❌ Ошибка при удалении мероприятия."

NO_EVENTS_FOR_ROLE_MESSAGE = "📭 Нет доступных событий. Сначала добавьте хотя бы одно событие."
EVENTS_LIST_MESSAGE = "📋 Список доступных событий:\n{events}"
ENTER_EVENT_ID_MESSAGE = "✏ Введите ID события, к которому хотите добавить роль:"

INVALID_EVENT_ID_MESSAGE = "⚠ Введите корректный числовой ID события."
EVENT_NOT_FOUND_MESSAGE = "❌ Событие с таким ID не найдено. Попробуйте снова."

ENTER_ROLE_NAME_MESSAGE = "✏ Введите название роли:"
EMPTY_ROLE_NAME_MESSAGE = "⚠ Название роли не может быть пустым. Попробуйте снова."

ENTER_ROLE_POINTS_MESSAGE = "✏ Введите количество очков для роли:"
INVALID_ROLE_POINTS_MESSAGE = "⚠ Введите корректное целое число для очков."

ROLE_ADDED_SUCCESS_MESSAGE = (
    "✅ Роль {name} для события (ID: {event_id}) с {points} очками успешно добавлена."
)
ROLE_ADD_ERROR_MESSAGE = "❌ Ошибка при добавлении роли. Попробуйте снова."

USER_NOT_FOUND_MESSAGE = "❌ Пользователь не найден."
USER_DELETE_ERROR_MESSAGE = "⚠ Ошибка при удалении пользователя."
USER_DELETED_MESSAGE = "✅ Пользователь успешно удалён."

def your_points_message(date, points, events_info):
    if points == 0:
        return 'У вас ещё нет баллов!'
    answer = f"На {date} вы заработали баллов: {points}\n\n" 
    for events_info_item in events_info:
        answer += str(events_info_item) + '\n'
    return  answer
