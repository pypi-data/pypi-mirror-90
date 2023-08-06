import traceback
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import LogHelper, SettingHelper, ObjectHelper

FIRST_LAYER_COLOR = 'FIRST_LAYER_COLOR'
SECOND_LAYER_COLOR = 'SECOND_LAYER_COLOR'
LOG_TEXT = 'LOG_TEXT'

LEVEL_DICTIONARY = {
    LogHelper.LOG : {
        FIRST_LAYER_COLOR : c.BRIGHT_BLACK,
        SECOND_LAYER_COLOR: c.BRIGHT_BLACK,
        LOG_TEXT : c.LOG
    },
    LogHelper.SUCCESS : {
        FIRST_LAYER_COLOR : c.DARK_GREEN,
        SECOND_LAYER_COLOR: c.BRIGHT_GREEN,
        LOG_TEXT : c.SUCCESS
    },
    LogHelper.SETTING : {
        FIRST_LAYER_COLOR : c.DARK_BLUE,
        SECOND_LAYER_COLOR: c.BRIGHT_BLUE,
        LOG_TEXT : c.SETTING
    },
    LogHelper.DEBUG : {
        FIRST_LAYER_COLOR : c.DARK_CYAN,
        SECOND_LAYER_COLOR: c.BRIGHT_CYAN,
        LOG_TEXT : c.DEBUG
    },
    LogHelper.WARNING : {
        FIRST_LAYER_COLOR : c.DARK_YELLOW,
        SECOND_LAYER_COLOR: c.BRIGHT_YELLOW,
        LOG_TEXT : c.WARNING
    },
    LogHelper.WRAPPER : {
        FIRST_LAYER_COLOR : c.BRIGHT_WHITE,
        SECOND_LAYER_COLOR: c.DARK_WHITE,
        LOG_TEXT : c.WRAPPER
    },
    LogHelper.FAILURE : {
        FIRST_LAYER_COLOR : c.DARK_MAGENTA,
        SECOND_LAYER_COLOR: c.BRIGHT_MAGENTA,
        LOG_TEXT : c.FAILURE
    },
    LogHelper.ERROR : {
        FIRST_LAYER_COLOR : c.DARK_RED,
        SECOND_LAYER_COLOR: c.BRIGHT_RED,
        LOG_TEXT : c.ERROR
    }
}

def getStatus(level) :
    status = LogHelper.LOG_HELPER_SETTINGS.get(level)
    return status if not status is None and isinstance(status, str) else c.TRUE

def levelStatusError(method, level) :
    error(method,f'"{level}" log level status is not properly defined: {getStatus(level)}',None)

def getColors(level) :
    if SettingHelper.activeEnvironmentIsLocal() :
        firstLayerColor = LEVEL_DICTIONARY.get(level).get(FIRST_LAYER_COLOR) if LEVEL_DICTIONARY.get(level) and LEVEL_DICTIONARY.get(level).get(FIRST_LAYER_COLOR) else c.NOTHING
        secondLayerColor = LEVEL_DICTIONARY.get(level).get(SECOND_LAYER_COLOR) if LEVEL_DICTIONARY.get(level) and LEVEL_DICTIONARY.get(level).get(SECOND_LAYER_COLOR) else c.NOTHING
        tirdLayerColor = c.MUTTED_COLOR if c.MUTTED_COLOR else c.NOTHING
        resetColor = c.RESET_COLOR if c.RESET_COLOR else c.NOTHING
    else :
        firstLayerColor = c.NOTHING
        secondLayerColor = c.NOTHING
        tirdLayerColor = c.NOTHING
        resetColor = c.NOTHING
    return (firstLayerColor, secondLayerColor, tirdLayerColor, resetColor) if not firstLayerColor is None and not firstLayerColor == c.NOTHING else (c.NOTHING, c.NOTHING, c.NOTHING, c.NOTHING)

