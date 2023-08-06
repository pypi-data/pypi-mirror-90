import requests


class XanderClient:

    def __init__(self, api, logger, server_address='35.192.211.33', server_port=5000):

        self.server_address = server_address

        self.server_port = server_port

        self.logger = logger

        if self.test_api_token(api=api):
            self.api = api
        else:
            raise ValueError('Log in failed!')

    def make_post_request(self, url, token, payload=None):
        payload = {} if payload is None else payload

        headers = {}
        if token:
            headers = {'Authorization': 'api_token {}'.format(token)}

        res = requests.post('http://{}:{}/{}'.format(self.server_address, self.server_port, url), json=payload,
                            headers=headers)

        if int(res.status_code) == 200:
            try:
                return True, res.json()
            except:
                return True, {'message': res.text}
        else:
            self.logger.error(message="Response code: {} while calling {}".format(res.status_code, url))

            return False, int(res.status_code)

    def test_api_token(self, api):
        result, payload = self.make_post_request(url='api/test_api_token', token=api['api_token'])

        if result:
            self.logger.info('You are logged as {} ({})'.format(api['user_name'], api['user_mail']))

        return result
