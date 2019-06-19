from pathlib import Path

from OpenGL.GL import glGetIntegerv, GL_MAX_TEXTURE_SIZE, glGenTextures, glBindTexture, GL_TEXTURE_2D, glTexImage2D, \
    GL_UNSIGNED_BYTE, GL_RGBA, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR, \
    glGenerateMipmap, glTexParameteri, glPixelStorei, GL_UNPACK_ALIGNMENT, \
    GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE, glTexParameterf
from PIL import Image as pilImage
from PIL.Image import FLIP_TOP_BOTTOM
from numpy import fromstring, uint8

from cc._constant import LOGGER
from cc._util import get_ccircle_image_path


class Image:
    """ Load an image into a 2D OpenGL texture using PIL. """

    def __init__(self, path: str):
        """ Create an image given a path relative to the ccircle directory. """
        resolved_path = get_ccircle_image_path(path)
        self.name = resolved_path.name
        self.id = Image.__to_texture(resolved_path)
        pass

    def __eq__(self, other):
        """ Two textures are equal if they share the same OpenGL-assigned id."""
        return self.id == other.id

    @staticmethod
    def __max_texture_size():
        """ Get the max texture size (n x n) that this GPU supports. """
        n = glGetIntegerv(GL_MAX_TEXTURE_SIZE)
        return n

    @staticmethod
    def __to_texture(path: Path):
        """ Convert img (BMP, IM, JPEG, PNG, etc.) to an OpenGL texture.

        Args:
            path: a pathlib.Path object--the path to the image.

        Returns:
            texture_id: the id of the texture loaded into OpenGL.

        Notes:
            Verifies image dimensions and ensures there is space for another texture in OpenGL.
        """
        try:
            img = pilImage.open(path)
        except IOError as ex:
            LOGGER.critical('Failed to open image file at %s: %s' % (path, str(ex)))
            raise

        # Verify the image size/channels are supported.
        width, height = img.size
        max_dimension = Image.__max_texture_size()
        if width > max_dimension or height > max_dimension:
            raise RuntimeError('Image dimensions must be < %s.' % max_dimension)

        # Transpose the image and convert to RGBA.
        img_data = img.transpose(FLIP_TOP_BOTTOM).convert('RGBA')
        img_data = fromstring(img_data.tobytes(), uint8)

        # Bind the image data to an OpenGL texture.
        texture_id = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        # Stretch texture; mipmaps for minification; clamp.
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            img_data
        )
        glGenerateMipmap(GL_TEXTURE_2D)

        LOGGER.debug('Loaded %dx%d image: %s' % (width, height, path.name))
        img.close()

        return texture_id
