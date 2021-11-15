from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def group(self):
        return self.groups.first()

    @property
    def group_desc(self):
        return self.group.name if self.group else 'Sem Perfil'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def get_user_by_id(id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    @property
    def favorite_audiobooks(self):
        return [ favorite.audiobook for favorite in self.favorites.all() ]
