from aifactory_alpha.Authentification import AFCrypto
from datetime import datetime
from aifactory_alpha.constants import *
import logging
import os
import requests
import http
import json


class AFContest:
    _summary_ = None
    logger = None
    auth_method = None
    user_token = None
    auth_token = None
    user_id = None
    user_email = None
    task_id = None
    model_name_prefix = None
    encrypt_mode = None
    def __init__(self, auth_method=AUTH_METHOD.USERINFO, user_token=None,
                 user_id=None, user_email=None, model_name_prefix=None, task_id=None,
                 log_dir="./log/", debug=False, encrypt_mode=True,
                 submit_url=SUBMISSION_DEFAULT_URL, auth_url=AUTH_DEFAULT_URL):
        self.set_log_dir(log_dir)
        self.auth_method = auth_method
        self.debug = debug
        self.submit_url = submit_url
        self.auth_url = auth_url
        if auth_method==AUTH_METHOD.TOKEN:
            if debug:
                user_token = DEBUGGING_PARAMETERS.TOKEN
            self.set_token(user_token)
            raise(AuthMethodNotAvailableError)
        elif auth_method==AUTH_METHOD.USERINFO:
            self.set_user_id(user_id)
            self.set_user_email(user_email)
            self.set_task_id(task_id)
            self.set_model_name_prefix(model_name_prefix)
        else:
            raise(WrongAuthMethodError)
        if encrypt_mode:
            self.crypt = AFCrypto()

    def set_log_dir(self, log_dir: str):
        self.log_dir = os.path.abspath(log_dir)
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        if not os.path.isdir(self.log_dir):
            raise AssertionError("{} is not a directory.".format(self.log_dir))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(module)s:%(levelname)s: %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def set_token(self, token=None, yes=False):
        token_in_env_var = os.getenv('AF_REFRESH_TOKEN')
        if token_in_env_var is not None:
            if token is not None and (token_in_env_var != token):
                if not yes:
                    print("It will replace your token in the environment variable `AF_REFRESH_TOKEN`.")
                    res = input("Do you want to proceed? [Y/N] - default: Y")
                    if res == 'N':
                        print("Using token from the environment variable `AF_REFRESH_TOKEN`.")
                        token = token_in_env_var
                else:
                    token = token_in_env_var
        self.user_token = user_token

    def set_user_email(self, email: str):
        self.user_email = email
        if self.user_id is None:
            self.user_id == self.user_email.split("@")[0]

    def set_user_id(self, id: str):
        self.user_id = id

    def set_task_id(self, task_id: int):
        self.task_id = task_id

    def set_model_name_prefix(self, model_name_prefix: str):
        self.model_name_prefix = model_name_prefix

    def reset_logger(self, prefix=LOG_TYPE.SUBMISSION):
        cur_log_file_name = prefix+datetime.now().__str__().replace(" ", "-").replace(":", "-").split(".")[0]+".log"
        log_path = os.path.join(self.log_dir, cur_log_file_name)
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s:%(module)s:%(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.log_path = log_path

    def _investigate_validation_(self):
        res = []
        if self.auth_method == AUTH_METHOD.TOKEN:
            if self.token is None:
                res.append(SubmitTokenNotFoundError)
        elif self.auth_method == AUTH_METHOD.USERINFO:
            if self.user_id is None and self.user_email is None:
                res.append(UserInfoNotDefinedError)
            if self.task_id is None:
                res.append(TaskIDNotDefinedError)
        else:
            res = res.append(WrongAuthMethodError)
        for r in res:
            self.logger.error(r.ment)
        return res

    def _require_password_(self):
        self.password = None
        if self.debug:
            self.password = DEBUGGING_PARAMETERS.PASSWORD
        else:
            self.password = input("Please put your password: ")
        self.hashed_password = self.crypt.encrypt_hash(self.password)
        return self.hashed_password

    def _is_token_valid_(self):
        return False

    def _user_info_auth_(self, num_trial=0):
        # ask for the token to the auth server.
        hashed_password = self._require_password_()
        if self.encrypt_mode:
            hashed_password = self.crypt(hashed_password, self.user_id)
        params = {'password': hashed_password, 'auth_method': self.auth_method,
                  'task_id': self.task_id, 'user_id': self.user_id,
                  'password_encrypted': self.encrypt_mode}
        response = requests.get(self.auth_url+'/token', params=params)
        tokens = json.loads(response.text)
        if response.status_code == http.HTTPStatus.OK:
            self.logger.info('Authentification process success.')
            self.logger.info('Response from auth server: {}'.format(response))
            self.auth_token = self.crypt.decrypt_aes(tokens['token'], self.user_id)
            return True
        else:
            if num_trial > AUTH_METHOD.MAX_TRIAL:
                return False
            self.logger.info('Authentification failed. Please try again with another password.')
            self.logger.info('Please check you have the right password that you use to log-in the AI Factory Website.')
            return self._user_info_auth_(num_trial+1)

    def _send_submssion_(self, submit_url=SUBMISSION_DEFAULT_URL):
        params = {'token': self.auth_token}
        response = requests.get(submit_url+'/token', params=params)
        print(response.text)

    def submit(self, file):
        # This method submit the answer file to the server.
        def _fail_(self, _status_):
            self.logger.error("Submission Failed.")
            print("Please have a look at the logs in '{}' for more details.".format(self.log_path))
            return _status_
        def _succeed_(self, _status_):
            self.logger.info("Submission was successful.")
            print("Results are recorded in the log file '{}'.".format(self.log_path))
            return _status_
        self.reset_logger(LOG_TYPE.SUBMISSION)
        status = SUBMIT_RESULT.FAIL_TO_SUBMIT
        if not os.path.exists(file):
            self.logger.error("File {} not found.".format(file))
            return status
        if not ((self.auth_token is not None) and (self._is_token_valid_())):
            res = self._investigate_validation_()
            if len(res) != 0:
                return _fail_(self, status, log_path)
            if not self._user_info_auth_():
                return _fail_(self, status)
        self._send_submssion_()
        status = SUBMIT_RESULT.SUBMIT_SUCCESS
        return _succeed_(self, status)


    def release(self):
        # This method submit the answer file and the code to the server.
        pass

    def summary(self):
        _summary_ = ">>> Contest Information <<<\n"
        _summary_ += "Authentification Method:"
        if self.auth_method is AUTH_METHOD.TOKEN:
            _summary_ += "Token \n"
            _summary_ += "    Token: {} \n".format(self.user_token)
        elif self.auth_method is AUTH_METHOD.USERINFO:
            _summary_ += "User Information \n"
            _summary_ += "    Task ID: {}\n".format(self.task_id)
            _summary_ += "    User ID: {}\n".format(self.user_id)
            _summary_ += "    User e-mail: {}\n".format(self.user_email)
        if self.model_name_prefix is not None:
            _summary_ += "Model Name Prefix: {}\n".format(self.model_name_prefix)
        return _summary_


if __name__ == "__main__":
    c = AFContest(user_id='user0', task_id='3000', debug=True)
    c.summary()
    c.submit('./sample_data/sample_answer.csv')