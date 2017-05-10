import random
import string

import json

import requests

URL = 'https://node-01.faceapp.io'
USER_AGENT = 'FaceApp/1.0.229 (Linux; Android 4.4)'
DEVICE_ID = ''


class FaceApp:
    def __init__(self):
        global DEVICE_ID
        DEVICE_ID = self._gen()

    @staticmethod
    def _gen(size=8, chars=string.ascii_lowercase + string.digits):
        """
        this function generates a 8 chars string that will be used as DEVICE_ID
        """
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def get_code(fp):
        """
        get photo code
        :param fp: photo's file path
        :return: photo code
        """
        if fp:
            with open(fp, 'rb') as p:
                r = requests.post(URL + '/api/v2.3/photos', files={'file': p},
                                  headers={'User-Agent': USER_AGENT, 'X-FaceApp-DeviceID': DEVICE_ID})
                rb = json.loads(json.dumps(r.json()))

                if r.status_code not in [200, 201, 202]:
                    return "Error: {}\nDescription:{}".format(rb['err'], rb['err']['desc'])

                else:
                    return rb['code']
        return 'wot'

    @staticmethod
    def make_img(code, filter_name):
        """
        Apply filter to the image
        :param code: the photo code you can get with get_code
        :param filter_name: the filter you want to apply
        :return: byte image
        """

        if filter_name in ['smile', 'smile_2', 'hot', 'old', 'young', 'female', 'male']:
            req = requests.get(URL + '/api/v2.3/photos/{}/filters/{}?cropped=true'.format(code, filter_name),
                               headers={'User-Agent': USER_AGENT, 'X-FaceApp-DeviceID': DEVICE_ID})

            if req.status_code == 200:
                req.raw.decode_content = True
                content = req.content
                return content

            else:
                return 'Error ' + str(req.status_code)
        return 'invalid filter'
