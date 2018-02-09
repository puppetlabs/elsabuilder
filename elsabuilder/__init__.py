import os

version = open("version").read().strip()
image_id = os.environ["HOSTNAME"]

version_info = {
    "image_id": elsabuilder.image_id,
    "version": elsabuilder.version,
}
