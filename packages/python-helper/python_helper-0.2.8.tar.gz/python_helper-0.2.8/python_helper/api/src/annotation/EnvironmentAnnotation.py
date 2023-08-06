from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import LogHelper, ReflectionHelper, EnvironmentHelper, ObjectHelper, SettingHelper

def EnvironmentVariable(*outerArgs, environmentVariables=None, **outerKwargs) :
    def innerMethodWrapper(resourceInstanceMethod,*innerMethodArgs,**innerMethodKwargs) :
        def innerResourceInstanceMethod(*innerArgs,**innerKwargs) :
            methodReturn = None
            wraperException = None
            originalEnvironmentVariables, originalActiveEnvironment = getOriginalEnvironmentVariables(environmentVariables)
            try :
                methodReturn = resourceInstanceMethod(*innerArgs,**innerKwargs)
            except Exception as exception :
                wraperException = exception
            resetEnvironmentVariables(environmentVariables, originalEnvironmentVariables, originalActiveEnvironment)
            if ObjectHelper.isNotNone(wraperException) :
                raise wraperException
            return methodReturn
        ReflectionHelper.overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper

def getOriginalEnvironmentVariables(environmentVariables) :
    if ObjectHelper.isNone(SettingHelper.ACTIVE_ENVIRONMENT_VALUE) :
        originalActiveEnvironment = None
    else :
        originalActiveEnvironment = f'{c.NOTHING}{SettingHelper.ACTIVE_ENVIRONMENT_VALUE}'
    if ObjectHelper.isNotEmpty(originalActiveEnvironment) :
        SettingHelper.ACTIVE_ENVIRONMENT_VALUE = None
    originalEnvironmentVariables = {}
    if ObjectHelper.isDictionary(environmentVariables) :
        for key,value in environmentVariables.items() :
            originalEnvironmentVariables[key] = EnvironmentHelper.switch(key, value)
    SettingHelper.getActiveEnvironment()
    LogHelper.loadSettings()
    return originalEnvironmentVariables, originalActiveEnvironment

def resetEnvironmentVariables(environmentVariables, originalEnvironmentVariables, originalActiveEnvironment) :
    EnvironmentHelper.reset(environmentVariables, originalEnvironmentVariables)
    LogHelper.loadSettings()
    SettingHelper.ACTIVE_ENVIRONMENT_VALUE = originalActiveEnvironment
