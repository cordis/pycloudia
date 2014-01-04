from abc import ABCMeta, abstractmethod


class IService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def authenticate(self, client_id, platform, access_token):
        """
        :type client_id: C{str}
        :type platform: C{str}
        :type access_token: C{str}
        :return: Tuple of (user_id, package)
        :rtype: (C{str}, L{pycloudia.packages.interfaces.IPackage})
        :raise: L{pycloudia.activities.auth.exceptions.AuthError}
        """


class IDao(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_or_create_user(self, platform, profile):
        """
        :type platform: C{str}
        :type profile: L{pycloudia.activities.auth.platforms.interfaces.IProfile}
        :return: Tuple of (user_id, created)
        :rtype: (C{str}, C{boolean})
        """

    @abstractmethod
    def set_user_friends(self, user_id, platform, profile_list):
        """
        :type user_id: C{str}
        :type platform: C{str}
        :type profile_list: C{list} of L{pycloudia.activities.auth.platforms.interfaces.IProfile}
        """
