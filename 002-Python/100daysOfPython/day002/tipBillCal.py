# This is a tip and bill calculator - 
print("----- Welcome to the tip calculator -----")
bill_amt = float(input("What is the bill amount?\n$: "))
tip_percent = float(input("How much would you like to tip? \nPercent: "))
people = int(input("How many people to split the bill? \nPeople: "))

total = bill_amt + ((tip_percent/100) * bill_amt)
print(f"The total cost is {total} \nAnd each person should pay : {total/people}")