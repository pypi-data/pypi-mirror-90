from pyfonybundles.loader import entryPoints

def getEntryPoints():
    return entryPoints.getByKey('pyfony.bundle')

def loadBundles():
    mappedEntryPoints = entryPoints.groupByModule(getEntryPoints())
    return [moduleEntryPoints['autodetect']() for moduleName, moduleEntryPoints in mappedEntryPoints.items()]
