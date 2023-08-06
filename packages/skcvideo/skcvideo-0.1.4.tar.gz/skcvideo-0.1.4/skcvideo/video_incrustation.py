import cv2


class VideoIncrustation(object):
    def __init__(self, box=[0, 575, 720, 575 + 1280]):
        self.box = box

    def build(self, *args, **kwargs):
        pass

    def incrust_image(self, big_image, image):
        y1, x1, y2, x2 = self.box
        box_height, box_width = y2 - y1, x2 - x1
        im_height, im_width = image.shape[:2]
        if im_height != box_height or im_width != box_width:
            image = cv2.resize(image, (box_width, box_height))
        big_image[y1:y2, x1:x2, :] = image

    def refresh(self, big_image, image):
        self.incrust_image(big_image, image)
