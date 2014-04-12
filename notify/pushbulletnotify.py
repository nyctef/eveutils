from pushbullet import PushBullet

class PushBulletNotify(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.pb = PushBullet(api_key)
        self.pb.reload_devices() # TODO is this needed?

    def send(self, title, text):
        for device in self.pb.devices:
            device.push_note(title, text)
 
