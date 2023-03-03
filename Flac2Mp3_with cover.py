from mutagen.id3 import ID3, APIC
from mutagen.flac import FLAC
import os, sys, subprocess

dir_with_flac_files = 'dir\\with\\flac\\files\\'
out_dir = 'F:\\mp3'

def Flac2Mp3_v2(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    try:
        flac_files = [f for f in os.listdir(input_dir) if f.endswith('.flac')]
        print(f'{len(flac_files)} files found in "{input_dir}"\n')
        
        for root, dirs, files in os.walk(input_dir):
            for e, filename in enumerate(files):
                if filename.endswith('.flac'):
                    print(f'⏳  |{e+1}/{len(flac_files)}| {filename}')
                    input_file = os.path.join(root, filename)
                    output_file = os.path.join(output_dir, filename.replace('.flac', '.mp3'))
                    subprocess.call(['ffmpeg', '-i', input_file, '-codec:a', 'libmp3lame', '-qscale:a', '0', output_file],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                    tags = FLAC(input_file)
                    audio = ID3(output_file)
                    audio.add(APIC(
                                encoding = 0,
                                mime = 'image/jpeg',
                                type = 3,
                                desc = '',
                                data = tags.pictures[0].data))
                    audio.save(v2_version=3)
                    print(f'✅ Saved')
        print('\nDone. All files converted\n')
    except:
        print(f'❌ | Error in {output_file}')
        print(sys.exc_info())

Flac2Mp3_v2(dir_with_flac_files, out_dir)
