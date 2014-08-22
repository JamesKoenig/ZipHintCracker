from czipfile import ZipFile
import json
import os #for system("pause")

#tests a password on a given zip file
def testPwd(filepath, pwd, checkMethod=ZipFile.testzip):
    z = ZipFile(filepath, "r")
    z.setpassword(pwd)
    try:
        checkMethod(z)
        #if no exception was raised, it was the right password
        return True
    except RuntimeError as err:
        #if it's not the right password, intercept the runtime error
        if err[0] == 'Bad password for file':
            return False
        #the runtime error was not one we expected, re-raise it
        else:
            raise 
    
#test all elements in a table (or iterateable ;))
def testTable(filepath, table):
    for i in table:
        if testPwd(filepath, i):
            print("***RESULT FOUND***")
            print(i) #shows correct password for file
            return i
    return False

#generate a hash from a json file of possible substitution
def permHashFromFile(path):
    permHash = {}
    with open(path) as f:
        permHash = json.load(f)
    return permHash
	
def permuteCharacter(char, permHash):
	if(char): #as long as we're not dealing with "" (empty string)
		if(char.isalpha()):  #yield both cases of any alphabetical character
			yield char.upper()
			yield char.lower()
          #if the character is in the hash then run through all its members
		if(type(permHash.get(char)) == list):
			for perm in permHash.get(char):
				yield perm
	
def permuteString(string, permHash):
	char = string[:1]
	rest = string[1:]
	if(len(string)> 1):
		for permutation in permuteCharacter(char, permHash):
			for restPermutation in permuteString(rest, permHash):
				yield permutation+restPermutation
	else:
		for permutation in permuteCharacter(char, permHash):
			yield permutation


#os.chdir(zipExecDir)
print("program loaded, I hope you're in interactive mode")
os.system("pause")
