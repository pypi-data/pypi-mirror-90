==============
MyCustomMailer
==============

Polls is a Django app to conduct Web-based polls. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "mcmailer" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mcmailer',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('mcmailer/', include('mcmailer.urls')),

3. Run ``python manage.py migrate`` to create the mcmailer models.

4. In the settings.py you must declare the following four settings::

    JSON_PATH = "/my/path/to/client_secret.json"
    LOCAL_HOST = True
    LOCAL_HOST_REDIRECT_URI = "http://localhost:8000/mcmailer/g-auth-endpoint/"
    PRODUCTION_REDIRECT_URI = "https://example.com/mcmailer/g-auth-endpoint/"

5. The JSON_PATH setting is the path that the 'credentials.json' will be located.The credentials.json is the file that Gmail API will give you when you create a project in the console and enable the Gmail API. Go to https://developers.google.com/gmail/api/quickstart/python and follow the step 1 to create a project and enable the Gmail API in the console.cloud.google.com, when you finish, download the credentials.json put it somewhere in your project and write the path of it in the JSON_PATH variable in your settings.py. Example: JSON_PATH = os.path.join(os.getcwd(), "mcmailer", "clientjson", "client_secret.json")

6. The LOCAL_HOST settings is a boolean variable that should be True if you are on localhost and False when you are in production.

7. The LOCAL_HOST_REDIRECT_URI setting is one (or the only one) of the Authorized redirect URIs that you will put in your credentials in the console.cloud.google.com. This URI will be used if the LOCAL_HOST is equal to True. The URI must point to a specific view so just change the part (if needed) before the /mcmailer/g-auth-endpoint/. Example: LOCAL_HOST_REDIRECT_URI = "http://localhost:8000/mcmailer/g-auth-endpoint/"

8. The PRODUCTION_REDIRECT_URI setting is one (or the only one) of the Authorized redirect URIs that you will put in your credentials in the console.cloud.google.com. This URI will be used if the LOCAL_HOST is equal to False. The URI must point to a specific view so just change the part (if needed) before the /mcmailer/g-auth-endpoint/. Example: LOCAL_HOST_REDIRECT_URI = "https://example.com/mcmailer/g-auth-endpoint/"
    * If your app doesn't need to authenticate new users on production and you only need to authenticate your own Gmail to sent emails programmatically then you can just authenticate your Gmail locally once and leave the LOCAL_HOST variable to False and don't declare the PRODUCTION_REDIRECT_URI variable in your settings.py.

9. Start the development server and visit http://127.0.0.1:8000/mcmailer/connect/
   to start the registration of a new Gmail