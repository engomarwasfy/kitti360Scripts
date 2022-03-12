#!/usr/bin/python
#
# Convert instances from png files to a dictionary
#

from __future__ import print_function, absolute_import, division
import os, sys

# Cityscapes imports
from kitti360scripts.evaluation.semantic_2d.instance import *
from kitti360scripts.helpers.csHelpers import *

# Confidence is saved in the format of uint16
# Normalize confidence to [0,1] by dividing MAX_CONFIDENCE
MAX_CONFIDENCE=65535.0

def instances2dict(imageFileList, verbose=False):
    instanceDict = {}

    if not isinstance(imageFileList, list):
        imageFileList = [imageFileList]

    if verbose:
        print(f"Processing {len(imageFileList)} images...")

    for imgCount, (imageFileName, imageConfFileName) in enumerate(imageFileList, start=1):
        # Load image
        img = Image.open(imageFileName)

        # Image as numpy array
        imgNp = np.array(img)

        # Load confidence
        imgConf = Image.open(imageConfFileName)

        # Confidence as nnumpy array and normalize to [0,1]
        imgConf = np.array(imgConf) / MAX_CONFIDENCE

        # Initialize label categories
        instances = {label.name: [] for label in labels}
        # Loop through all instance ids in instance image
        for instanceId in np.unique(imgNp):
            instanceObj = Instance(imgNp, imgConf, instanceId)

            instances[id2label[instanceObj.labelID].name].append(instanceObj.toDict())

        # Merge garage instances to building instances
        # TODO: better solution?
        for instanceObj in instances['garage']:
            instanceObj['labelID'] = name2label['building'].id
            instances['building'].append(instanceObj)

        imgKey = os.path.abspath(imageFileName)
        instanceDict[imgKey] = instances
        if verbose:
            print("\rImages Processed: {}".format(imgCount), end=' ')
            sys.stdout.flush()

    if verbose:
        print("")

    return instanceDict

def main(argv):
    fileList = []
    if (len(argv) > 2):
        fileList.extend(arg for arg in argv if ("png" in arg))
    instances2dict(fileList, True)

if __name__ == "__main__":
    main(sys.argv[1:])
