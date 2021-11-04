from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def group(self):
        group = self.groups.first()
        return group.name if group else 'Sem perfil'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
