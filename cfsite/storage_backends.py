import base64

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# class StaticStorage(S3Boto3Storage):
#     location = settings.AWS_STATIC_LOCATION


# class PublicMediaStorage(S3Boto3Storage):
#     location = settings.AWS_PUBLIC_MEDIA_LOCATION
#     file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

    def get_valid_name(self, name):
        name_bytes = bytearray(name, 'utf-8')
        encoded_name = base64.urlsafe_b64encode(name_bytes)
        return super(PrivateMediaStorage, self).get_valid_name(encoded_name.decode('ascii'))
        # return encoded_name.decode('ascii')