def softLog(origin,message,level,exception=None) :
    if ObjectHelper.isNotNone(exception) :
        hardLog(origin,message,exception,level)
    elif c.TRUE == getStatus(level) :
        firstLayerColor, secondLayerColor, tirdLayerColor, resetColor = getColors(level)
        if not origin or origin == c.NOTHING :
            classPortion = c.NOTHING
        else :
            classPortion = f'{tirdLayerColor}{origin.__name__}{c.COLON_SPACE}{resetColor}'
        print(f'{firstLayerColor}{LEVEL_DICTIONARY[level][LOG_TEXT]}{classPortion}{secondLayerColor}{message}{resetColor}')
    elif not c.FALSE == getStatus(level) :
        levelStatusError(method, level)

def hardLog(origin,message,exception,level) :
    if c.TRUE == getStatus(level) :
        firstLayerColor, secondLayerColor, tirdLayerColor, resetColor = getColors(level)
        if not origin or origin == c.NOTHING :
            classPortion = c.NOTHING
        else :
            classPortion = f'{tirdLayerColor}{origin.__name__}{c.COLON_SPACE}{resetColor}'
        if not exception or exception == c.NOTHING :
            errorPortion = c.NOTHING
        else :
            errorPortion = f'{firstLayerColor}{c.DOT_SPACE_CAUSE}{secondLayerColor}{str(exception)}{c.NEW_LINE}{tirdLayerColor}{traceback.format_exc()}{resetColor}'
        print(f'{firstLayerColor}{LEVEL_DICTIONARY[level][LOG_TEXT]}{classPortion}{secondLayerColor}{message}{errorPortion}{resetColor}')
    elif not c.FALSE == getStatus(level) :
        levelStatusError(method, level)

def printMessageLog(level,message,condition=False) :
    if condition :
        print(f'{Constant.TAB}{LEVEL_DICTIONARY[level][LOG_TEXT]}{message}')

# FORE_SIMPLE_RESET_COLOR = colorama.Fore.RESET
# LEVEL_DICTIONARY = {
#     SUCCESS : {
#         FIRST_LAYER_COLOR : colorama.Fore.GREEN,
#         SECOND_LAYER_COLOR: colorama.Fore.GREEN + colorama.Style.BRIGHT
#     },
#     SETTING : {
#         FIRST_LAYER_COLOR : colorama.Fore.BLUE,
#         SECOND_LAYER_COLOR: colorama.Fore.BLUE + colorama.Style.BRIGHT
#     },
#     DEBUG : {
#         FIRST_LAYER_COLOR : colorama.Fore.CYAN,
#         SECOND_LAYER_COLOR: colorama.Fore.CYAN + colorama.Style.BRIGHT
#     },
#     WARNING : {
#         FIRST_LAYER_COLOR : colorama.Fore.YELLOW,
#         SECOND_LAYER_COLOR: colorama.Fore.YELLOW + colorama.Style.BRIGHT
#     },
#     WRAPPER : {
#         FIRST_LAYER_COLOR : colorama.Fore.WHITE + colorama.Style.BRIGHT,
#         SECOND_LAYER_COLOR: colorama.Fore.WHITE
#     },
#     FAILURE : {
#         FIRST_LAYER_COLOR : colorama.Fore.MAGENTA,
#         SECOND_LAYER_COLOR: colorama.Fore.MAGENTA + colorama.Style.BRIGHT
#     },
#     ERROR : {
#         FIRST_LAYER_COLOR : colorama.Fore.RED,
#         SECOND_LAYER_COLOR: colorama.Fore.RED + colorama.Style.BRIGHT
#     }
# }

# def print_format_table():
#     """
#     prints table of formatted text format options
#     """
#     for style in range(8):
#         for fg in range(30,38):
#             s1 = ''
#             for bg in range(40,48):
#                 format = ';'.join([str(style), str(fg), str(bg)])
#                 s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
#             print(s1)
#         print('\n')
#
# print_format_table()
#
# x = 0
# for i in range(24):
#   colors = ""
#   for j in range(5):
#     code = str(x+j)
#     colors = colors + "\33[" + code + "m\\33[" + code + "m\033[0m "
#   print(colors)
#   x=x+5
