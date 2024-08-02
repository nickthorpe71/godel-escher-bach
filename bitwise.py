n1 = 42342
n2 = 12334

# AND
n3 = n1 & n2
# print(bin(n3)[2:])

# OR
n4 = n1 | n2
# print(bin(n4)[2:])

# XOR
n5 = n1 ^ n2
# print(bin(n5)[2:])

# NOT (~ doesn't negate correctly)
# print("0" + bin(0b1111111111111111 - n1)[2:])
# print(bin(n1)[2:])

# SHIFTS
number = 20
# print(bin(number))
number <<= 1 # Shift all bits of the number 1 to the left by adding 0 to the right
# print(bin(number))
number >>= 2
# print(bin(number))

# Shifting one to the left is the same as multiplying by 2
# Shifting two to the right is the same as dividing by 2

# -------- What are they used for? ------------

# Flags

# Read, Write, Execute, Change Policy
person1 = 0b1000 # Can only read
person2 = 0b1110 # Can do everything but change policy
person3 = 0b1010
person4 = 0b1100
person5 = 0b1111

# Use AND to check what the lowest permissions is
together1 = person1 & person2 & person3 & person4 & person5
# print(bin(together1))

# Use OR to check that at least one has the permission
together2 = person1 | person2 | person3 | person4 | person5
# print(bin(together2))

READ = 0b1000
WRITE = 0b0100
EXEC = 0b0010
CHANGE = 0b0001

def my_func(permission):
    print(bin(permission))

# my_func(WRITE | READ) # Use OR to combine permissions

# Swap Variables
a = 10
b = 20

a ^= b
b ^= a
a ^= b

print(a)
print(b)
