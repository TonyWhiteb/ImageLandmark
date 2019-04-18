import sys, os, multiprocessing, urllib, csv
from PIL import Image
from io import StringIO

def ParseData(data_file):
    csvfile = open(data_file, 'r')
    csvreader = csv.reader(csvfile)
    key_url_list = [line[:2] for line in csvreader]
    return key_url_list[1:]

def DownloadImage(key_url):
    out_dir = sys.argv[2]
    (key,url) = key_url
    filename = os.path.join(out_dir, '%s.jpg' % key)
    
    if os.path.exists(filename):
        print('image %s already exists and skippppppping' % filename)
        return
    
    try:

        response = urllib.request.urlopen(url)
        image_data = response.read()
    except:
        print('Warning: Could not download image%s from %s' % (key,url))
        return
    
    try:
        pil_image = Image.open(StringIO(image_data))
    except:
        print('Warning: Failed to parse image %s' % key)
        return
    
    try:
        pil_image_rpg = pil_image.convert('RGB')
    except:
        print('Warning: Failed to save image %s to RGB' % key)        
        return
    
    try:
        pil_image_rgb.save(filename, format = 'JPEG', quality = 90)
    except:
        print('Warning: Failed to save image %s' % filename)
        return

def Run():
    if len(sys.argv) != 3:
        print('Syntax: %s <data_file.csv> <output_dir>' % sys.argv[0])
        sys.exit(0)
    
    (data_file, out_dir) = sys.argv[1:]

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    key_url_list = ParseData(data_file)
    pool = multiprocessing.Pool(processes = 50)
    pool.map(DownloadImage, key_url_list)


if __name__ == '__main__':
    Run()


