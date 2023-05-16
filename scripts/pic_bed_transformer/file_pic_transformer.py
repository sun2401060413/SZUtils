"""
Process the picture in the markdown file and upload it to the picture bed, then replace the original url with the new url.
"""

# ///////// IMPORT /////////

# ======== Standard Lib ========
import os
import re
import time
import urllib.request
# ======== Third-Party Lib ========

# ======== Local Lib ========
import pic_bed_transformer
# ///////// CONFIG /////////
# The root folder of saving the pictures
cache = "cache"
# The root folder of saving the new documents
output = "output"



# ///////// CLASS /////////
class FilePicTransformer:
    def __init__(self, mode="aliyun_oss", cache_folder=cache, output_folder=output):
        self.pic_bed_transformer = pic_bed_transformer.PicBedTransformer(mode=mode)

        self.cache_folder = cache_folder
        self.output_folder = output_folder

        self.content = None
        self.pic_urls = None

    def set_file(self, file_path):
        self.file_path = file_path
        # read the markdown file
        self.content = read_md_file(self.file_path)
        # get the file name
        self.file_name = os.path.split(self.file_path)[-1]
        # find the picture urls
        self.pic_urls = find_pic_url(self.content)
        pass

    def set_cache_folder(self, cache_folder):
        self.cache_folder = cache_folder

    def set_output_folder(self, output_folder):
        self.output_folder = output_folder

    def clear(self):
        self.content = None
        self.pic_urls = None

    def transform(self):
        if self.content is None or self.pic_urls is None:
            raise ValueError("The content and the pic_urls should be set first.")

        # Download the pictures
        for i, pic_url in enumerate(self.pic_urls):
            # Get the new url using the time stamp
            local_pic_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_" + str(i) + ".png"
            local_pic_path = os.path.join(cache, local_pic_name)
            # Download the picture from the url and save it to the local folder
            try:
                new_url = self.pic_bed_transformer.transform(pic_url, local_pic_path)
                # Replace the old url with the new url
                self.content = self.content.replace(pic_url, new_url)
                print("Transform the picture %d/%d" % (i + 1, len(self.pic_urls)))
            except Exception as e:
                print("Failed to transform the picture %d/%d" % (i + 1, len(self.pic_urls)))
                print(e)

        # Write the new markdown file
        write_md_file(os.path.join(self.output_folder, self.file_name), self.content)

        # print the result
        print("Transform the markdown file successfully.")



# ///////// UTILS /////////
# Read the markdown file and return the content
def read_md_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content

# Write the markdown file
def write_md_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

# Find the picture url in the markdown file
def find_pic_url(content):
    # The pattern of the picture url
    pattern = re.compile(r"!\[.*?\]\((.*?)\)")
    # Find all the picture urls
    pic_urls = pattern.findall(content)
    return pic_urls

# Replace the picture url in the markdown file
def replace_pic_urls(content, pic_urls):
    for i, pic_url in enumerate(pic_urls):
        # Get the new url using the time stamp
        new_url = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_" + str(i) + ".png"
        # Replace the url
        content = content.replace(pic_url, new_url)
    return content

# Download the picture from the url
def download_pic(url, local_file_path):
    # Download the picture
    urllib.request.urlretrieve(url, local_file_path)

# Download the picture from the url without the extension
def download_pic_without_extension(url, local_file_path):
    # Download the picture
    urllib.request.urlretrieve(url, local_file_path)
    # Get the extension
    extension = os.path.splitext(local_file_path)[1]
    # Rename the file
    os.rename(local_file_path, local_file_path + extension)

# ///////// TEST CASE /////////
# ====== Test the read_md_file() ======
def test_read_md_file():
    file_path = r"C:\Users\hp\Desktop\2万字长文说清自动驾驶功能架构的演进.md"
    content = read_md_file(file_path)
    print(content)

# ====== Test the find_pic_url() ======
def test_find_pic_url():
    file_path = r"C:\Users\hp\Desktop\2万字长文说清自动驾驶功能架构的演进.md"
    content = read_md_file(file_path)
    pic_urls = find_pic_url(content)
    print(pic_urls)

# ====== Test the write_md_file() ======
def test_write_md_file():
    file_path = r"C:\Users\hp\Desktop\2万字长文说清自动驾驶功能架构的演进.md"
    new_file_path = r"C:\Users\hp\Desktop\2万字长文说清自动驾驶功能架构的演进_bak.md"
    content = read_md_file(file_path)
    write_md_file(new_file_path, content)
    print("test_write_md_file() passed!")

# ====== Test the download_pic() ======
def test_download_pic():
    file_path = r"C:\Users\hp\Desktop\2万字长文说清自动驾驶功能架构的演进.md"
    img_save_path = r"C:\Users\hp\Desktop\cache"
    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)
    content = read_md_file(file_path)
    pic_urls = find_pic_url(content)
    for i, pic_url in enumerate(pic_urls):
        # Get the picture name using the time stamp
        pic_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_" + str(i) + ".jpg"
        local_file_path = os.path.join(img_save_path, pic_name)
        download_pic(pic_url, local_file_path)
        print("Downloaded the picture: {}".format(pic_name))
    print("test_download_pic() passed!")

# ====== Test the download_pic_without_extension() ======
def test_download_pic_without_extension():
    url = "https://mmbiz.qpic.cn/sz_mmbiz_png/Mw7QHzQec2hvKrR3DiayMIibicJpcE8nRdfhzeaSII7BQfdlkOvkzbccW8qpicUXR6pGia2iclzlbSOvoCXZqyeMCu2A/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1"
    local_file_path = r"C:\Users\hp\Desktop\cache\test.jpg"
    # download the picture
    ret = urllib.request.urlretrieve(url, local_file_path)
    print(ret)

# ===== Test the replace_pic_urls() =====
def test_replace_pic_urls():
    file_path = r"C:\Users\hp\Desktop\2万字长文说清自动驾驶功能架构的演进.md"
    content = read_md_file(file_path)
    pic_urls = find_pic_url(content)
    content = replace_pic_urls(content, pic_urls)
    new_file_path = r"C:\Users\hp\Desktop\2万字长文说清自动驾驶功能架构的演进_bak.md"
    write_md_file(new_file_path, content)

# ===== Test FilePicTransformer =====
def test_FilePicTransformer():
    file_path = r"C:\Users\hp\Desktop\2万字长文说清自动驾驶功能架构的演进.md"
    img_save_path = r"C:\Users\hp\Desktop\cache"
    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)
    file_save_path = r"C:\Users\hp\Desktop\output"
    fpt = FilePicTransformer(cache_folder=img_save_path, output_folder=file_save_path)
    fpt.set_file(file_path)
    fpt.transform()
    print("test_FilePicTransformer() passed!")

if __name__ == "__main__":
    # # ====== Test the read_md_file() ======
    # test_read_md_file()

    # # ====== Test the find_pic_url() ======
    # test_find_pic_url()

    # # ====== Test the write_md_file() ======
    # test_write_md_file()

    # ====== Test the download_pic() ======
    # test_download_pic()

    # ====== Test the download_pic_without_extension() ======
    # test_download_pic_without_extension()

    # ====== Test the replace_pic_urls() ======
    # test_replace_pic_urls()

    # ====== Test FilePicTransformer ======
    test_FilePicTransformer()

    pass
