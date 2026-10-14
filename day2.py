p=1000
t=1
r=10
si =(p*t*r)/100
print("simple interest amount",si)

p=1000
t=2
r=10
ci=p*(1+r/100)**t-p
print("compound interest ", ci)

phy = 90
bio =80
eng = 90
avg =(phy+bio+eng)/3
print(avg)

a=10
b=20
print("before swapping")
print("a=",a)
print("b=",b)

a,b =b,a
print("after swapping")
print("a=",a)
print("b=",b)

num1 = int(input("enter number 1:"))
num2 =int(input("enter number 2:"))
print(num1+num2)