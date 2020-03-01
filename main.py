import os
from PIL import Image
from resizeimage import resizeimage

imageWidth = 180
imageHeight = 180
startDirectory = '../portfolio2019/public/images/project/vids/'
endDirectory = '../portfolio2019/public/images/project/vidthumbs/'
prependName = ''
appendName = ''
turnAnimatedIntoStill = True
# allowedTypes = ['jpg', 'png', 'gif']
allowedTypes = ['gif']

# resize_crop crop the image with a centered rectangle of the specified size.
# resize_cover resize the image to fill the specified area, crop as needed (same behavior as background-size: cover).
# resize_contain resize the image so that it can fit in the specified area, keeping the ratio and without crop (same behavior as background-size: contain).
# resize_height resize the image to the specified height adjusting width to keep the ratio the same.
# resize_width resize the image to the specified width adjusting height to keep the ratio the same.
# resize_thumbnail resize image while keeping the ratio trying its best to match the specified size.

def resize_jpg(imgLoc, endLoc, imageWidth, imageHeight):
    with open(imgLoc, 'r+b') as readFile:
        with Image.open(readFile) as image:
            newImage = resizeimage.resize_cover(image, [imageWidth, imageHeight])
            newImage.save(endLoc, image.format)

def resize_gif(path, save_as=None, resize_to=None, turnAnimatedIntoStill = False):
    all_frames = extract_and_resize_frames(path, resize_to)
    if not save_as:
        save_as = path
    if len(all_frames) == 1 or turnAnimatedIntoStill == True:
        all_frames[0].save(save_as, optimize=True)
    else:
        all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)


def analyseImage(path):
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def extract_and_resize_frames(path, resize_to=None):
    mode = analyseImage(path)['mode']
    im = Image.open(path)
    if not resize_to:
        resize_to = (im.size[0] // 2, im.size[1] // 2)
    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')
    all_frames = []
    try:
        while True:
            if not im.getpalette():
                im.putpalette(p)
            new_frame = Image.new('RGBA', im.size)
            if mode == 'partial':
                new_frame.paste(last_frame)
            new_frame.paste(im, (0, 0), im.convert('RGBA'))
            new_frame.thumbnail(resize_to, Image.ANTIALIAS)
            all_frames.append(new_frame)
            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return all_frames


# main function
def processFiles(startDirectory, endDirectory, imageWidth, imageHeight, appendName, prependName, allowedTypes, turnAnimatedIntoStill):
    allFiles = os.listdir(startDirectory)
    print(allFiles)
    for fileName in allFiles:
        fileType = None
        splitName = fileName.split('.')
        if len(splitName) < 2:
            continue
        else:
            fileType = splitName[1]
        if fileType not in allowedTypes:
            continue
        if fileType:
            fileLoc = startDirectory + fileName
            endLoc = endDirectory + fileName
            if appendName and appendName != '':
                endLoc = endLoc.replace('.' + fileType, appendName + '.' + fileType)
            if prependName and prependName != '':
                endLoc = endDirectory + prependName + fileName
            if fileType == 'gif':
                imgSize = (imageHeight, imageWidth)
                resize_gif(fileLoc, endLoc, imgSize, turnAnimatedIntoStill)
            else:
                resize_jpg(fileLoc, endLoc, imageWidth, imageHeight)

processFiles(startDirectory, endDirectory, imageWidth, imageHeight, appendName, prependName, allowedTypes, turnAnimatedIntoStill)