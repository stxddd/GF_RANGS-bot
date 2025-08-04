from config import settings

def check_admin_tg_id(tg_id):
    return str(tg_id) in str(settings.ADMIN_TG_IDS).split(',')