welcome_message = """
*Привет, активист ГФ!*
Мы создали этого бота для работы с ранговой системой. Здесь ты можешь:  
🔹 Получать баллы за участие в мероприятиях  
🔹 Проверять свой текущий ранг  
🔹 Узнавать, сколько баллов осталось до следующего уровня  
🔹 Читать подробнее о ранговой системе
"""

registration_message = "Давай начнём с регистрации!"
already_register_message = "Ты уже зарегистрирован, выбери, что хочешь сделать!"

enter_fullname_message = "Укажи своё ФИО"
enter_course_number_message = "На каком ты курсе? (отправь число)"
enter_group_name_message = "В какой ты группе?"

success_registration_message = "🔹 Регистрация успешно завершена!"
accec_deny_message = "❌ Тебе отказано в доступе"
register_error = "❌ Ошибка регистрации! Попробуй позже."
wait_message = "⏳ Ожидай, администратор скоро одобрит твою заявку!"
too_many_attempts_message = "⚠ Слишком много попыток, попробуй позже!"
enter_event_name_message = "✏ Укажи название мероприятия"
enter_role_name_message = "✏ Укажи название роли"

def event_message(roles, event):
    if not roles:
        return f"У события «{event.name}» пока нет ролей."

    message_lines = [f"Роли события «{event.name}»\n"]
    for role in roles:
        message_lines.append(f"• {role.name} — {role.points} балл(ов)")

    message = "\n".join(message_lines) + "\n\n" + "Участники:"
    
    return message

def user_info_message(user, role, event):
    return f"Мероприятие «{event.name}»\n\n{user.fullname}\n{user.course_number} курс\nГруппа {user.group_number}\n\nРоль: {role.name}\nБаллы: {role.points}"
        
def are_you_sure_to_delete_user_message(user, event, role):
    return f"Ты уверен, что хочешь удалить {user.fullname} | {role.name} с мероприятия «{event.name}»?"

def are_you_sure_to_delete_event_message(event):
    return "Ты уверен, что хочешь удалить мероприятие? У всех участников останутся баллы."


ENTER_EVENT_NAME_MESSAGE = "✏ Введи название события:"
EMPTY_EVENT_NAME_MESSAGE = "⚠ Название не может быть пустым. Попробуй снова:"
EVENT_ADDED_SUCCESS_MESSAGE = "✅ Событие «{name}» успешно добавлено."
EVENT_ADD_ERROR_MESSAGE = "❌ Ошибка при добавлении события. Попробуй позже."

NO_EVENTS_MESSAGE = "📭 Пока нет ни одного мероприятия."
ALL_EVENTS_MESSAGE = "📋 Список всех мероприятий:"

NO_EVENT_FOUND_MESSAGE = "⚠ Мероприятие не найдено."

CONFIRM_DELETE_EVENT_MESSAGE = "❗ Ты уверен, что хочешь удалить мероприятие «{name}»?"
EVENT_DELETED_SUCCESS_MESSAGE = "🗑 Мероприятие успешно удалено."
EVENT_DELETE_ERROR_MESSAGE = "❌ Ошибка при удалении мероприятия."

NO_EVENTS_FOR_ROLE_MESSAGE = "📭 Нет доступных событий. Сначала добавь хотя бы одно."
EVENTS_LIST_MESSAGE = "📋 Список доступных событий:\n{events}"
ENTER_EVENT_ID_MESSAGE = "✏ Введи ID события, к которому хочешь добавить роль:"

INVALID_EVENT_ID_MESSAGE = "⚠ Введи корректный числовой ID события."
EVENT_NOT_FOUND_MESSAGE = "❌ Событие с таким ID не найдено. Попробуй снова."

ENTER_ROLE_NAME_MESSAGE = "✏ Введи название роли:"
EMPTY_ROLE_NAME_MESSAGE = "⚠ Название роли не может быть пустым. Попробуй снова."

ENTER_ROLE_POINTS_MESSAGE = "✏ Введи количество очков для роли:"
INVALID_ROLE_POINTS_MESSAGE = "⚠ Введи корректное целое число для очков."

ROLE_ADDED_SUCCESS_MESSAGE = (
    "✅ Роль «{name}» для события (ID: {event_id}) с {points} очками успешно добавлена."
)
ROLE_ADD_ERROR_MESSAGE = "❌ Ошибка при добавлении роли. Попробуй снова."

USER_NOT_FOUND_MESSAGE = "❌ Пользователь не найден."
USER_DELETE_ERROR_MESSAGE = "⚠ Ошибка при удалении пользователя."
USER_DELETED_MESSAGE = "✅ Пользователь успешно удалён."

def your_points_message(date, points, events_info, rank_info):
    if points == 0:
        return "У тебя ещё нет баллов!"
    answer = (
        f"{date}\n\n🏆 Ранг: {rank_info[0]}\n"
        f"ℹ️ Баллов сейчас: {points}\n"
        + (f"ℹ️ Баллов до следующего: {rank_info[1]}\n" if rank_info[1] != -1 else "")
        + "\nТвои участия:\n"
    )
    for events_info_item in events_info:
        answer += str(events_info_item) + "\n"
    return answer

condition_message = """
*🔹🔷 Ранговая система ГФ 🔷🔹*
Твой прогресс имеет значение!

Каждая твоя активность, инициатива и вклад в движение приносят баллы, которые повышают твой ранг. Чем выше уровень — тем больше возможностей и признания в команде!  

*Как это работает?*
🔹 Баллы начисляются за участие в мероприятиях факультета, их организацию, а также за работу в медиа.  
🔹 Ранги обновляются автоматически — как только набираешь нужное количество баллов, получаешь новый статус.  
🔹 За переход на новый ранг активист получает особые призы в конце семестра.

Расти вместе с ГФ!
"""

ROLE_DELETED_SUCCESS_MESSAGE = "✅ Роль «{name}» (ID: {role_id}) успешно удалена."
ROLE_DELETE_ERROR_MESSAGE = "❌ Ошибка при удалении роли."

you_need_to_register_message = 'Ты не зарегистрирован! Напиши /start'
no_user_role_events_text = f'🔹 Ранг: нет\n🔹 Баллов: 0\n\nВы не зарегистрированы ни на одном мероприятии!'
def enter_event_message(events_len): return "🔹 Выбери мероприятие" if events_len>0 else 'Нет доступных мероприятий'  
def enter_role_message(roles_len): return "🔹 Выбери роль" if roles_len > 0 else 'Нет доступных ролей'  
enter_media_message = "🔹 Пришли своё фото с мероприятия. 1 фото (до 20 МБ)\n\nЕсли ты 'медиа' - отправь ссылку на свою работу!"
participation_added_message = '🔹 Участие добавлено!'
you_need_to_register_message = "❌ Чтобы редактировать профиль, необходимо зарегистрироваться!"
edit_profile_message_template = (
    "Имя: {fullname}\n"
    "Курс: {course}\n"
    "Группа: {group}\n\n"
    "🔹 Что хочешь изменить?"
)
ask_fullname_message = "Введи новое имя:"
fullname_updated_message = "‼️Нажми ✅ Сохранить изменения для обновления имени"
ask_course_message = "Введи новый номер курса:"
invalid_course_message = "Введи число!"
course_updated_message = "Но‼️Нажми ✅ Сохранить изменения для обновления номера курса"
ask_group_message = "Введи новый номер группы:"
group_updated_message = "‼️Нажми ✅ Сохранить изменения для обновления группы"
profile_updated_message = "🔹 Профиль успешно обновлён!"
no_changes_message = "Нет изменений для сохранения."