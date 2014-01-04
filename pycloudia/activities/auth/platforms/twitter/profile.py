from pycloudia.activities.auth.platforms.interfaces import IProfile


class Profile(IProfile):
    def __init__(self, info):
        self.info = info

    @property
    def user_id(self):
        return super(Profile, self).user_id()

    def email(self):
        return super(Profile, self).email()

    def avatar(self):
        return super(Profile, self).avatar()

    def birthday(self):
        return super(Profile, self).birthday()

    def name(self):
        return super(Profile, self).name()
