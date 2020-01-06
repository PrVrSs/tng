import functools


def requires_auth(f):

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        bot, update, auth = args
        print(update.from_user.id)
        print(update.from_user.username)

        return f(*args, **kwargs)

    return wrapper
