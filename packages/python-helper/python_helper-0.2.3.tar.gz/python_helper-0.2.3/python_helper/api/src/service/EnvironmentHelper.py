import os, sys, json
from python_helper.api.src.service import StringHelper, LogHelper, ObjectHelper
from python_helper.api.src.domain import Constant as c

OS = os
SYS = sys
OS_SEPARATOR = OS.path.sep

clear = lambda: OS.system('cls')

def getEnvironmentValue(environmentKey, default=None) :
    environmentValue = OS.environ.get(environmentKey) if not environmentKey is None else default
    return environmentValue if not environmentValue is None else default

def setEnvironmentValue(environmentKey, environmentValue, default=None) :
    if ObjectHelper.isNotEmpty(environmentKey) :
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
                LogHelper.log(setEnvironmentValue, f'Failed to delete "{environmentKey}" enviroment variable key', exception=exception)
        return associatedValue
    else :
        LogHelper.debug(setEnvironmentValue, f'arguments: environmentKey: {environmentKey}, environmentValue: {environmentValue}, default: {default}')
        raise Exception(f'Error associating environment variable "{environmentKey}" key to environment variable "{environmentValue}" value')

def replaceEnvironmentVariable(environmentKey, environmentValue, default=None) :
    originalEnvironmentValue = getEnvironmentValue(environmentKey, default=default)
    setEnvironmentValue(environmentKey, environmentValue, default=default)
    return originalEnvironmentValue

def resetEnvironmentVariables(environmentVariables, originalEnvironmentVariables) :
    if environmentVariables :
        for key in environmentVariables.keys() :
            if key in originalEnvironmentVariables :
                setEnvironmentValue(key, originalEnvironmentVariables[key])

def deleteEnvironmentValue(environmentKey) :
    if not environmentKey is None :
        OS.environ.pop(environmentKey)

def getActiveEnvironmentVariableSet() :
    try :
        return json.loads(str(OS.environ)[8:-1].replace(c.DOUBLE_QUOTE, c.BACK_SLASH_DOUBLE_QUOTE).replace(c.SINGLE_QUOTE, c.DOUBLE_QUOTE))
    except Exception as exception :
        LogHelper.error(getActiveEnvironmentVariableSet, 'Not possible to load os.environ as a json. Returning os.environ as string by default', exception)
        return str(OS.environ)[8:-1]

def listDirectoryContent() :
    return OS.listdir(apisPath)

def appendPath(path) :
    SYS.path.append(path)

def getCurrentSoutStatus() :
    return SYS.stdout, SYS.stderr

def overrideSoutStatus(stdout, stderr) :
    SYS.stdout = stdout
    SYS.stderr = stderr
