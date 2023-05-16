"""
# The main function is to transform the picture bed from the original one to the new one.
# Created by: Sun Zhu, 2023-05-02, version 0.0

"""
# ///////// IMPORT /////////
# ======== Standard Lib ========
import os
# ======== Third-Party Lib ========
import oss2  # Third-Party Lib of aliyun oss
import urllib.request
# ======== Local Lib ========
# Load the custom config file if the config file exists
if os.path.exists("config_private.py"):
    from config_private import *
else:
    from config import *

# ////////// CONFIG //////////
# ======== cache ========
# The cache folder for the picture bed transformer
cache_folder = "cache"



# ////////// CLASS //////////
class PicBedTransformer:
    """
    The factory class of the pic_bed_transformer.
    """
    def __init__(self, mode="aliyun_oss"):
        self.mode = mode
        if self.mode == "aliyun_oss":
            self.pic_bed_transformer = PicBedTransformer_AliyunOSS()
        else:
            self.pic_bed_transformer = None
            raise NotImplementedError("The mode %s is not implemented." % self.mode)

    def transform(self, orignial_url, local_file_path):
        """
        Transform the picture bed from the original one to the new one.
        :param local_file_path:
        :return:
        """
        # # The transoform process can be divided into two steps:
        # # 1. Download the picture from the original picture bed.
        # # Save the file via urllib.request.urlretrieve(url, local_file_path)
        urllib.request.urlretrieve(orignial_url, local_file_path)

        # 2. Upload the picture to the new picture bed.
        new_url = self.pic_bed_transformer.upload(local_file_path)

        return new_url

class PicBedTransformer_AliyunOSS():
    """
    # Transform the picture bed from the original one to aliyun oss.
    :return:
    """
    def __init__(self,
                 access_key_id=aliyun_oss_access_key_id,
                 access_key_secret=aliyun_oss_access_key_secret,
                 endpoint=aliyun_oss_endpoint,
                 bucket_name=aliyun_oss_bucket_name,
                 file_path_prefix=aliyun_oss_file_path_prefix):
        # Aliyun OSS settings
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        self.file_path_prefix = file_path_prefix

        # Create the bucket
        self.bucket = oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret), self.endpoint, self.bucket_name)

    def upload(self, local_file_path):
        """
        Upload the local file to the remote file path.
        :param local_file_path:
        :param remote_file_path:
        :return:
        """
        filename = os.path.split(local_file_path)[-1]
        remote_file_path = self.file_path_prefix + filename
        self.bucket.put_object_from_file(remote_file_path, local_file_path)
        # # http_link = "https://" + pic_bed_transformer_aliyun_oss.bucket_name + "." + pic_bed_transformer_aliyun_oss.endpoint + "/" + pic_bed_transformer_aliyun_oss.file_path_prefix + "test230515.png"
        http_link = "https://" + self.bucket_name + "." + self.endpoint + "/" + remote_file_path
        return http_link

    def download(self, remote_file_path, local_file_path):
        """
        Download the remote file to the local file path.
        :param remote_file_path:
        :param local_file_path:
        :return:
        """
        self.bucket.get_object_to_file(remote_file_path, local_file_path)

# ////////// UTILS //////////

# ///////// TEST CASE ////////
# Test the class PicBedTransformer_AliyunOSS
def test_PicBedTransformer_AliyunOSS():
    """
    Test the class PicBedTransformer_AliyunOSS.
    Upload a file to the aliyun oss, and then download it.
    :return:
    """

    # Define the file to upload
    file_to_upload = r"C:\Users\hp\Desktop\test230515.png"
    filepath_root, filename = os.path.split(file_to_upload)
    filepath_save_root, filename_save = filepath_root, filename.split(".")[0] + "_bak." + filename.split(".")[-1]

    # Create the object
    pic_bed_transformer_aliyun_oss = PicBedTransformer_AliyunOSS()

    # Upload the file
    http_link = pic_bed_transformer_aliyun_oss.upload(file_to_upload)

    # Download the file
    pic_bed_transformer_aliyun_oss.download(aliyun_oss_file_path_prefix+filename, os.path.join(filepath_save_root, filename_save))

    # Get the http link
    # http_link = "https://" + pic_bed_transformer_aliyun_oss.bucket_name + "." + pic_bed_transformer_aliyun_oss.endpoint + "/" + pic_bed_transformer_aliyun_oss.file_path_prefix + "test230515.png"
    print("test_PicBedTransformer_AliyunOSS() passed!")
    print("http_link = " + http_link)

# Test the class PicBedTransformer
def test_PicBedTransformer():
    """
    Test the class PicBedTransformer.
    Step 1: Download the picture from the original picture bed.
    Step 2: Upload the picture to the new picture bed.
    :return:
    """
    # Define the url of the picture to download
    url = "https://p1.itc.cn/images01/20230513/32332e82a60f44329b80335cba950ad8.jpeg"

    # Parse the url to get the filename
    filename = url.split("/")[-1]

    # Define the local file path to save the picture
    local_file_path = os.path.join(cache_folder, filename)

    # Create the object
    pic_bed_transformer = PicBedTransformer(mode="aliyun_oss")

    # Transform the picture bed
    new_url = pic_bed_transformer.transform(url, local_file_path)

    print("test_PicBedTransformer() passed!")
    print("new_url = " + new_url)

    pass



if __name__=="__main__":
    # # ======== Test Case 1: PicBedTransformer_AliyunOSS ========
    # test_PicBedTransformer_AliyunOSS()    # Passed

    # # ======== Test Case 2: PicBedTransformer ========
    test_PicBedTransformer()
    pass