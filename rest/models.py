""" Module where the models are defined """

from django.db import models

from common.crypto import ec_secp256k1 as crypto


class KeyField(models.CharField):
    """ Field for user keys/IDs """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = crypto.SERIALIZED_KEY_LENGTH
        super().__init__(*args, **kwargs)


class SignatureField(models.CharField):
    """ Field for signatures """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 256
        super().__init__(*args, **kwargs)


class Group(models.Model):
    """ Model for groups """
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Group(id={self.id} name={self.name})"


class User(models.Model):
    """ Model for registered users """
    id = KeyField(primary_key=True)
    email = models.EmailField(max_length=256)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    # Do not use ForeignKey because we want to keep invitee ID event if he leaves
    invited_by = KeyField()
    payload = models.CharField(max_length=1024)
    invitee_signature = SignatureField()
    user_signature = SignatureField()

    def __str__(self):
        return self.email

    def __repr__(self):
        return f"User(id={self.id} email={self.email} group={self.group.id})"
