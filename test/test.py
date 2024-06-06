import os
import struct

# Constants for vtar format
TAR_TYPE_FILE = b'0'
TAR_TYPE_DIR = b'5'

# Function to convert octal string to integer
def oct2bin(s):
    return int(s, 8)

# Function to create vtar archive from a directory
def create_vtar(directory, output_file):
    bufsize = 1 << 16  # Buffer size for file copying

    with open(output_file, 'wb') as tarfile:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                stat = os.stat(file_path)

                # Prepare header
                hdr = struct.pack('<100s8s8s8s12s12s8s1s100s6s2s32s32s8s8s151sIII',
                                  rel_path.encode('utf-8'),  # name
                                  oct(stat.st_mode & 0o777).encode('utf-8'),  # mode
                                  oct(stat.st_uid).encode('utf-8'),  # uid
                                  oct(stat.st_gid).encode('utf-8'),  # gid
                                  oct(stat.st_size).encode('utf-8'),  # size
                                  oct(int(stat.st_mtime)).encode('utf-8'),  # mtime (converted to octal integer)
                                  b' ' * 8,  # chksum placeholder
                                  TAR_TYPE_FILE if os.path.isfile(file_path) else TAR_TYPE_DIR,  # type
                                  b'',  # linkname (empty for files)
                                  b'visor ',  # magic
                                  b'00',  # version (unused)
                                  b'',  # uname
                                  b'',  # gname
                                  b'0' * 8,  # devmajor
                                  b'0' * 8,  # devminor
                                  b'',  # prefix
                                  0,  # offset (not used)
                                  0,  # textoffset (not used)
                                  0)  # textsize (not used)

                # Calculate checksum
                chksum = sum(hdr)
                chksum = struct.pack('<8s', oct(chksum).encode('utf-8'))
                hdr = hdr[:148] + chksum + hdr[156:]

                # Write header to tarfile
                tarfile.write(hdr)

                # Write file content to tarfile
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        while True:
                            buf = f.read(bufsize)
                            if not buf:
                                break
                            tarfile.write(buf)

        # Write two empty blocks at the end of the archive
        tarfile.write(b'\0' * 1024)
        tarfile.write(b'\0' * 1024)

# Example usage:
if __name__ == "__main__":
    create_vtar('weaselin_extracted', 'test.vtar')
