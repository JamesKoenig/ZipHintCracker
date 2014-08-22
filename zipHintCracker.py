import os
import json

zipExecDir = "C:\\Program Files\\7-Zip"

#tests a password on a given zip file
def testPwd(filepath, pwd):
    return (os.system("7z t -p"+pwd+" "+filepath) == 0)
	
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
		if(char.isalpha()):
			yield char.upper()
			yield char.lower()
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


os.chdir(zipExecDir)
print("program loaded, I hope you're in interactive mode")
os.system("pause")
