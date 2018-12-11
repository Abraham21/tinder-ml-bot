import robobrowser
import re


class UserAgent:
    class Mobile:
        class iOS:
            safari = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A356 Safari/604.1'

class Facebook:

    AUTHAPP_FORM_ACTION = '/v2.8/dialog/oauth/confirm'
    AUTH_URL = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"

    def __init__(self, username, password, user_agent=None):
        self.username = username
        self.password = password

        self.user_agent = user_agent
        if not self.user_agent:
            self.user_agent = UserAgent.Mobile.iOS.safari

        self.browser = robobrowser.RoboBrowser(user_agent=self.user_agent, parser="lxml")

    def get_access_token(self):        
        self.browser.open(self.AUTH_URL)

        # Authentication
        login_form = self.browser.get_form()
        login_form["pass"] = self.password
        login_form["email"] = self.username
        self.browser.submit_form(login_form)

        # Authorizing App
        authapp_form = self.browser.get_form(action=self.AUTHAPP_FORM_ACTION)
        if authapp_form.submit_fields.get('__CONFIRM__'):
            self.browser.submit_form(authapp_form, submit=authapp_form.submit_fields['__CONFIRM__'])
        else:
            raise Exception("Couldn't find the continue button. Maybe you supplied the wrong login credentials? Or maybe Facebook is asking a security question?")
        self.access_token = re.search(r"access_token=([\w\d]+)", self.browser.response.content.decode()).groups()[0]
        return self.access_token

if __name__ == '__main__':
    username = 'USERNAME_HERE'
    password = 'PASSWORD_HERE'
    facebook = Facebook(username, password)
    print(facebook.get_access_token())
