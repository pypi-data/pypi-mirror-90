from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import LogHelper, ReflectionHelper, EnvironmentHelper, ObjectHelper
from python_helper.api.src.annotation.EnvironmentAnnotation import EnvironmentVariable

TEST_VALUE_NOT_SET = '__TEST_VALUE_NOT_SET__'

CALL_BEFORE = 'callBefore'
CALL_AFTER = 'callAfter'

RETURN_VALUE_FROM_CALL_BEFORE = 'returnOfCallBefore'
RETURN_VALUE_FROM_CALL_AFTER = 'returnOfCallAfter'

BEFORE_THE_TEST = 'before'
AFTER_THE_TEST = 'after'

def Test(
    *outerArgs,
    environmentVariables = None,
    callBefore = TEST_VALUE_NOT_SET,
    argsOfCallBefore = TEST_VALUE_NOT_SET,
    kwargsOfCallBefore = TEST_VALUE_NOT_SET,
    callAfter = TEST_VALUE_NOT_SET,
    argsOfCallAfter = TEST_VALUE_NOT_SET,
    kwargsOfCallAfter = TEST_VALUE_NOT_SET,
    returns = None,
    **outerKwargs
) :
    def innerMethodWrapper(resourceInstanceMethod,*innerMethodArgs,**innerMethodKwargs) :
        @EnvironmentVariable(environmentVariables=environmentVariables)
        def innerResourceInstanceMethod(*innerArgs,**innerKwargs) :
            methodReturnException = None
            methodReturn = TEST_VALUE_NOT_SET
            callBeforeException = handleAction(handleBefore, BEFORE_THE_TEST, resourceInstanceMethod, callBefore, argsOfCallBefore, kwargsOfCallBefore, returns)
            if ObjectHelper.isNotNone(callBeforeException) :
                raise callBeforeException
            try :
                methodReturn = resourceInstanceMethod(*innerArgs,**innerKwargs)
                LogHelper.printSuccess(f'{ReflectionHelper.getName(resourceInstanceMethod)} test succeed', condition=True)
            except Exception as exception :
                methodReturnException = exception
                LogHelper.printError(f'"{ReflectionHelper.getName(resourceInstanceMethod)}" test failed', condition=True, exception=methodReturnException)
            callAfterException = handleAction(handleAfter, AFTER_THE_TEST, resourceInstanceMethod, callAfter, argsOfCallAfter, kwargsOfCallAfter, returns)
            return handleReturn(methodReturn, methodReturnException, callAfterException)
        ReflectionHelper.overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper

def handleReturn(methodReturn, methodReturnException, callAfterException) :
    if ObjectHelper.isNotNone(methodReturnException) or ObjectHelper.isNotNone(callAfterException) :
        if ObjectHelper.isNotNone(methodReturnException) and ObjectHelper.isNotNone(callAfterException) :
            raise Exception(f'{LogHelper.getExceptionMessage(methodReturnException)}. Followed by: {LogHelper.getExceptionMessage(callAfterException)}')
        elif ObjectHelper.isNotNone(methodReturnException) :
            raise methodReturnException
        raise callAfterException
    if not TEST_VALUE_NOT_SET == methodReturn :
        return methodReturn

def handleAction(action, moment, resourceInstanceMethod, callAfter, argsOfCallAfter, kwargsOfCallAfter, returns) :
    try :
        action(resourceInstanceMethod, callAfter, argsOfCallAfter, kwargsOfCallAfter, returns)
    except Exception as exception :
        LogHelper.printError(f'"{ReflectionHelper.getName(resourceInstanceMethod)}" test went wrong while handling "{ReflectionHelper.getName(action)}" {moment} the test. Check TEST logs for more information', condition=True, exception=exception)
        return exception

def handleBefore(resourceInstanceMethod, methodInstance, args, kwargs, returns) :
    LogHelper.test(resourceInstanceMethod, 'Test started')
    handle(resourceInstanceMethod, methodInstance, args, kwargs, returns, CALL_BEFORE, RETURN_VALUE_FROM_CALL_BEFORE)

def handleAfter(resourceInstanceMethod, methodInstance, args, kwargs, returns, methodReturnException=None) :
    handle(resourceInstanceMethod, methodInstance, args, kwargs, returns, CALL_AFTER, RETURN_VALUE_FROM_CALL_AFTER)

def handle(resourceInstanceMethod, methodInstance, args, kwargs, returns, moment, returnKey) :
    returnCall = None
    if methodIsPresent(methodInstance) :
        argsMessage = getArgsLogMessage(args)
        kwargsMessage = getKwargsLogMessage(kwargs)
        returnCall = getRetrunValue(methodInstance, args, kwargs)
        LogHelper.test(resourceInstanceMethod, f'{moment}({argsMessage}, {kwargsMessage}): {returnCall}')
    else :
        LogHelper.test(resourceInstanceMethod, f'Method "{moment}" not defined')
    if returnsValueIsPresent(returns) :
        returns[returnKey] = returnCall

def getArgsLogMessage(args) :
    if TEST_VALUE_NOT_SET == args :
        return '*()'
    return f'*({args})'

def getKwargsLogMessage(kwargs) :
    if TEST_VALUE_NOT_SET == kwargs :
        return '**{}'
    return f'**{kwargs}'

def getRetrunValue(methodInstance, givenArgs, givenKwargs) :
    if methodIsPresent(methodInstance) :
        args = [] if TEST_VALUE_NOT_SET == givenArgs else givenArgs
        kwargs = {} if TEST_VALUE_NOT_SET == givenKwargs else givenKwargs
        return methodInstance(*args, **kwargs)

def methodIsPresent(methodInstance) :
    return not TEST_VALUE_NOT_SET == methodInstance and ObjectHelper.isNotNone(methodInstance)

def returnsValueIsPresent(returns) :
    isPresent = ObjectHelper.isDictionary(returns)
    if not isPresent :
        LogHelper.test(returnsValueIsPresent, f'the key "returns" from "{ReflectionHelper.getName(Test)}" annotation call was not defined')
    return isPresent
