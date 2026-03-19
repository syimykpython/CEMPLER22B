from django.core.cache import cache

CONFIRM_CODE_TTL = 60 * 5  # 5 минут

def set_confirmation_code(user_id: int, code: str):
    key = f"confirm_code:{user_id}"
    cache.set(key, code, timeout=CONFIRM_CODE_TTL)

def get_confirmation_code(user_id: int):
    key = f"confirm_code:{user_id}"
    return cache.get(key)

def delete_confirmation_code(user_id: int):
    key = f"confirm_code:{user_id}"
    cache.delete(key)