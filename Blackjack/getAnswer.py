def getAnsStr(question,txtArray):
    ans=input(question)
    while ans not in txtArray:
        print(f'Please respond with an answer in {txtArray}')
        ans=input(question)
    return ans
def getAnsFlt(question,limits=[None,None],error='Please respond with a valid number'):
    ans=''
    while True:
        ans=input(question)
        try:
            ans=float(ans)
        except ValueError:
            print(error)
            continue
        if limits is None:
            return ans
        else:
            if not (limits[0]<=ans<=limits[1]):
                print(f"Please enter a value between {limits[0]} and {limits[1]}")
            else:
                return ans
def getAnsInt(question,limits=[None,None],error='Please respond with a valid integer'):
    ans=''
    while True:
        ans=input(question)
        try:
            ans=int(ans)
        except ValueError:
            print(error)
            continue
        if limits is None:
            return ans
        else:
            if not (limits[0]<=ans<=limits[1]):
                print(f"Please enter a inter between {limits[0]} and {limits[1]}")
            else:
                return ans