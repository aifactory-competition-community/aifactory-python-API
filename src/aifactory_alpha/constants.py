SUBMISSION_DEFAULT_URL = 'release.aifactory.solutions'


# Authentication method
class AUTH_METHOD:
    USERINFO = 0
    TOKEN = 1


class DEBUGGING_PARAMETERS:
    TOKEN = "DEBUGGING_TOKEN"


class SUBMIT_RESULT:
    FAIL_TO_SUBMIT = 0
    SUBMIT_SUCCESS = 200


class SubmitTokenNotFoundError(Exception):
    ment = "You have to either set AIF_TOKEN environment variable \n \
                or put your submission token as a parameter."
    def __str__(self):
        return self.ment


class UserInfoNotDefinedError(Exception):
    ment = "You must provide `email` or `user_id` to submit your result."
    def __str__(self):
        return self.ment


class TaskIDNotDefinedError(Exception):
    ment = "You must provide `task_id` to submit your result."
    def __str__(self):
        return self.ment


class WrongAuthMethodError(Exception):
    ment = "Wrong Authentification Method. Method should be either AUTH_METHOD.USERINFO or AUTH_METHOD.TOKEN."
    def __str__(self):
        return self.ment


class AuthentificationNotValidError(Exception):
    ment="Information for authentification not enough."
    def __str__(self):
        return self.ment

