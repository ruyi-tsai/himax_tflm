from raw_to_bitmap import parse_file, reshape_bitmaps
from PIL import Image
import sys
import serial  # 引用pySerial模組

 
COM_PORT = 'COM7'    # 指定通訊埠名稱
BAUD_RATES = 115200   # 設定傳輸速率
width = 96
height = 96
channels = 1
count = 0
start=0
enable = 0
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
prefix_name='bmp_'


def show_bitmap(buf):
    global count
    single_frame = parse_file(buf[:].splitlines(False), width, height, channels)
    if(single_frame==[]):
        return;
    bitmap = reshape_bitmaps(single_frame, width, height, channels)
    img = Image.fromarray(bitmap[0], 'L')
    img.save(prefix_name + str(count) + '.bmp')
    print('start to analyze image{} ...'.format(count))
    img.show()
    
    count += 1


buf=''

try:
    while True:
        while ser.in_waiting:          # 若收到序列資料…
            data_raw = ser.readline()  # 讀取一行
            data = data_raw.decode().strip('\r\n')+'\n'   # 用預設的UTF-8解碼
            #print(data)
            index = data.find("000 frame 000", 0)
            if index!=-1:
                buf=''
                start=1
                enable = 2
                

            frame_end = data.find("--- frame ---",0)
            if frame_end!=-1:
                buf+=data
                start=0
                

            if start==1:
                buf+=data                
            elif start==0 and frame_end!=-1 and enable==2:
                show_bitmap(buf)
                buf=''
                
           
            if data.find("score", 0)!=-1:
                print(data)
               

except KeyboardInterrupt:
    ser.close()    # 清除序列通訊物件



