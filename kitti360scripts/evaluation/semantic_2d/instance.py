#!/usr/bin/python
#
# Instance class
#

class Instance(object):
    instID     = 0
    labelID    = 0
    pixelCount = 0
    medDist    = -1
    distConf   = 0.0

    def __init__(self, imgNp, imgConf, instID):
        if (instID == -1):
            return
        self.instID     = int(instID)
        self.labelID    = int(self.getLabelID(instID))
        self.pixelCount = self.getWeightedInstancePixels(imgNp, imgConf, instID)

    def getLabelID(self, instID):
        return instID if (instID < 1000) else int(instID / 1000)

    def getInstancePixels(self, imgNp, instLabel):
        return (imgNp == instLabel).sum()

    def getWeightedInstancePixels(self, imgNp, imgConf, instLabel):
        return imgConf[imgNp == instLabel].sum()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def toDict(self):
        return {
            "instID": self.instID,
            "labelID": self.labelID,
            "pixelCount": self.pixelCount,
            "medDist": self.medDist,
            "distConf": self.distConf,
        }

    def fromJSON(self, data):
        self.instID     = int(data["instID"])
        self.labelID    = int(data["labelID"])
        self.pixelCount = int(data["pixelCount"])
        if ("medDist" in data):
            self.medDist    = float(data["medDist"])
            self.distConf   = float(data["distConf"])

    def __str__(self):
        return f"({str(self.instID)})"
