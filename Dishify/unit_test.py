import unittest

image_uri = 'https://weelicious.com/imager/weelicious_com/wp-content/uploads/2012/09/blueberrypancakes-book-spread_1b74faffbe944b0675f0e20473d3ad34.jpg'
api_call = f"https://3z6kv0n0v6.execute-api.us-east-2.amazonaws.com/test/dishify?imageURL={image_uri}"


class TestImageUrl(unittest.TestCase):

    def test_path(self):
        """
        Checks if user is addressing the correct function
        """
        self.assertTrue('/dishify' in api_call)

    def test_is_image_extension(self):
        """
        Checks if the URI ends in an image extension
        """
        image_extensions = ['JPEG', 'JPG', 'PNG', 'PNG8', 'PNG24', 'GIF', 'BMP', 'WEBP', 'RAW', 'ICO', 'PDF', 'TIFF']
        any_in = lambda image_extensions, image_uri: any(i in image_uri for i in image_extensions)
        self.assertTrue(any_in)


if __name__ == '__main__':
    unittest.main()