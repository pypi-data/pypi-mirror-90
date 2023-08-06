from ..interfaces.ISource import ISource
import cv2

class DeviceStream(ISource):

    def __init__(self, device_id):

        super().__init__()
        self.device_id = device_id
        self.cap = cv2.VideoCapture(device_id)

