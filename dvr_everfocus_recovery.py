# extract videos from RAW image of disk from EverFocus DVR
# save in .avr format
# playable with DVRViewer from ftp://webguest@ftp.everfocus.com.tw/fae_firmware/tools/DVR_Viewer/DVRViewer.exe
# (c) sprokopenko@CyberLab.com.ua and olbioua@gmail.com, densa@ukr.net 2018
# we dont know why it doesn't correctly work in wINDOWS os
# OS X/Linux works correct

import os, datetime, struct, sys


def is_valid(structure):
    sign = structure[0]
    length = structure[2]
    length1 = structure[3]
    cam_no = structure[5]

    if sign != 2857740885 or length != length1:
        return False

    return cam_no[:2] == 'CH'


def main():
    source_file = './dvr.dd'

    struct_fmt = '=IlIIl12s'  # int[5], float, byte[255]
    struct_len = struct.calcsize(struct_fmt)
    struct_unpack = struct.Struct(struct_fmt).unpack_from

    pos = 0
    i = 0
    out_path = './out/'


    fs = os.path.getsize(source_file)

    with open(source_file, "rb") as f:
        while True:
            try:
                data = f.read(struct_len)
                s = struct_unpack(data)
            except:
                print "End!!"
                sys.exit()

            if is_valid(s):
                date = s[1]
                length = s[2]
                cam_no = s[5].strip()
                date_print = datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y')
                chunk_size = 32 + length

                f.seek(pos)
                buffer_out = f.read(chunk_size)
                out_file_name = out_path + cam_no + "_" + date_print + ".arv"
                with open(out_file_name, "a") as out_file:
                    out_file.write(buffer_out)
                pos += chunk_size
                i += 1
                perc = (pos * 100.00) / fs
                print "%.3f" % perc, "%"
            else:
                pos += 1

            f.seek(pos)


if __name__ == '__main__':
    main()
