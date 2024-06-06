import os
import struct

# Define TAR types
TAR_TYPE_FILE         = b'0'
TAR_TYPE_DIR          = b'5'

# Function to convert integer to octal string
def int2oct(i):
    return oct(i)[2:].encode('utf-8')

# Function to create vmtar archive
def create_vmtar(input_dir, archive_file):
    with open(archive_file, 'wb') as f:
        for root, dirs, files in os.walk(input_dir):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(full_path, input_dir)
                
                # Write TAR header
                f.write(relative_path.ljust(100, '\x00').encode('utf-8')[:100])
                stat_info = os.stat(full_path)
                f.write(int2oct(stat_info.st_mode).rjust(8, b'0'))
                f.write(int2oct(stat_info.st_uid).rjust(8, b'0'))
                f.write(int2oct(stat_info.st_gid).rjust(8, b'0'))
                f.write(int2oct(stat_info.st_size).rjust(12, b'0'))
                f.write(int2oct(stat_info.st_mtime).rjust(12, b'0'))
                f.write(b' ' * 8)  # chksum
                f.write(TAR_TYPE_FILE)
                f.write(b' ' * 100)  # linkname
                f.write(b'visor ')
                f.write(b'00')
                f.write(stat_info.st_uid.ljust(32, '\x00').encode('utf-8'))
                f.write(stat_info.st_gid.ljust(32, '\x00').encode('utf-8'))
                f.write(b' ' * 8)  # devmajor
                f.write(b' ' * 8)  # devminor
                f.write(relative_path.ljust(151, '\x00').encode('utf-8')[:151])
                f.write(struct.pack('<I', 0))  # offset
                f.write(struct.pack('<I', 0))  # textoffset
                f.write(struct.pack('<I', 0))  # textsize
                f.write(struct.pack('<I', 0))  # numfixuppgs
                
                # Write file contents
                with open(full_path, 'rb') as fr:
                    while True:
                        chunk = fr.read(1 << 16)
                        if not chunk:
                            break
                        f.write(chunk)
    
# Example usage
create_vmtar('directory_to_archive', 'test.vtar')
