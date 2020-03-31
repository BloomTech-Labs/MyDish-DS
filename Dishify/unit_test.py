import unittest

image_uri = 'https://images-na.ssl-images-amazon.com/images/I/81%2B1uNsyR0L.jpg'
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
        test = False
        for i in image_extensions:
            if i.lower() in image_uri:
                test = True
        self.assertTrue(test)


if __name__ == '__main__':
    unittest.main()