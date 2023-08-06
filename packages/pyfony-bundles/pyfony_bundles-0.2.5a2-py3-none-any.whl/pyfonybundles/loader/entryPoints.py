import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata # pylint: disable = no-name-in-module
else:
    import importlib_metadata # pylint: disable = import-error

def getByKey(key: str):
    return importlib_metadata.entry_points().get(key, ())

def groupByModule(entryPoints: list):
    groupedEntryPoints = dict()

    for entryPoint in entryPoints:
        moduleName = entryPoint.value.split(':')[0]

        if moduleName not in groupedEntryPoints:
            groupedEntryPoints[moduleName] = dict()

        groupedEntryPoints[moduleName][entryPoint.name] = entryPoint.load()

    return groupedEntryPoints
