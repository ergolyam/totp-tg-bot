import tortoise.models
from tortoise import fields


class Totp(tortoise.models.Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True)
    totp_key = fields.CharField(max_length=128, null=False)
    class Meta(tortoise.models.Model.Meta):
        table = "user_totp"


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
