from czipfile import ZipFile
import json
import os #for system("pause")

class zipHintCracker:
    def __init__(self, passCandidate, zipPath, hashPath):
        self.pwdHint       = passCandidate
        self.zipInfo       = ZipFile(zipPath, "r")
        self.substitutions = self.loadPermutations(hashPath)       
    
    #tests a password on a given zip file
    #FIXME: currently giving false positives, maybe switch libraries?
    def testPwd(self, pwd, checkMethod=ZipFile.testzip):
        self.zipInfo.setpassword(pwd)
        try:
            checkMethod(self.zipInfo)
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
    def testTable(self,table):
        for i in table:
            if self.testPwd(i):
                print("***RESULT FOUND***")
                print(i) #shows correct password for file
                return i
        return False
    
    #generate a hash from a json file of possible substitution
    def loadPermutations(path):
        permHash = {}
        with open(path) as f:
            permHash = json.load(f)
        return permHash

    #permute a given character based on a dictionary of known substitutions
    #   is a generator, so this function returns an iteratable object
    def permuteCharacter(self,char):
        if(char): #as long as we're not dealing with "" (empty string)
            if(char.isalpha()):  #yield both cases of any alphabetical character
                yield char.upper()
                yield char.lower()
          #if the character is in the hash then run through all its members
        if(type(self.substitutions.get(char)) == list):
            for perm in self.substitutions.get(char):
                yield perm

    #permute a given string based on a dictionary of known substitutions
    #   is a generator, so it's used in for loops
    def permuteString(self, string):
        char = string[:1]
        rest = string[1:]
        if(len(string)> 1):
            for permutation in self.permuteCharacter(char):
                for restPermutation in self.permuteString(rest):
                    yield permutation+restPermutation
        else:
            for permutation in self.permuteCharacter(char):
                yield permutation

print("program loaded, I hope you're in interactive mode")
os.system("pause")
