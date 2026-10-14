# Rama_Height = 1.3
# Raja_Height = 1.7

# if Rama_Height > Raja_Height:
#     print("Rama is Taller")
    
# else:
#     print('Raja is Taller')

total = float(input("Enter total purchase amount:"))
if total >= 1000:
    discount = total * 0.10
    final_amount = total-discount
    print("discount applied:", discount)
    print("Final Amount to pay:", final_amount)
else:
     print("no discount applied:")
     print("total discount:", total)
    