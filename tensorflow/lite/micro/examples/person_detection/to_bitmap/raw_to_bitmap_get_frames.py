from raw_to_bitmap import parse_file, reshape_bitmaps
from PIL import Image
import sys

width = 96
height = 96
channels = 1

if len(sys.argv) < 2 :
    print("python raw_to_bitmap_get_frames.py <file_name>\n")
    exit()

file_name = sys.argv[1]
with open(file_name, "r") as f :
    data = f.read()
    count = 0
    index = data.find("+++ frame +++", 0)
    frame_end = data.find("--- frame ---", index)
    while(index != -1 and frame_end != -1) :
        single_frame = parse_file(data[index : frame_end + 14].splitlines(True), width, height, channels)
        bitmap = reshape_bitmaps(single_frame, width, height, channels)
        img = Image.fromarray(bitmap[0], 'L')
        img.save(file_name[:-4] + str(count) + '.bmp')
        img.show()
        index = data.find("+++ frame +++", index + 1)
        frame_end = data.find("--- frame ---", index)
        count += 1
    