import sys
import os
import struct
import argparse
import gzip
import tarfile

vmtar = struct.Struct(
    '<'
    '100s'      # [0]  0x000 name
    '8s'        # [1]  0x064 mode
    '8s'        # [2]  0x06C uid
    '8s'        # [3]  0x074 gid
    '12s'       # [4]  0x07C size
    '12s'       # [5]  0x088 mtime
    '8s'        # [6]  0x094 chksum
    'c'         # [7]  0x09C type
    '100s'      # [8]  0x09D linkname
    '6s'        # [9]  0x101 magic
    '2s'        # [10] 0x107 version
    '32s'       # [11] 0x109 uname
    '32s'       # [12] 0x129 gname
    '8s'        # [13] 0x149 devmajor
    '8s'        # [14] 0x151 devminor
    '151s'      # [15] 0x159 prefix
    'I'         # [16] 0x1F0 offset
    'I'         # [17] 0x1F4 textoffset
    'I'         # [18] 0x1F8 textsize
    'I'         # [19] 0x1FC numfixuppgs
)               #      0x200 (total size)

TAR_TYPE_FILE         = b'0'
TAR_TYPE_LINK         = b'1'
TAR_TYPE_SYMLINK      = b'2'
TAR_TYPE_CHARDEV      = b'3'
TAR_TYPE_BLOCKDEV     = b'4'
TAR_TYPE_DIR          = b'5'
TAR_TYPE_FIFO         = b'6'
TAR_TYPE_SHAREDFILE   = b'7'
TAR_TYPE_GNU_LONGLINK = b'K'
TAR_TYPE_GNU_LONGNAME = b'L'

GZIP_MAGIC = b'\037\213'

def parse_args():
    parser = argparse.ArgumentParser(description='Extracts and creates VMware ESXi .vtar files')
    parser.add_argument('vtarfile', help='.vtar file')
    parser.add_argument('-C', '--directory', metavar='DIR', help='Change to directory DIR')
    
    # Actions
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument('-x', '--extract', action='store_true', help='Extract contents of vtarfile')
    grp.add_argument('-c', '--create', action='store_true', help='Create a new vtarfile from directory')
    
    return parser.parse_args()


def main():
    args = parse_args()
    print(args)

    if args.create:
        if not args.directory:
            print("Error: Missing directory argument (-C DIR) for creating vtar.")
            sys.exit(1)
        create_vtar(args.directory, args.vtarfile)
    elif args.extract:
        extract_vtar(args.vtarfile, args.directory)


def create_vtar(source_dir, vtarfile):
    with tarfile.open(vtarfile, 'w') as tar:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=os.path.relpath(file_path, source_dir))


def extract_vtar(vtarfile, output_dir):
    with open(vtarfile, 'rb') as raw_input_file:
        gzip_header = raw_input_file.read(2)
        raw_input_file.seek(0)
        f = raw_input_file

        if gzip_header == GZIP_MAGIC:
            f = gzip.GzipFile(fileobj=raw_input_file)

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            os.chdir(output_dir)
    
        print('pos         type offset   txtoff   txtsz    nfix size     name')
    
        while True:
            pos = f.tell()
            
            buf = f.read(vmtar.size)
            if len(buf) < vmtar.size:
                raise Exception('Short read at 0x{0:X}'.format(pos))
            
            obj = vmtar.unpack(buf)
            
            hdr_magic       = obj[9]
            if hdr_magic != b'visor ':
                break
            
            hdr_type        = obj[7]
            hdr_offset      = obj[16]
            hdr_textoffset  = obj[17]
            hdr_textsize    = obj[18]
            hdr_numfixuppgs = obj[19]
            hdr_size        = int(obj[4].rstrip(b'\0'), 8)
            hdr_name        = obj[0].rstrip(b'\0')
            
            print('0x{0:08X}  {1}    {2:08X} {3:08X} {4:08X} {5:04X} {6:08X} {7}'.format(
                pos, hdr_type.decode('utf-8'), hdr_offset, hdr_textoffset, hdr_textsize, hdr_numfixuppgs, hdr_size, hdr_name.decode('utf-8')))
                
            if hdr_type == TAR_TYPE_DIR:
                try:
                    os.mkdir(hdr_name.decode('utf-8'))
                except FileExistsError:
                    pass
            
            if hdr_type == TAR_TYPE_FILE:
                pos = f.tell()
                f.seek(hdr_offset, os.SEEK_SET)
                
                blob = f.read(hdr_size)
                with open(hdr_name.decode('utf-8'), 'wb') as outf:
                    outf.write(blob)
                
                f.seek(pos, os.SEEK_SET)


if __name__ == '__main__':
    sys.exit(main())
