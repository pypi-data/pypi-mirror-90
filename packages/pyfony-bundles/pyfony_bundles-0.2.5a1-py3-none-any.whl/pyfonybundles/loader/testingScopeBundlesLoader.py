from pyfonybundles.loader import entryPoints, pyfonyBundlesLoader

def getTestingScopes():
    groupedEntryPoints = entryPoints.groupByModule(getEntryPoints())
    return _extractUniqueScopes(groupedEntryPoints)

def getEntryPoints():
    return entryPoints.getByKey('pyfony.testing_scope')

def loadBundles(testingScopeName: str):
    mappedEntryPoints = entryPoints.groupByModule(pyfonyBundlesLoader.getEntryPoints())
    mappedEntryPointsTesting = entryPoints.groupByModule(getEntryPoints())

    def createBundle(moduleName, moduleEntryPoints: dict):
        if moduleName in mappedEntryPointsTesting and testingScopeName in mappedEntryPointsTesting[moduleName]:
            return mappedEntryPointsTesting[moduleName][testingScopeName]()

        return moduleEntryPoints['autodetect']()

    return [createBundle(moduleName, moduleEntryPoints) for moduleName, moduleEntryPoints in mappedEntryPoints.items()]

def _extractUniqueScopes(groupedEntryPoints: dict):
    allScopes = set()

    for _, moduleEntryPoints in groupedEntryPoints.items():
        for scope in moduleEntryPoints.keys():
            allScopes.add(scope)

    return allScopes
