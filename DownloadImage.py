import sys, os, urllib.request, csv
from multiprocessing import Pool
from PIL import Image
from io import BytesIO

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
        pil_image = Image.open(BytesIO(image_data))
    except:
        print('Warning: Failed to parse image %s' % key)
        return
    
    try:
        pil_image_rgb = pil_image.convert('RGB')
    except:
        print('Warning: Failed to save image %s to RGB' % key)        
        return
    
    pil_image_rgb.save(filename , format = 'JPEG', quality = 90)
    # try:
    #     pil_image_rgb.save(filename , format = 'JPEG', quality = 90)
    # except:
    #     print('Warning: Failed to save image %s' % filename)
    #     return

def Run():
    if len(sys.argv) != 3:
        print('Syntax: %s <data_file.csv> <output_dir>' % sys.argv[0])
        sys.exit(0)
    
    (data_file, out_dir) = sys.argv[1:]
    print(data_file, out_dir)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    # os.chdir(out_dir)

    key_url_list = ParseData(data_file)
    p = Pool(processes = 50)
    p.map(DownloadImage, key_url_list)

def Test():
    if len(sys.argv) != 3:
        print('Syntax: %s <data_file.csv> <output_dir>' % sys.argv[0])
        sys.exit(0)
    (data_file, out_dir) = sys.argv[1:]
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    (data_file, out_dir) = sys.argv[1:]
    csvfile = open(data_file, 'r')
    csvreader = csv.reader(csvfile)
    key_url_list = [line[:2] for line in csvreader]
    
    (key,url) = key_url_list[1]
    filename = os.path.join(out_dir, '%s.jpg' % key)
    test = urllib.request.urlopen(url)
    image_data = test.read()

    pil_image = Image.open(BytesIO(image_data))

    pil_image_rgb = pil_image.convert('RGB')

    pil_image_rgb.save(filename, format = 'JPEG', quality = 90)



if __name__ == '__main__':
    Run()


