def reverse(s):
	str = ""
	for i in s:
		str = i + str
	return str
def Concat(str1,str2):  
    str3 = str1 + str2  
    return(str3)   # Printing the new combined string 

def slic(str4):
    str5 = slice(6)
    return(str5)


s = "MISSISSIPPI"
print("The original string is : ", end="")
print(s)
print("The reversed string is : ", end="")
print(reverse(s))


str1 = "Hello "  
str2 = "World"
print("String 1 : ", end="")
print(str1)
print("String 2 : ", end="")
print(str2)
print("The concatenated string is : ", end="")
print(Concat(str1,str2))


text = 'Hello World'
print("The original string is : ", end="")
print(text)
print("The sliced string: ",end="")
print(text[slic(text)])

