letters = ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']

def getDigitsAmount(value):
    return len(str(value))

    # 16 248 504 -> 16M
def getShortValueName(value):
    digitsAmount = getDigitsAmount(value)
    if digitsAmount < 5:
        return str(value)
    
    lettersIndex = int((digitsAmount - 1) / 3) - 1
    importantPart = digitsAmount - 3 * (lettersIndex + 1)

    return str(str(value)[0:importantPart]) + letters[lettersIndex]

    # 16 248 504 -> 16 248M
def getMiddleValueName(value):
    digitsAmount = getDigitsAmount(value)
    if digitsAmount < 4:
        return str(value)
    elif digitsAmount < 6:
        return str(value)[0 : digitsAmount-3] + ' ' + str(value)[digitsAmount-3 : digitsAmount]
    
    lettersIndex = int((digitsAmount - 1) / 3) - 2
    importantPart = digitsAmount - 3 * (lettersIndex + 1)

    return str(value)[0 : importantPart-3] + ' ' + str(value)[importantPart-3 : importantPart] + letters[lettersIndex]
