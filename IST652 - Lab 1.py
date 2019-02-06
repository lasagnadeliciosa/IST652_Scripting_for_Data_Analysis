#!/usr/bin/env python
# coding: utf-8

# # IST 652 Lab #1
# ### Instructions
# - Complete all 6 questions in this assignment.
# - You may work with others, <b> but the work you submit must be your own </b>. You can differentiate your work by adding comments or changing the values you use to test your code. However, submitting some else's work as your own is an academic integrity violation and will be raised to academic affairs.
# - It is always better to attempt a problem as partial credit may be granted.
#
#
# ### Submission Guide:
# - Submit your answers on BlackBoard by Saturday 2019-02-02.
# - The file must be either a .py or .ipynb file type.
# - The name of the file should be <i> ist652_lab1_lastname.py (.ipynb) </i> .
#
#
# ### Grading [ 6 total points ]
# For Each Question, the following credit will be awarded:
# - 0.75 for printing the correct answer to the console.
# - 0.15 for approaching the problem efficiently.
# - 0.05 for properly documenting and commenting your code.

# ---
# ### Questions

# #### ( 1 ) Write the following code and retrun <i>x</i> using the print function. What does it return and why?
# - x = 11110
# - x = x+1
#
# ##### [1 point]

# In[2]:


# Enter your code here, printing relevant answers to console:
x = 11110
x = x+1
print(x)

#It returns 11111 as the output because the new x is the addition of the old x(11110) + 1.


# ----
# #### ( 2 ) Assume that we execute the following assignment statements:
# - width = 17
# - height = 12.0
#
# #### For each of the following expressions, print the value of the expression and its data type.
# -  width / 2
# -  width / 2.0
# -  height * 2
# -  height / 2.0
# -  width / height
#
#
# ##### [1 point]

# In[15]:


# Enter your code here, printing relevant answers to console:
width = 17
height = 12.0

print(width/2)
print(type(width/2))
print(width/2.0)
print(type(width/2.0))
print(height*2)
print(type(height*2))
print(height/2.0)
print(type(height/2.0))
print(width/height)
print(type(width/height))


# ---
# #### ( 3 ) Write a sequence of statements which <u><i>prompt</i></u> the user for hours and rate per hour, printing each one, and then to computing gross pay as:
# - ( hours * rate )
#
# #### Your output lines should look something like:
# - Enter Hours: 35
# - Enter Rate: 2.75
# - Pay: 96.25
#
#
# ##### [1 point]

# In[26]:


# Enter your code here, printing relevant answers to console:
try:
    x = int(input("Enter Hours: "))
    y = float(input("Enter Rates: "))
    print("Pay: " + str(x*y))
except:
    print("please enter a number")


#  ----

# #### ( 4 ) Rewrite your pay computation <i><u>(#3)</u></i> to give the employee 1.5 times the hourly rate for hours worked above 40 hours.
# #### For example:
# - Hours: 45
# - Rate: 10
# - Pay: 475.0
#
#
# ##### [1 point]

# In[2]:


# Enter your code here, printing relevant answers to console:
try:
    x = int(input("Hours: "))
    y = int(input("Rate: "))
    if x > 40:
        print("Pay: "+str((40*y)+((x-40)*1.5*y)))
    else:
        print("Pay: "+str(x*y))
except:
    print("please enter a number")



# ---
#
# #### ( 5 ) Suppose that there is a list of strings defined, called samples. Define the list so that some strings have only 1 or 2 characters and some strings have more.  Write a loop that prints out all the strings whose length is greater than 2.
#
# Nake up a list then write your loop to use the list samples, for example:
#
#    <i> samples = [‘at’, ‘bat’, ‘c’, . . . .  ]  </i>
#
# Submit your list, your code and an example run.
#
#
# ##### [1 point]

# In[16]:


# Enter your code here, printing relevant answers to console:
a =[]
samples = ['at', 'milk', 'he', 'it', 'z', 'chocolate', 'cookies']
for i in samples:
    if len(i) > 2:
        a.append(i)

print(a)


# #### ( 6 ) Again suppose that there is a list of strings defined, called samples.  Define the list so that some strings have only 1 or 2 characters and some strings have <u>more than 5.</u>  Write a loop that prints out all the strings whose length is greater than 2 and whose length is less than 5.
#
# Make up a list then write your loop to use the list samples. For example:
#
# <i>samples = [‘at’, ‘book’, ‘c’, ‘dog’, ‘elephant’, . . .  ]</i>
#
# Submit your list, your code and an example run.
#
#
# ##### [1 point]

# In[18]:


# Enter your code here, printing relevant answers to console:
a = []
samples = ['he','eat', 'plum', 'o', 'cake', 'dinosaur', '!', 'computer']
for i in samples:
    if len(i) > 2 and len(i) < 5:
        a.append(i)

print(a)
