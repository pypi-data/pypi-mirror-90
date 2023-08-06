from python_helper.api.src.domain  import Constant as c
from python_helper.api.src.service import LogHelper, ObjectHelper, StringHelper, RandomHelper

MAXIMUN_ARGUMENTS = 20
METHOD_TYPE_NAME_LIST = [
    'method',
    'builtin_function_or_method'
]

def getAttributeOrMethod(instance, name) :
    attributeOrMethodInstance = None
    try :
        attributeOrMethodInstance = None if ObjectHelper.isNone(instance) or ObjectHelper.isNone(name) else getattr(instance, name)
    except Exception as exception :
        LogHelper.warning(getAttributeOrMethod, f'Not possible to get "{name}" from "{instance.__class__.__name__ if ObjectHelper.isNotNone(instance) else instance}" instance')
    return attributeOrMethodInstance

def getAttributeAndMethodNameList(instanceClass) :
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass)
    return [
        attributeOrMethodName
        for attributeOrMethodName in dir(objectNullArgsInstance)
        if isNotPrivate(attributeOrMethodName)
    ]

def isAttributeName(attributeName, objectNullArgsInstance) :
    return isNotPrivate(attributeName) and isNotMethod(objectNullArgsInstance, attributeName)

def getAttributeNameList(instanceClass) :
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass)
    return [
        attributeName
        for attributeName in dir(objectNullArgsInstance)
        if isAttributeName(attributeName, objectNullArgsInstance)
    ]

def getMethodNameList(instanceClass) :
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass)
    return [
        methodName
        for methodName in dir(objectNullArgsInstance)
        if isNotPrivate(methodName) and isMethod(objectNullArgsInstance, methodName)
    ]

def isMethodInstance(methodInstance) :
    return methodInstance.__class__.__name__ in METHOD_TYPE_NAME_LIST if ObjectHelper.isNotNone(methodInstance) else False

def isNotMethodInstance(methodInstance) :
    return not isMethodInstance(methodInstance)

def isMethod(objectInstance, name) :
    if ObjectHelper.isNone(objectInstance) or StringHelper.isBlank(name) :
        return False
    return isMethodInstance(getAttributeOrMethod(objectInstance, name))

def isNotMethod(objectInstance, name) :
    if ObjectHelper.isNone(objectInstance) or StringHelper.isBlank(name) :
        return False
    return isNotMethodInstance(getAttributeOrMethod(objectInstance, name))

def instanciateItWithNoArgsConstructor(targetClass, amountOfNoneArgs=0, args=None) :
    if ObjectHelper.isNone(args) :
        args = []
    for _ in range(amountOfNoneArgs) :
        args.append(None)
    objectInstance = None
    for _ in range(MAXIMUN_ARGUMENTS) :
        try :
            objectInstance = targetClass(*args)
            break
        except :
            args.append(None)
    if not isinstance(objectInstance, targetClass) :
        raise Exception(f'Not possible to instanciate {targetClass} class in instanciateItWithNoArgsConstructor() method with None as args constructor')
    return objectInstance

def getArgsOrder(targetClass) :
    noneArgs = []
    noneInstance = instanciateItWithNoArgsConstructor(targetClass, amountOfNoneArgs=0, args=noneArgs)
    strArgs = []
    for arg in range(len(noneArgs)) :
        strArgs.append(RandomHelper.string(minimum=10))
    try :
        instance = targetClass(*strArgs)
        instanceDataDictionary = getAttributeDataDictionary(instance)
        argsOrderDictionary = {}
        for key,value in instanceDataDictionary.items() :
            if StringHelper.isNotBlank(value) :
                argsOrderDictionary[strArgs.index(value)] = key
        argsOrder = [argsOrderDictionary[key] for key in sorted(argsOrderDictionary)]
    except Exception as exception :
        errorMessage = f'Not possible to get args order from "{targetClass.__name__}" target class'
        LogHelper.error(getArgsOrder, errorMessage, exception)
        raise Exception(errorMessage)
    return argsOrder

    #
    #
    #
    # args = []
    # objectInstance = None
    # for _ in range(MAXIMUN_ARGUMENTS) :
    #     try :
    #         objectInstance = instanceClass(*args)
    #         break
    #     except :
    #         args.append(None)
    # if not isinstance(objectInstance, instanceClass) :
    #     raise Exception(f'Not possible to instanciate {instanceClass} class in instanciateItWithNoArgsConstructor() method with None as args constructor')
    return targetClass

def isNotPrivate(attributeOrMethodName) :
    return StringHelper.isNotBlank(attributeOrMethodName) and (
        not attributeOrMethodName.startswith(f'{2 * c.UNDERSCORE}') and
        not attributeOrMethodName.startswith(c.UNDERSCORE) and
        not ObjectHelper.METADATA_NAME == attributeOrMethodName
    )

def getAttributePointerList(instance) :
    return [
        getattr(instance, instanceAttributeName)
        for instanceAttributeName in dir(instance)
        if isNotPrivate(attributeOrMethodName)
    ]

def getAttributeDataList(instance) :
    return [
        (getattr(instance, instanceAttributeName), instanceAttributeName)
        for instanceAttributeName in dir(instance)
        if isAttributeName(instanceAttributeName, instance)
    ]

def getAttributeDataDictionary(instance) :
    instanceDataDictionary = {}
    for name in dir(instance) :
        if isAttributeName(name, instance) :
            instanceDataDictionary[name] = getattr(instance, name)
    return instanceDataDictionary

def setAttributeOrMethod(instance, attributeOrMethodName, attributeOrMethodInstance) :
    setattr(instance, attributeOrMethodName, attributeOrMethodInstance)

def overrideSignatures(toOverride, original) :
    try :
        toOverride.__name__ = original.__name__
        toOverride.__module__ = original.__module__
        toOverride.__qualname__ = original.__qualname__
    except Exception as exception :
        LogHelper.error(overrideSignatures,f'''failed to override signatures of {toOverride} by signatures of {original} method''',exception)

def printDetails(toDetail):
    print(f'{2 * c.TAB}printDetails({toDetail}):')
    try :
        print(f'{2 * c.TAB}type({toDetail}).__name__ = {type(toDetail).__name__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__ = {type(toDetail).__class__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__.__module__ = {type(toDetail).__class__.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__.__name__ = {type(toDetail).__class__.__name__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__name__ = {toDetail.__class__.__name__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__module__ = {toDetail.__class__.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__qualname__ = {toDetail.__class__.__qualname__}')
    except :
        pass

def printClass(instanceClass) :
    print(f'{2 * c.TAB}printClass({instanceClass}):')
    try :
        print(f'{2 * c.TAB}{instanceClass}.__name__ = {instanceClass.__name__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{instanceClass}.__module__ = {instanceClass.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{instanceClass}.__qualname__ = {instanceClass.__qualname__}')
    except :
        pass
