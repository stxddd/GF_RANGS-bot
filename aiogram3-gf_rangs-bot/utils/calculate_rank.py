from bot.db.users.dao import UserDAO

async def get_rank_and_remaining(user_id):
    points = await UserDAO.get_total_points_by_user_id(user_id)
    
    if points < 40: return [0, 40-points]
    elif points >= 40 and points < 70: return [1, 70-points]
    elif points >= 70 and points < 100: return [2, 100-points]
    elif points >= 100 and points < 160: return [3, 160-points]
    elif points >= 160 and points < 200: return [4, 200-points]
    elif points >= 200 : return [5,-1]

