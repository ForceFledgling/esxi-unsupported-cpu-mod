import os

TAR_TYPE_FILE = b'0'
TAR_TYPE_DIR = b'5'

# Function to convert octal string to integer, handling null bytes
def oct2int(oct_str):
    # Remove null bytes
    cleaned_oct_str = oct_str.replace(b'\x00', b'')
    
    # Convert cleaned string to integer
    return int(cleaned_oct_str.decode('utf-8'), 8) if cleaned_oct_str else 0


# Function to extract vmtar archive
def extract_vmtar(archive_file, output_dir):
    with open(archive_file, 'rb') as f:
        while True:
            # Read header
            name = f.read(100).decode('utf-8').strip('\x00')
            if not name:
                break
            
            mode = f.read(8).decode('utf-8')
            uid = f.read(8).decode('utf-8')
            gid = f.read(8).decode('utf-8')
            size = f.read(12).decode('utf-8')
            mtime = f.read(12).decode('utf-8')
            chksum = f.read(8).decode('utf-8')
            typeflag = f.read(1)
            linkname = f.read(100).decode('utf-8').strip('\x00')
            
            # Skip magic and version fields
            f.read(6 + 2)
            
            uname = f.read(32).decode('utf-8').strip('\x00')
            gname = f.read(32).decode('utf-8').strip('\x00')
            devmajor = f.read(8).decode('utf-8')
            devminor = f.read(8).decode('utf-8')
            
            # Read prefix as bytes, not decoding it
            prefix = f.read(151)
            
            # Skip offset, textoffset, textsize, numfixuppgs fields
            f.read(4 * 4)
            
            # Calculate size from octal to integer
            size_int = oct2int(size)
            
            # Create full file path
            full_path = os.path.join(output_dir, name)
            
            if typeflag == TAR_TYPE_DIR:
                # Create directory
                os.makedirs(full_path, exist_ok=True)
                print(f"Created directory: {full_path}")
            elif typeflag == TAR_TYPE_FILE:
                # Create file and write contents
                with open(full_path, 'wb') as fw:
                    remaining_size = size_int
                    while remaining_size > 0:
                        chunk_size = min(remaining_size, 1 << 16)
                        chunk = f.read(chunk_size)
                        fw.write(chunk)
                        remaining_size -= len(chunk)
                
                print(f"Extracted file: {full_path}")

# Example usage
if __name__ == "__main__":
    extract_vmtar('source.vtar', 'source_extracted')
