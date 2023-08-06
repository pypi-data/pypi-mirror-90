import colorama
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import SettingHelper, StringHelper, EnvironmentHelper

LOG = 'LOG'
SUCCESS = 'SUCCESS'
SETTING = 'SETTING'
DEBUG = 'DEBUG'
WARNING = 'WARNING'
WRAPPER = 'WRAPPER'
FAILURE = 'FAILURE'
ERROR = 'ERROR'

RESET_ALL_COLORS = colorama.Style.RESET_ALL

from python_helper.api.src.helper import LogHelperHelper

global LOG_HELPER_SETTINGS
def loadSettings() :
    global LOG_HELPER_SETTINGS
    settings = {}
    settings[SettingHelper.ACTIVE_ENVIRONMENT] : SettingHelper.getActiveEnvironment()
    if SettingHelper.activeEnvironmentIsLocal() :
        colorama.init(autoreset=True)
        print(RESET_ALL_COLORS,end=c.NOTHING)
    for level in LogHelperHelper.LEVEL_DICTIONARY :
        status = EnvironmentHelper.getEnvironmentValue(level)
        settings[level] = status if not status is None else c.TRUE
    LOG_HELPER_SETTINGS = settings

loadSettings()

def log(origin,message,level=LOG,exception=None) :
    LogHelperHelper.softLog(origin,message,LOG,exception=exception)

def success(origin,message) :
    LogHelperHelper.softLog(origin,message,SUCCESS)

def setting(origin,message) :
    LogHelperHelper.softLog(origin,message,SETTING)

def debug(origin,message) :
    LogHelperHelper.softLog(origin,message,DEBUG)

def warning(origin,message) :
    LogHelperHelper.softLog(origin,message,WARNING)

def wraper(origin,message,exception) :
    LogHelperHelper.hardLog(origin,message,exception,WRAPPER)

def failure(origin,message,exception) :
    LogHelperHelper.hardLog(origin,message,exception,FAILURE)

def error(origin,message,exception) :
    LogHelperHelper.hardLog(origin,message,exception,ERROR)

def printLog(message,condition=False) :
    LogHelperHelper.printMessageLog(LOG,message,condition=condition)

def printSuccess(message,condition=False) :
    LogHelperHelper.printMessageLog(SUCCESS,message,condition=condition)

def printSetting(message,condition=False) :
    LogHelperHelper.printMessageLog(SETTING,message,condition=condition)

def printDebug(message,condition=False) :
    LogHelperHelper.printMessageLog(DEBUG,message,condition=condition)

def printWarning(message,condition=False) :
    LogHelperHelper.printMessageLog(WARNING,message,condition=condition)

def printWarper(message,condition=False) :
    LogHelperHelper.printMessageLog(WRAPPER,message,condition=condition)

def printFailure(message,condition=False) :
    LogHelperHelper.printMessageLog(FAILURE,message,condition=condition)

def printError(message,condition=False) :
    LogHelperHelper.printMessageLog(ERROR,message,condition=condition)

def prettyPython(
        origin,
        message,
        dictionaryInstance,
        quote=c.SINGLE_QUOTE,
        tabCount=0,
        nullValue=c.NONE,
        trueValue=c.TRUE,
        falseValue=c.FALSE,
        logLevel=LOG
    ) :
    stdout, stderr = EnvironmentHelper.getCurrentSoutStatus()
    prettyPythonValue = StringHelper.prettyPython(
        dictionaryInstance,
        quote=quote,
        tabCount=tabCount,
        nullValue=nullValue,
        trueValue=trueValue,
        falseValue=falseValue,
        withColors=SettingHelper.activeEnvironmentIsLocal()
    )
    LogHelperHelper.softLog(origin, f'{message}{c.COLON_SPACE}{prettyPythonValue}', logLevel)
    EnvironmentHelper.overrideSoutStatus(stdout, stderr)

def prettyJson(
        origin,
        message,
        dictionaryInstance,
        quote=c.DOUBLE_QUOTE,
        tabCount=0,
        nullValue=c.NULL_VALUE,
        trueValue=c.TRUE_VALUE,
        falseValue=c.FALSE_VALUE,
        logLevel=LOG
    ) :
    stdout, stderr = EnvironmentHelper.getCurrentSoutStatus()
    prettyJsonValue = StringHelper.prettyJson(
        dictionaryInstance,
        quote=quote,
        tabCount=tabCount,
        nullValue=nullValue,
        trueValue=trueValue,
        falseValue=falseValue,
        withColors=SettingHelper.activeEnvironmentIsLocal()
    )
    LogHelperHelper.softLog(origin, f'{message}{c.COLON_SPACE}{prettyJsonValue}', logLevel)
    EnvironmentHelper.overrideSoutStatus(stdout, stderr)
