from django.db import models


class SystemFromEmailAddress(models.Model):
    email = models.EmailField()
    from_official_name = models.CharField(
        max_length=255,
        help_text="This is the text that it gets displayed when "
                  "viewing the email from the email list on your email client."
    )
    code_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "System From Email Address"
        verbose_name_plural = "System From Email Address"

    def __str__(self):
        return "{}".format(self.email)


class EmailNotificationRecipient(models.Model):
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "Email Notification Recipients"

    def __str__(self):
        return "{}".format(self.email)


class EmailTemplate(models.Model):
    code_name = models.CharField(max_length=255)
    from_official_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    plain_body = models.TextField()
    html_body = models.TextField()

    def __str__(self):
        return "{}".format(self.code_name)


class GmailConnectionToken(models.Model):
    json_string = models.TextField()
    valid = models.BooleanField()
    gmail_address = models.EmailField()

    def __str__(self):
        return self.gmail_address
