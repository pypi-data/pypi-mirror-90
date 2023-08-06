from python_helper.api.src.service import LogHelper, ReflectionHelper, EnvironmentHelper

def EnvironmentVariable(*outerArgs, environmentVariables=None, **outerKwargs) :
    def innerMethodWrapper(resourceInstanceMethod,*innerMethodArgs,**innerMethodKwargs) :
        def innerResourceInstanceMethod(*innerArgs,**innerKwargs) :
            originalEnvironmentVariables = {}
            if environmentVariables :
                for key,value in environmentVariables.items() :
                    originalEnvironmentVariables[key] = EnvironmentHelper.replaceEnvironmentVariable(key, value)
            LogHelper.loadSettings()
            try :
                methodReturn = resourceInstanceMethod(*innerArgs,**innerKwargs)
            except Exception as exception :
                resetEnvironmentVariables(environmentVariables, originalEnvironmentVariables)
                raise exception
            resetEnvironmentVariables(environmentVariables, originalEnvironmentVariables)
            return methodReturn
        ReflectionHelper.overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper

def resetEnvironmentVariables(environmentVariables, originalEnvironmentVariables) :
    EnvironmentHelper.resetEnvironmentVariables(environmentVariables, originalEnvironmentVariables)
    LogHelper.loadSettings()
