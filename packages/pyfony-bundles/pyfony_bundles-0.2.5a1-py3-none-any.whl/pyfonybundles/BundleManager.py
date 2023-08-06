from pathlib import Path
from typing import List
from box import Box
from injecta.compiler.CompilerPassInterface import CompilerPassInterface
from injecta.config.ConfigLoader import ConfigLoader
from injecta.config.ConfigMerger import ConfigMerger
from injecta.service.Service import Service
from injecta.package.pathResolver import resolvePath
from pyfonybundles.Bundle import Bundle

class BundleManager:

    def __init__(self, bundles: List[Bundle]):
        self.__bundles = bundles
        self.__configLoader = ConfigLoader()
        self.__configMerger = ConfigMerger()

    def getCompilerPasses(self) -> List[CompilerPassInterface]:
        compilerPasses = []

        for bundle in self.__bundles:
            compilerPasses += bundle.getCompilerPasses()

        return compilerPasses

    # @deprecated, to be removed in 0.3
    def mergeRawConfig(self, appRawConfig: dict) -> dict:
        config = self.getBundlesConfig()

        return self.__configMerger.merge(config, appRawConfig)

    def getBundlesConfig(self) -> dict:
        config = dict()

        for bundle in self.__bundles:
            rootModuleName = bundle.__module__[:bundle.__module__.find('.')]
            configBasePath = resolvePath(rootModuleName) + '/_config'

            for configFileName in bundle.getConfigFiles():
                configFilePath = Path(configBasePath + '/' + configFileName)
                newConfig = self.__configLoader.load(configFilePath)

                config = self.__configMerger.merge(config, newConfig, False)

        return config

    # @deprecated, to be removed in 0.3
    def loadProjectBundlesConfig(self, rawConfig: dict, bundlesConfigsDir: str):
        config = self.getProjectBundlesConfig(bundlesConfigsDir)

        return self.__configMerger.merge(config, rawConfig)

    def getProjectBundlesConfig(self, bundlesConfigsDir: str) -> dict:
        config = dict()

        for bundle in self.__bundles:
            rootPackageName = bundle.__module__[:bundle.__module__.find('.')]
            projectBundleConfigPath = Path(bundlesConfigsDir + '/' + rootPackageName + '.yaml')

            if projectBundleConfigPath.exists():
                projectBundleConfig = self.__configLoader.load(projectBundleConfigPath)

                config = self.__configMerger.merge(config, projectBundleConfig)

        return config

    def modifyRawConfig(self, rawConfig: dict) -> dict:
        for bundle in self.__bundles:
            rawConfig = bundle.modifyRawConfig(rawConfig)

        return rawConfig

    def modifyServices(self, services: List[Service]):
        for bundle in self.__bundles:
            services = bundle.modifyServices(services)

        return services

    def modifyParameters(self, parameters: Box) -> Box:
        for bundle in self.__bundles:
            parameters = bundle.modifyParameters(parameters)

        return parameters
