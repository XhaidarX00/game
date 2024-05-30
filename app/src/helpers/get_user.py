from app import ubot, OWNER_ID

async def get_users_(client, user_id):
    try:
        user = await client.get_users(user_id)
        return user
    except Exception as e:
        await client.send_message(OWNER_ID, e)
        return None