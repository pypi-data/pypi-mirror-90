from numbers import Number
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import ObjectHelper, StringHelper

def newLine(strReturn, charactere, withColors):
    if charactere == strReturn[-len(charactere):] :
        return f'{c.NEW_LINE}'
    else :
        return f'{getItAsColoredString(c.COMA, withColors, color=c.COMA_PROMPT_COLOR)}{c.NEW_LINE}'

def getValueCollection(outterValue) :
    return outterValue if not isinstance(outterValue, set) else ObjectHelper.getSortedCollection(outterValue)

def getItAsColoredString(thing, withColors, replaceBy=None, color=None) :
    thingValue = str(thing) if ObjectHelper.isNone(replaceBy) else str(replaceBy)
    colorValue = color if ObjectHelper.isNotNone(color) else c.NATIVE_PROMPT_COLOR[type(thing).__name__]
    return thingValue if not withColors else f'{colorValue}{thingValue}{c.RESET_COLOR}'

def getFilteredAndColoredString(keyOrValue, string, pretyFunction, withColors, color) :
    if ObjectHelper.isNativeClassIsntance(keyOrValue) and not isinstance(keyOrValue, str) :
        return c.NOTHING if pretyFunction == StringHelper.prettyPython else getItAsColoredString(string, withColors, color=color)
    return getItAsColoredString(string, withColors, color=color)

def getStrReturn(
        key,
        value,
        collectionType,
        quote,
        pretyFunction,
        tabCount,
        nullValue,
        trueValue,
        falseValue,
        withColors
    ) :
    if c.TYPE_DICT == collectionType :
        filteredAndColoredQuote = getFilteredAndColoredString(key, quote, pretyFunction, withColors, c.QUOTE_PROMPT_COLOR)
        filteredAndColoredColonSpace = getItAsColoredString(c.COLON_SPACE, withColors, color=c.COLON_PROMPT_COLOR)
        return f'{tabCount * c.TAB}{filteredAndColoredQuote}{getItAsColoredString(key, withColors)}{filteredAndColoredQuote}{filteredAndColoredColonSpace}{pretyFunction(value, quote=quote, tabCount=tabCount, nullValue=nullValue, trueValue=trueValue, falseValue=falseValue, withColors=withColors)}'
    else :
        return f'{tabCount * c.TAB}{pretyFunction(value, quote=quote, tabCount=tabCount, nullValue=nullValue, trueValue=trueValue, falseValue=falseValue, withColors=withColors)}'

def prettyInstance(
        outterValue,
        quote,
        pretyFunction,
        tabCount,
        nullValue,
        trueValue,
        falseValue,
        withColors=False
    ) :
    strReturn = c.NOTHING
    filteredAndColoredQuote = getFilteredAndColoredString(outterValue, quote, pretyFunction, withColors, c.QUOTE_PROMPT_COLOR)
    if (isinstance(outterValue, int) or isinstance(outterValue, float)) and not isinstance(outterValue, bool) :
        strReturn += getItAsColoredString(outterValue, withColors)
    elif isinstance(outterValue, bool) :
        if True == outterValue:
            strReturn += getItAsColoredString(outterValue, withColors, replaceBy=trueValue)
        elif False == outterValue:
            strReturn += getItAsColoredString(outterValue, withColors, replaceBy=falseValue)
    elif outterValue is None :
        strReturn += getItAsColoredString(outterValue, withColors, replaceBy=nullValue, color=c.NONE_PROMP_COLOR)
    else :
        strReturn += f'{filteredAndColoredQuote}{getItAsColoredString(outterValue, withColors)}{filteredAndColoredQuote}'
    return strReturn

def prettyCollection(
        outterValue,
        collectionType,
        quote,
        pretyFunction,
        tabCount,
        nullValue,
        trueValue,
        falseValue,
        withColors=False
    ) :
    openCollection = c.COLLECTION_TYPE[collectionType][c.OPEN_COLLECTION][withColors]
    closeCollection = c.COLLECTION_TYPE[collectionType][c.CLOSE_COLLECTION][withColors]
    strReturn = c.NOTHING
    if len(outterValue) == 0 :
        strReturn += f'{openCollection}{closeCollection}'
    else :
        strReturn += openCollection
        tabCount += 1
        if isinstance(outterValue, dict) :
            for key,value in outterValue.items() :
                strReturn += newLine(strReturn, openCollection, withColors)
                strReturn += getStrReturn(key, value, collectionType, quote, pretyFunction, tabCount, nullValue, trueValue, falseValue, withColors)
        else :
            for value in outterValue :
                strReturn += newLine(strReturn, openCollection, withColors)
                strReturn += getStrReturn(None, value, collectionType, quote, pretyFunction, tabCount, nullValue, trueValue, falseValue, withColors)
        strReturn += c.NEW_LINE
        tabCount -= 1
        strReturn += f'{tabCount * c.TAB}{closeCollection}'
    return strReturn

def isNotOneLineLongString(quoteType, thing) :
    if isinstance(thing, str) and isinstance(quoteType, str) and quoteType in [c.TRIPLE_SINGLE_QUOTE, c.TRIPLE_DOUBLE_QUOTE] :
        return not 0 == thing.count(quoteType) % 2
    else :
        return True
