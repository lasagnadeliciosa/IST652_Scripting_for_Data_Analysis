#!/usr/bin/env python
# coding: utf-8

# # IST 652 Lab #3
# ### Instructions
# - Complete all 5 questions in this assignment.
# - You may work with others, <b> but the work you submit must be your own </b>. You can differentiate your work by adding comments or changing the values you use to test your code. However, submitting some else's work as your own is an academic integrity violation and will be raised to academic affairs.
# - It is always better to attempt a problem as partial credit may be granted.
# 
# 
# ### Submission Guide:
# - Submit your answers on BlackBoard by Saturday 2019-02-16.
# - The file must be either a .py or .ipynb file type.
# - <i><span style="color:red">The name of the file you submit should be <i><b> ist652_lab3_lastname.py (.ipynb) </i></b>.</span>
# 
# 
# 
# ### Grading [ 6 total points ]
# For Each Questions (1-4), the following credit will be awarded:
# - 0.75 for printing the correct answer to the console.
# - 0.15 for approaching the problem efficiently.
# - 0.05 for properly documenting and commenting your code.
# 
# 
# For Question (5), the following credit will be awarded:
# - 1.75 for printing the correct answer to the console.
# - 0.15 for approaching the problem efficiently.
# - 0.05 for properly documenting and commenting your code.

# ---
# ### Questions

# ### For Questions 1 - 4, consider the following two dictionaries:

# In[13]:


stock = {
    "banana": 6,
    "apple": 0,
    "orange": 32,
    "pear": 15,
    "avacado": 3,
    "mango": 5
}
prices = {
    "banana": 4,
    "apple": 2,
    "orange": 1.5,
    "pear": 3,
    "avacado": 10,
    "mango": 1
}


# #### ( 1a ) Show the expression that fetches the value of the stock dictionary at the key <u><i>orange</u></i>.
# 
# #### ( 1b ) Show a statement that adds an item to the stock dictionary called "cherry" with some integer value AND that adds <i><u>cherry</u></i> to the prices dictionary with a numeric value. 
# - <i>Or pick your own fruit name.</i>
# 
# 
# ##### [1 point]

# In[14]:


# Enter your code here, printing relevant answers to console:
#1a
print(stock["orange"])

#1b
stock["cherry"] = 3
print("stock:", stock)
prices["cherry"] = 5
print("prices:", prices)


# ---
# #### ( 2 ) Write the code for a loop that iterates over the stock dictionary and prints each key and value. i.e.:
#     - print(key, value)
# 
# ##### [1 point]

# In[16]:


# Enter your code here, printing relevant answers to console:
for i in stock:
    print(i, stock[i]) #prints the fruit and number of stocks


#  ----

# #### ( 3 )  Suppose that we have a grocery list:
# groceries = ['apple', 'banana', 'pear']
# 
# #### Write the code that will sum the total number in stock for all the items in the groceries list and prints this value to console.
# 
# 
# ##### [1 point]

# In[17]:


# Enter your code here, printing relevant answers to console:
groceries = ['apple', 'banana', 'pear']
totalNumber = 0
for grocery in groceries:
    totalNumber += stock[grocery] #lookup grocery in stock dictionary and add the number of fruits in each iteration.

print('Total number of fruits:', totalNumber)


# #### ( 4 ) Write the code that can print out the total value of in-stock items. 
# #### This program can iterate over the stock dictionary and for each item and multiply the number in stock times the price of that item in the prices dictionary. 
# - This must include the items for <i><u>cherry</i></u> (or your equivalent from [1b]).
# 
# 
# ##### [1 point]

# In[19]:


# Enter your code here, printing relevant answers to console:
totalValue = 0
for fruit in stock:
    if fruit in prices: #check if fruit is in prices dictionary.
        totalValue += prices[fruit] * stock[fruit]
    else:
        print(fruit, "in stock, but not priced") #this will tell you what extra fruit you have that's not priced.
print('Tatal Value:', totalValue)


# ---

# ---

# #### ( 5 ) Given the number guessing code below, add <i>try</i> and <i>except</i> clauses such that:
# - If the user enters a string, then the following message appears:
#     - <i>"Sorry this is not a number. Try Again."</i>
# - Then the iteration jumps back to the beginning of the loop without having counted as a guess
# 
# #### [2 points]

# In[1]:


# Enter your code here, printing relevant answers to console:

import random
guessesTaken = 0


number = random.randint(1, 20)
print('I am thinking of a number between 1 and 20.')

while guessesTaken < 6:
    print('Take a guess.') # There are four spaces in front of print.
    try:
        guess = input()
        guess = int(guess)
    except:
        print("Sorry this is not a number. Try Again.")
        continue
        
    guessesTaken = guessesTaken + 1
    
    if guess < number:
        print('Your guess is too low.') # There are eight spaces in front of print.

    if guess > number:
        print('Your guess is too high.')
        
    if guess == number:
        break


if guess == number:
    guessesTaken = str(guessesTaken)
    print('Good job - You guessed my number in ' + guessesTaken + ' guesses!')

if guess != number:
    number = str(number)
    print('Nope. The number I was thinking of was ' + number)


# In[ ]:




