import os
import sys
import eyed3

if len(sys.argv) > 1:
    meta = eyed3.load(sys.argv[1])
    with open(os.path.splitext(sys.argv[1])[0] + ".jpg", 'wb') as f:
        f.write(meta.tag.images.get("Cover").image_data)
