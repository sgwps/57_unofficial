from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

# EMAIL TOKENS ( HOW THEY WORK - I DON'T REALLY KNOW )


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )


account_activation_token = TokenGenerator()