import os, sys, json
from python_helper.api.src.service import StringHelper, LogHelper, ObjectHelper, SettingHelper
from python_helper.api.src.domain import Constant as c

OS = os
SYS = sys
OS_SEPARATOR = OS.path.sep

clear = lambda: OS.system('cls')

def getEnvironmentValue(environmentKey, default=None, avoidRecursiveCall=False) :
    environmentValue = default if ObjectHelper.isNone(environmentKey) else OS.environ.get(environmentKey)
    return environmentValue if ObjectHelper.isNotNone(environmentValue) else default

def updateEnvironmentValue(environmentKey, environmentValue, default=None, avoidRecursiveCall=False) :
    if ObjectHelper.isNotEmpty(environmentKey) :
        if SettingHelper.ACTIVE_ENVIRONMENT == environmentKey and not avoidRecursiveCall :
            return SettingHelper.updateActiveEnvironment(environmentValue)
        associatedValue = None
        if not environmentValue is None :
            associatedValue = str(StringHelper.filterString(environmentValue))
            OS.environ[environmentKey] = associatedValue
        elif not default is None :
            associatedValue = str(StringHelper.filterString(default))
            OS.environ[environmentKey] = associatedValue
        else :
            try:
                deleteEnvironmentValue(environmentKey)
            except Exception as exception :
                LogHelper.warning(updateEnvironmentValue, f'Failed to delete "{environmentKey}" enviroment variable key', exception=exception)
        return associatedValue
    else :
        LogHelper.debug(updateEnvironmentValue, f'arguments: environmentKey: {environmentKey}, environmentValue: {environmentValue}, default: {default}')
        raise Exception(f'Error associating environment variable "{environmentKey}" key to environment variable "{environmentValue}" value')

def replaceEnvironmentVariable(environmentKey, environmentValue, default=None, avoidRecursiveCall=False) :
    originalEnvironmentValue = getEnvironmentValue(environmentKey, default=default)
    updateEnvironmentValue(environmentKey, environmentValue, default=default)
    return originalEnvironmentValue

def resetEnvironmentVariables(environmentVariables, originalEnvironmentVariables, avoidRecursiveCall=False) :
    if environmentVariables :
        for key in environmentVariables.keys() :
            if key in originalEnvironmentVariables :
                updateEnvironmentValue(key, originalEnvironmentVariables[key])

def deleteEnvironmentValue(environmentKey, avoidRecursiveCall=False) :
    if ObjectHelper.isNotNone(environmentKey) :
        OS.environ.pop(environmentKey)

def getActiveEnvironmentVariableSet(avoidRecursiveCall=False) :
    try :
        return json.loads(str(OS.environ)[8:-1].replace(c.DOUBLE_QUOTE, c.BACK_SLASH_DOUBLE_QUOTE).replace(c.SINGLE_QUOTE, c.DOUBLE_QUOTE))
    except Exception as exception :
        LogHelper.error(getActiveEnvironmentVariableSet, 'Not possible to load os.environ as a json. Returning os.environ as string by default', exception)
        return str(OS.environ)[8:-1]

def listDirectoryContent(avoidRecursiveCall=False) :
    return OS.listdir(apisPath)

def appendPath(path, avoidRecursiveCall=False) :
    SYS.path.append(path)

def getCurrentSoutStatus(avoidRecursiveCall=False) :
    return SYS.stdout, SYS.stderr

def overrideSoutStatus(stdout, stderr, avoidRecursiveCall=False) :
    SYS.stdout = stdout
    SYS.stderr = stderr
