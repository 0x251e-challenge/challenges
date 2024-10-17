print()
print("=== rruussttyy R0tAT10nN ===")
print()
print("Give me the flag i'll give you points ;)")
print()
print("flag: " ,end="")

flag=input()
out= ""

for i in range(len(flag)):
  out=out+chr(ord(flag[i]) - (i+3))

if out=="@PAukjliihlD@D0b6[Yg":
  print("correct! +999 points")

else:
  print("wrong! try again --_--)")

