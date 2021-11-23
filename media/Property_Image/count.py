#Write a program to input text from user. Count the number of words in the input. Also, count the number of words starting with vowels and consonants. Use Dictionary.

counts = dict()
line = input("\nEnter the line:")
words = line.split()

print("\nWords : ",words)

v = 0
c = 0
d = 0

for i in range(0, len(line)):
    ch = line[i]
 
    if ( (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z') ):
        ch = ch.lower()        
        if (ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u'):
            v += 1
        else:
            c += 1
    elif (ch >= '0' and ch <= '9'):
        d += 1
    

print("\nToatl number of words : ",len(line.split()))
print("Toatl number of vowels : ",v)
print("Toatl number of constants : ",c)
print("Toatl number of digits : ",d)

print("\nCounting words : ")
for word in words:
    counts[word] = counts.get(word,0) + 1
print("Counts : ",counts)

vow = "aeiou"
constant = "qwrtypsdfghjklzxcvbnm"
digit = "0123456789"
#special =  = " !#$%&'()*+,-./:;<=>?@[\]^_`{|}~""

vowels = []
constants = []
digits = []
for sub in words:
    flag = 0
      
    # checking for begin char
    for ele in vow:
        if sub.startswith(ele):
            flag = 1
            break
    
    if (flag==1):
        vowels.append(sub)
        
    for ele in constant:
        if sub.startswith(ele):
            flag = 2
            break
    
    if (flag==2):
        constants.append(sub)
        
    for ele in digit:
        if sub.startswith(ele):
            flag = 3
            break
    
    if (flag==3):
        digits.append(sub)
        
print("\nWords starting with vowels : " + str(vowels))
print("Toatl number of words starting with vowels : ",len(vowels))

print("\nWords starting with constants : " + str(constants))
print("Toatl number of words starting with constants : ",len(constants))

print("\nWords starting with digits : " + str(digits))
print("Toatl number of words starting with digits : ",len(digits))

#print(counts)
