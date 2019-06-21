#import os
import boto3

#from .render import render_attachment_setup_pattern


# s3_client = boto3.client('s3')
# s3_resource = boto3.resource('s3')


# def download_dir(prefix, local=local, bucket=bucket,
#                  client=s3_client, resource=s3_resource):
#     keys = []
#     dirs = []
#     next_token = ''
#     base_kwargs = {
#         'Bucket': bucket,
#         'Prefix': prefix,
#     }
#     while next_token is not None:
#         kwargs = base_kwargs.copy()
#         if next_token != '':
#             kwargs.update({'ContinuationToken': next_token})
#         results = s3_client.list_objects_v2(**kwargs)
#         contents = results.get('Contents')
#         for i in contents:
#             k = i.get('Key')
#             if k[-1] != '/':
#                 keys.append(k)
#             else:
#                 dirs.append(k)
#         next_token = results.get('NextContinuationToken')
#     for d in dirs:
#         dest_pathname = os.path.join(local, d)
#         if not os.path.exists(os.path.dirname(dest_pathname)):
#             os.makedirs(os.path.dirname(dest_pathname))
#     for k in keys:
#         dest_pathname = os.path.join(local, k)
#         if not os.path.exists(os.path.dirname(dest_pathname)):
#             os.makedirs(os.path.dirname(dest_pathname))
#         resource.meta.client.download_file(bucket, k, dest_pathname)


def get_session(auth):
    return boto3.Session(**auth)
