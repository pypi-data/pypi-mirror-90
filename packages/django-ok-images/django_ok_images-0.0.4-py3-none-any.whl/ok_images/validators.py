# stolen from https://github.com/codingjoe/django-stdimage/blob/master/stdimage/validators.py

from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _
from PIL import Image

__all__ = (
    'BaseSizeValidator',
    'MinSizeValidator',
    'MaxSizeValidator'
)


class BaseSizeValidator(BaseValidator):
    """Base validator that validates the size of an image."""

    def __init__(self, width, height):
        self.limit_value = width or float('inf'), height or float('inf')

    def __call__(self, value):
        cleaned = self.clean(value)

        if self.compare(cleaned, self.limit_value):
            params = {
                'width': self.limit_value[0],
                'height': self.limit_value[1],
            }

            raise ValidationError(
                self.message,
                code=self.code,
                params=params
            )

    def compare(self, a, b):
        return True

    def clean(self, value):
        value.seek(0)
        stream = BytesIO(value.read())
        size = Image.open(stream).size
        value.seek(0)
        return size


class MaxSizeValidator(BaseSizeValidator):
    """
    ImageField validator to validate the max width and height of an image.
    You may use None as an infinite boundary.

    image2 = StdImageField(validators=[MaxSizeValidator(1028, 768)])
    """
    code = 'max_resolution'
    message = _(
        'The image you uploaded is too large.'
        ' The required maximum resolution is:'
        ' %(width)sx%(height)s px.'
    )

    def compare(self, img_size, max_size):
        return img_size[0] > max_size[0] or img_size[1] > max_size[1]


class MinSizeValidator(BaseSizeValidator):
    """
    ImageField validator to validate the min width and height of an image.
    You may use None as an infinite boundary.

    image1 = StdImageField(validators=[MinSizeValidator(800, 600)])

    """
    message = _(
        'The image you uploaded is too small.'
        ' The required minimum resolution is:'
        ' %(width)sx%(height)s px.'
    )

    def compare(self, img_size, min_size):
        return img_size[0] < min_size[0] or img_size[1] < min_size[1]

