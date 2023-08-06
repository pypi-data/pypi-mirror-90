from python_helper.api.src.service import LogHelper, ReflectionHelper
from python_helper.api.src.domain import Constant as c

KW_CLASS = 'class'
KW_METHOD = 'method'
KW_FUNCTION = 'function'
NAME_NOT_PRESENT = 'name not present'

def Function(function,*args,**kwargs) :
    def wrapedFunction(*args,**kwargs) :
        try :
            functionReturn = function(*args,**kwargs)
        except Exception as exception :
            try :
                functionName = f'{function.__name__}'
            except :
                functionName = f'({KW_FUNCTION} {NAME_NOT_PRESENT})'
            LogHelper.wraper(Function,f'''failed to execute "{functionName}(args={args}, kwargs={kwargs})"''',exception)
            raise Exception(f'{functionName} function error{c.DOT_SPACE_CAUSE}{str(exception)}')
        return functionReturn
    ReflectionHelper.overrideSignatures(wrapedFunction, function)
    return wrapedFunction

def FunctionThrough(function,*args,**kwargs) :
    def wrapedFunction(*args,**kwargs) :
        try :
            functionReturn = function(*args,**kwargs)
        except Exception as exception :
            try :
                functionName = f'{function.__name__}'
            except :
                functionName = f'({KW_FUNCTION} {NAME_NOT_PRESENT})'
            LogHelper.wraper(Function,f'''exception trace passed through "{functionName}(args={args}, kwargs={kwargs})"''',exception)
            raise exception
        return functionReturn
    ReflectionHelper.overrideSignatures(wrapedFunction, function)
    return wrapedFunction

def Method(method,*args,**kwargs) :
    def wrapedMethod(*args,**kwargs) :
        try :
            methodReturn = method(*args,**kwargs)
        except Exception as exception :
            try :
                className = f'{args[0].__class__.__name__}'
            except :
                className = f'({KW_CLASS} {NAME_NOT_PRESENT})'
            try :
                methodName = method.__name__
            except :
                methodName = f'({KW_METHOD} {NAME_NOT_PRESENT})'
            LogHelper.wraper(Method,f'''failed to execute {className}{c.DOT}{methodName} method. Received args: {args}. Received kwargs: {kwargs}''',exception)
            raise Exception(f'{className}{methodName} method error{c.DOT_SPACE_CAUSE}{str(exception)}')
        return methodReturn
    ReflectionHelper.overrideSignatures(wrapedMethod, method)
    return wrapedMethod
