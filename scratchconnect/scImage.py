"""
ScratchConnect Image Class
"""

import requests
from PIL import Image as pyImage
from scratchconnect.scOnlineIDE import _change_request_url

_scratch_api = "https://api.scratch.mit.edu/"


class Image:
    def __init__(self, online_ide):
        self.length = []
        self._image_size = None
        self.image_success = None
        self.name = None
        if online_ide:
            _change_request_url()

    def _shorten_code(self, r, g, b):
        """
        Don't use this
        """
        decimal = str((r * 256 * 256) + (g * 256) + b)
        code = ("0" * (8 - len(decimal))) + str(decimal)
        return code

    def download_image(self, url, name):
        """
        Download the image
        """
        self.name = name
        try:
            response = requests.get(url).content
            with open(f"{self.name}.png", 'wb') as file:
                file.write(response)
            self.image_success = True
        except:
            self.image_success = False

    def resize_image(self, size, name, maintain_aspect_ratio=True):
        """
        Resize the given image
        :param size: The size (in tuple format)
        :param name: The new name of the image you want to save
        :param maintain_aspect_ratio: Set it to "True" if you want to maintain the aspect ratio of the image while resizing
        """
        image = pyImage.open(f"{self.name}.png")
        if maintain_aspect_ratio:
            image.thumbnail(size)
            image.save(f"{name}.png")
        else:
            new_image = image.resize(size)
            new_image.save(f"{name}.png")
        self.name = name

    def get_user_image(self, query, size=32, name="scImage"):
        """
        Get the image of a user on Scratch
        """
        user_id = requests.get(f"{_scratch_api}users/{query}").json()["id"]
        url = f"https://cdn2.scratch.mit.edu/get_image/user/{user_id}_{size}x{size}.png?v="
        self.download_image(url, name)

    def get_studio_image(self, studio_id, name="scImage"):
        """
        Get the image of a studio on Scratch
        """
        url = f"https://uploads.scratch.mit.edu/get_image/gallery/{studio_id}_170x100.png"
        self.download_image(url, name)

    def get_project_image(self, project_id, size=32, name="scImage"):
        """
        Get the image of a project on Scratch
        """
        url = f"https://uploads.scratch.mit.edu/get_image/project/{project_id}_{size}x{size}.png"
        self.download_image(url, name)

    def encode_image(self):
        """
        Encode the image data to numbers. Use the function get_data() to get the encoded data
        """
        try:
            if self.image_success in [False, None]:
                return False
            image = pyImage.open(f"{self.name}.png").convert('RGBA')

            # Making the transparent background of the image white rather than black
            background = pyImage.new('RGBA', image.size, (255, 255, 255))
            alpha_composite = pyImage.alpha_composite(background, image)
            alpha_composite.save(f"{self.name}.png", 'PNG')

            image = pyImage.open(f"{self.name}.png").convert('RGBA')
            self._image_size = image.size
            try:
                is_animated = image.is_animated
            except:
                is_animated = False
            if is_animated:
                image.seek(0)
                self._image_size = image.size
                frame = image.convert("RGB").getdata()
                image_data = list(frame)
            else:
                image_data = list(image.convert("RGB").getdata())
            hex_values = ""
            for pixel_color in image_data:
                hex_values += self._shorten_code(pixel_color[0], pixel_color[1], pixel_color[2])
            self.hex_values = hex_values
            return True
        except Exception as E:
            print(E)
            return None

    def get_image_data(self):
        """
        Get the encoded image data
        """
        return self.hex_values

    def get_size(self):
        """
        Get the size of the image
        """
        return self._image_size
