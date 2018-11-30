import random as r
import re
import time

with open('wordlist.txt') as f:
    wordlist = f.readlines()
## THE SORTING OF wordlist IS MANDATORY BECAUSE OF THE BINARY-SEARCH PROCESS
wordlist.sort() # nlogn

## EVALUATE THE INDEX WHERE THE CHARACTER IN THE wordlist IS ON THE VERGE TO ITS PREDECESSOR
def binarySearchStart(char, s, v):
    ## THE INDEX BETWEEN S AND V
    index = s+((v-s)//2)
    ## CONDITION MENTIONED ABOVE IS ACHIEVED OR IS AT THE VERY BEGINNING OF wordlist
    if index==0 or (char is wordlist[index][0] and wordlist[index][0] is not wordlist[index-1][0]):
        return index
    ## BASIC BINARY-SEARCH:
    if (char>wordlist[index][0]):
        return binarySearchStart(char, index, v)
    # NOTE: char = wordlist[index][0] BECAUSE IF char IS IN THE CORRECT RANGE ALEADY IT STILL IS SUPPOSED TO JUMP TO THE BEGINNING LEDGE
    elif (char<=wordlist[index][0]):
        return binarySearchStart(char, s, index)

def binarySearchEnd(char, s, v):
    index = s+((1+v-s)//2)
    if index >= len(wordlist)-1 or (wordlist[index][0] is not char and wordlist[index-1][0] is char):
        return index
    if (char>=wordlist[index][0]):
        return binarySearchEnd(char, index, v)
    elif (char<wordlist[index][0]):
        return binarySearchEnd(char, s, index)

## BASICALLY THE SAME ALGORITHM AS ABOVE, BUT EACH TIME A WORD GETS TWISTED ABOVE, IT GETS UNTWISTED HERE
def getStartEnd(letter):
    start = binarySearchStart(letter, 0, len(wordlist)-1)
    end = binarySearchEnd(letter, start, len(wordlist)-1)
    return (start, end)

## TWISTS AN INPUT WORD ARBITRARILY -- ONLY THE FIRST AND LAST CHARACTER STAY UNTOUCHED
def twistify(word):
    ## RANGING FROM THE FIRST TO SECOND-LAST AND MIXING THE LETTERS
    # NOTE: IF THE ARBITRARY INTEGERS ARE THE SAME NOTHING CHANGES
    ## -- WORDS MAY ACCIDENTALLY STAY THE SAME -- I DIDNOT SEE SPECIFICATION FOR THIS CASE SO I WILL IGNORE IT
    for i in range(1, len(word)-1):
        word=swap(r.randint(1, len(word)-2), r.randint(1, len(word)-2), word)
    return word

## WITH TWO INDICES AND AN INITIAL WORD -- THE ELEMENTS AT THE INDICES RESPECTIVELY SWAP
def swap(i,j,input):
    word=list(input)
    word[i],word[j]=word[j],word[i]
    return ''.join(word)

## INTAKING A PATH TO A TXT-FILE -- APPLY THE twistify-METHOD TO EACH WORD
def twistifySentence(path):
    result=[]
    startWord = False
    startSChar = False
    with open(path) as f:
        data = f.read()
    ## SEPARATING WORDS IN GERMAN.. (ARE THE ONLY ONES BEING TWISTED)
    words = re.findall(r"[a-zA-ZöÖüÜäÄß]+", data)
    ## ..FROM THE NON-READABLE CHARACTERS (I.E. NUMBERS, PUNCTUATION. ETC.)
    specialChars = re.findall(r"[^a-zA-ZöÖüÜäÄß]+", data)
    ## IF A WORD IS COMMENCING THE STRING THIS IS TRUE
    if len(words)>0:
        startWord = bool(re.match(words[0], data))
    ## VICE VERSA WITH specialChars
    if len(specialChars)>0:
        startSChar = bool(re.match(specialChars[0], data))
    ##  IF THE STRING BEGINS WITH A WORD
    ##  IT MEANS THAT THE LENGTH OF specialChars CAN ONLY SMALLER-OR-EQUAL TO THE LENGTH OF words
    if  startWord:
        for iter in range(0, len(specialChars)):
            result.append(twistify(words.pop(0))+specialChars.pop(0))
    ## VICE VERSA
    if startSChar:
        for iter in range(0, len(words)):
            result.append(specialChars.pop(0)+twistify(words.pop(0)))
    ## IF THERE ARE LEFT-OVER ELEMENTS THEY GET INSERTED HERE
    if len(words)>0:
        result.append(twistify(words.pop(0)))
    elif len(specialChars)>0:
        result.append(specialChars.pop(0))
    ## RETURN RESULT
    return ''.join(result)

## DETERMINES WETHER A TWISTED WORD IS IN THE wordlist DICTIONARY(IF FOUND => RETURNING IT)
def untwistify(twisted):
    ## ESTABLISHES IF THE FIRST LETTER IS UPPER-CASE (THIS WORD MAY NOT EXACTLY BE IN THE DICTIONARY IF IT IS 'SUBSTANTIVIERT')
    firstUpper = twisted[0].isupper()
    ## EVALUATE THE INTERVAL WHERE ALL THE WORDS WITH THE FIRST LETTER(IN LOWER CASE) LIE
    # BUG: chr(ord(...)) IS NECESARRY
    start, end = getStartEnd(chr(ord(twisted[0].lower())))
    ## ALL RESULTS WHERE THE FIRST- AND LAST CHARACTER ARE THE SAME AND LENGTHS CONCUR
    # NOTE: re.IGNORECASE -> BECAUSE THE OF THE SAME REASON FROM firstUpper
    possibleWords=[]
    for dictWord in range(start, end):
        match = re.findall(\
        r'\b'+twisted[0]+r'[a-zA-ZöÖüÜäÄß]{'+str(len(twisted)-2)+r'}'+twisted[len(twisted)-1]+r'\b'
        , wordlist[dictWord], re.IGNORECASE)
        if len(match)>0:
            possibleWords.append(match[0])
    ## SAME PROCESS AS ABOVE JUST IN CASE THE FIRST LETTER IS UPPER-CASE
    if firstUpper:
        start, end = getStartEnd(twisted[0])
        for dictWord in range(start, end):
            match = re.findall(\
            r'\b'+twisted[0]+r'[a-zA-ZöÖüÜäÄß]{'+str(len(twisted)-2)+r'}'+twisted[len(twisted)-1]+r'\b'
            , wordlist[dictWord])
            if len(match)>0:
                possibleWords.append(match[0])
    ## FOR EVERY word OUT OF THE possibleWords IT CHECKS WETHER THE FOLLOWING CONSTRAINTS APPLY
    for word in possibleWords:
        correctWord=True
        ## IN AN INTERVAL FROM THE SECOND TO SECOND-LAST CHARACTER
        for i in range(1, len(twisted)-1):
   ## IF A CHARACTER APPEARANCE DIFFERS IN EITEHR WORDS IT GETS EXCLUDED
            if  len(re.findall(twisted[i], twisted[1:len(twisted)-1])) is not len(re.findall(twisted[i], word[1:len(twisted)-1])):
                correctWord=False
                break
        ## IF IT DIDNOT BREAK IT CONNOTES THE word BEING CORRECT
        if correctWord:
            ## RAISES THE FIRST CHARACTER TO UPPER-CASE IF TEH INITIAL WORD WAS SO
            ## ALTHOUGH IF IT IS A NOUN AND ALREADY UPPER-CASE IT STILL ASURES FOR THE INFAMOUS 'SUBSTANTIVIER'-CASE
            if firstUpper:
                word = word[0].upper()+word[1:]
            ## RETURNS FOUND WORD
            return word
    ## THE WORD WAS NOT IN THE DICTIONARY AND GETS RETURNED UNALTERED
    return twisted

def untwistifySentence(path):
    result=[]
    startWord = False
    startSChar = False
    with open(path) as f:
        data = f.read()
    ## SEPARATING WORDS CONSISTING OF GERMAN CHARACTERS.. (ARE THE ONLY ONES BEING UNTWISTED)
    words = re.findall(r"[a-zA-ZöÖüÜäÄß]+", data)
    ## ..FROM THE NON-READABLE CHARACTERS (I.E. NUMBERS, PUNCTUATION. ETC.)
    specialChars = re.findall(r"[^a-zA-ZöÖüÜäÄß]+", data)
    ## IF A WORD IS COMMENCING THE STRING THIS IS TRUE
    if len(words)>0:
        startWord = bool(re.match(words[0], data))
    ## VICE VERSA WITH specialChars
    if len(specialChars)>0:
        startSChar = bool(re.match(specialChars[0], data))
    ##  IF THE STRING BEGINS WITH A WORD
    ##  IT MEANS THAT THE LENGTH OF specialChars CAN ONLY SMALLER-OR-EQUAL TO THE LENGTH OF words
    if  startWord:
        for iter in range(0, len(specialChars)):
            result.append(str(untwistify(words.pop(0)))+str(specialChars.pop(0)))
    ## VICE VERSA
    elif startSChar:
        for iter in range(0, len(words)):
            result.append(specialChars.pop(0)+untwistify(words.pop(0)))
    ## IF THERE ARE LEFT-OVER ELEMENTS THEY GET INSERTED HERE
    if len(words)>0:
        result.append(untwistify(words.pop(0)))
    elif len(specialChars)>0:
        result.append(specialChars.pop(0))
    ## RETURN RESULT
    return ''.join(result)

# ----------------------------------------------------- #
timeResult=""
for num in range(1, 8):
    start=time.time()
    with open("toUntwist/untwist"+str(num)+".txt", "w") as f:
        f.write(twistifySentence('toTwist/twist'+str(num)+'.txt'))
    with open("twistedUntwisted/twist"+str(num)+"_output.txt", "w") as f:
        f.write(untwistifySentence('toUntwist/untwist'+str(num)+'.txt'))
    end=time.time()
    timeResult+=("{} took {} amount of seconds\n".format(num, end-start))
with open("time.txt", "w") as timef:
    timef.write(timeResult)
