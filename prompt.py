#!/usr/bin/env python
# coding: utf-8

# ### Will a Customer Accept the Coupon?
# 
# **Context**
# 
# Imagine driving through town and a coupon is delivered to your cell phone for a restaraunt near where you are driving. Would you accept that coupon and take a short detour to the restaraunt? Would you accept the coupon but use it on a sunbsequent trip? Would you ignore the coupon entirely? What if the coupon was for a bar instead of a restaraunt? What about a coffee house? Would you accept a bar coupon with a minor passenger in the car? What about if it was just you and your partner in the car? Would weather impact the rate of acceptance? What about the time of day?
# 
# Obviously, proximity to the business is a factor on whether the coupon is delivered to the driver or not, but what are the factors that determine whether a driver accepts the coupon once it is delivered to them? How would you determine whether a driver is likely to accept a coupon?
# 
# **Overview**
# 
# The goal of this project is to use what you know about visualizations and probability distributions to distinguish between customers who accepted a driving coupon versus those that did not.
# 
# **Data**
# 
# This data comes to us from the UCI Machine Learning repository and was collected via a survey on Amazon Mechanical Turk. The survey describes different driving scenarios including the destination, current time, weather, passenger, etc., and then ask the person whether he will accept the coupon if he is the driver. Answers that the user will drive there ‘right away’ or ‘later before the coupon expires’ are labeled as ‘Y = 1’ and answers ‘no, I do not want the coupon’ are labeled as ‘Y = 0’.  There are five different types of coupons -- less expensive restaurants (under \\$20), coffee houses, carry out & take away, bar, and more expensive restaurants (\\$20 - \\$50). 

# **Deliverables**
# 
# Your final product should be a brief report that highlights the differences between customers who did and did not accept the coupons.  To explore the data you will utilize your knowledge of plotting, statistical summaries, and visualization using Python. You will publish your findings in a public facing github repository as your first portfolio piece. 
# 
# 
# 
# 

# ### Data Description
# Keep in mind that these values mentioned below are average values.
# 
# The attributes of this data set include:
# 1. User attributes
#     -  Gender: male, female
#     -  Age: below 21, 21 to 25, 26 to 30, etc.
#     -  Marital Status: single, married partner, unmarried partner, or widowed
#     -  Number of children: 0, 1, or more than 1
#     -  Education: high school, bachelors degree, associates degree, or graduate degree
#     -  Occupation: architecture & engineering, business & financial, etc.
#     -  Annual income: less than \\$12500, \\$12500 - \\$24999, \\$25000 - \\$37499, etc.
#     -  Number of times that he/she goes to a bar: 0, less than 1, 1 to 3, 4 to 8 or greater than 8
#     -  Number of times that he/she buys takeaway food: 0, less than 1, 1 to 3, 4 to 8 or greater
#     than 8
#     -  Number of times that he/she goes to a coffee house: 0, less than 1, 1 to 3, 4 to 8 or
#     greater than 8
#     -  Number of times that he/she eats at a restaurant with average expense less than \\$20 per
#     person: 0, less than 1, 1 to 3, 4 to 8 or greater than 8
#     -  Number of times that he/she goes to a bar: 0, less than 1, 1 to 3, 4 to 8 or greater than 8
#     
# 
# 2. Contextual attributes
#     - Driving destination: home, work, or no urgent destination
#     - Location of user, coupon and destination: we provide a map to show the geographical
#     location of the user, destination, and the venue, and we mark the distance between each
#     two places with time of driving. The user can see whether the venue is in the same
#     direction as the destination.
#     - Weather: sunny, rainy, or snowy
#     - Temperature: 30F, 55F, or 80F
#     - Time: 10AM, 2PM, or 6PM
#     - Passenger: alone, partner, kid(s), or friend(s)
# 
# 
# 3. Coupon attributes
#     - time before it expires: 2 hours or one day

# In[79]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


# ### Problems
# 
# Use the prompts below to get started with your data analysis.  
# 
# 1. Read in the `coupons.csv` file.
# 
# 
# 

# In[80]:


data = pd.read_csv('C:\\Users\Lisha\Downloads\coupons.csv')


# In[81]:


data.head()


# 2. Investigate the dataset for missing or problematic data.

# In[103]:


data.count()
data.info()


# In[111]:


#updating the age column so that the conversion to int can be done for these two columns
data.loc[data['age'] == 'below21','age'] = '20'
data.loc[data['age'] == '50plus','age'] = '51'
data['age'].value_counts()


# In[112]:


data['income'].value_counts()


# In[113]:


#finidng the sum of missing rows for each column
missing_data = data.isnull().sum()
print(missing_data)


# 3. Decide what to do about your missing data -- drop, replace, other...

# In[114]:


#As we saw in the above results the more tha 90% of rows in car column are blank and based on our questions 
#I don't see any relevance of car coumn value in the final results and hence dropping the car column from the datset.
update_data = data.drop('car',axis=1)
update_data.count()


# In[115]:


#updating the values as 'Never' in columns RestaurantLessThan20 and Restaurant20To50 , 
#Assuming empty rows means there were no visits to those restuarnsts .
update_data["RestaurantLessThan20"].fillna('never', inplace = True)
update_data["Restaurant20To50"].fillna('never', inplace = True)
update_data.count()

#Assuming the same for columns Bar,CoffeeHouse,CarryAway , updating the empty rows with Never
update_data["Bar"].fillna('never', inplace = True)
update_data["CoffeeHouse"].fillna('never', inplace = True)
update_data["CarryAway"].fillna('never', inplace = True)
update_data.count()


# 4. What proportion of the total observations chose to accept the coupon? 
# 
# 

# In[116]:


accept_coupon = update_data.query('Y == 1')['Y'].count()/update_data['Y'].count()
print(accept_coupon.round(2),"is the proporation of the total observations chose to accept the coupon")


# 5. Use a bar plot to visualize the `coupon` column.

# In[117]:


update_data.groupby('coupon')['coupon'].count().plot(kind = 'bar')
plt.xlabel("Coupon types")
plt.ylabel("Number of Coupons")
plt.title('Coupons')


# 6. Use a histogram to visualize the temperature column.

# In[118]:


sns.histplot(data=update_data, x="temperature",bins = 5)


# In[119]:


#visualizing the temperature column with coupons
sns.histplot(data=update_data, x="temperature",bins = 5,hue = 'coupon')


# **Investigating the Bar Coupons**
# 
# Now, we will lead you through an exploration of just the bar related coupons.  
# 
# 1. Create a new `DataFrame` that contains just the bar coupons.
# 

# In[120]:


data_bar_coupons = update_data.query('coupon in ("Bar")')
data_bar_coupons.head(10)


# 2. What proportion of bar coupons were accepted?
# 

# In[121]:


accept_bar_coupon_ratio = data_bar_coupons.query('Y == 1')['Y'].count()/data_bar_coupons['Y'].count()
print(accept_bar_coupon_ratio.round(2),"is the proporation of the bar coupons that were acceped")


# 3. Compare the acceptance rate between those who went to a bar 3 or fewer times a month to those who went more.
# 

# In[122]:


#the below doesn't include where there were no visists to the Bar
accept_bar_coupon = data_bar_coupons.query('Y == 1')
acceptance_rate_less3 = accept_bar_coupon.query("Bar in ('less1','1~3')")['Bar'].count()/accept_bar_coupon['Bar'].count()
print(acceptance_rate_less3, "is the acceptance rate for those who visited less than 3 time")
acceptance_rate_more3 = accept_bar_coupon.query("Bar in ('gt8','4~8')")['Bar'].count()/accept_bar_coupon['Bar'].count()
print(acceptance_rate_more3,"is the acceptance rate for those visited more than 3 times")


# 4. Compare the acceptance rate between drivers who go to a bar more than once a month and are over the age of 25 to the all others.  Is there a difference?
# 

# In[123]:


#the below doesn't include where there were no visists to the Bar- 
#Empty rows were tagged as never in previous assumption,those rows will aso be included.
acceptance_rate_more_than1_age_25 = accept_bar_coupon.loc[accept_bar_coupon['age'].astype('int') > 25].query("Bar not in ('never','less1',0)")['Bar'].count()/accept_bar_coupon['Bar'].count()
print(acceptance_rate_more_than1_age_25, "is the acceptance rate for those who who go to a bar more than once a month and are over the age of 25")


# 5. Use the same process to compare the acceptance rate between drivers who go to bars more than once a month and had passengers that were not a kid and had occupations other than farming, fishing, or forestry. 
# 

# In[124]:


acceptance_rate_more_than1_age_25 = accept_bar_coupon.query("Bar not in ('never','less1',0) and passanger not in ('Kid(\s)\') and occupation not in ('farming','fishing','forestry')")['Bar'].count()/accept_bar_coupon['Bar'].count()
print(acceptance_rate_more_than1_age_25, "is the acceptance rate for those who go to bars more than once a month and had passengers that were not a kid and had occupations other than farming, fishing, or forestry")


# 6. Compare the acceptance rates between those drivers who:
# 
# - go to bars more than once a month, had passengers that were not a kid, and were not widowed *OR*
# - go to bars more than once a month and are under the age of 30 *OR*
# - go to cheap restaurants more than 4 times a month and income is less than 50K. 
# 
# 

# In[126]:


df_nokid_widowed = accept_bar_coupon.loc[accept_bar_coupon['passanger'] != 'Kid(s)'].query("maritalStatus not in ['Widowed'] and Bar not in('never','less1',0)")
df_age30 = accept_bar_coupon.loc[accept_bar_coupon['age'].astype('int') <30].query("Bar not in('never','less1',0)")
df_inless50k = accept_bar_coupon.query("RestaurantLessThan20 in ['4~8','gt8'] and income in ('$25000 - $37499','$12500 - $24999','$37500 - $49999','Less than $12500')")

df_nokid_widowed_rate = (df_nokid_widowed.shape[0] *100)/accept_bar_coupon.shape[0]
df_age30_rate = (df_age30.shape[0]*100)/accept_bar_coupon.shape[0]
df_inless50k_rate = (df_inless50k.shape[0]*100)/accept_bar_coupon.shape[0]

print(f"Attendance rate for drivers 'going to bars more than once a month, had passengers that were not a kid, and were not widowed' is {df_nokid_widowed_rate}%")
print(f"Attendance rate for drivers 'attending a Bar more than once a month under the age of 30' is {df_age30_rate}%")
print(f"Attendance rate for drivers 'going to cheap restaurants more than 4 times a month and income is less than 50K' is {df_inless50k_rate}%")


# 7.  Based on these observations, what do you hypothesize about drivers who accepted the bar coupons?

# Drivers with No kids or drivers under the age of 30 have higher probability of accpeting the bar coupon.
# Overall proportion of accepting the bar coupon is 41% .

# ### Independent Investigation
# 
# Using the bar coupon example as motivation, you are to explore one of the other coupon groups and try to determine the characteristics of passengers who accept the coupons.  

# In[ ]:


#Analyzing the Carry out & Take away coupons
Data_Carryout_takeaway = update_data.query("coupon in ('Carry out & Take away')")
Data_Carryout_takeaway_accept = update_data.query("coupon in ('Carry out & Take away') and Y == 1")
print(Data_Carryout_takeaway_accept.shape[0])


# In[131]:


#How many of the drivers accept the coupon for Carryout and take out
rate_of_acceptannce = Data_Carryout_takeaway_accept.shape[0]/Data_Carryout_takeaway.shape[0]
print(f"Drivers accept the coupon for Carryout and take out is {rate_of_acceptannce}")


# In[147]:


#analyzing how many drivers with kids prefer carrry out and take out 
accept_with_kids = Data_Carryout_takeaway_accept.query("passanger in ('Kid(s)')")
acccpet_with_kids_rate = accept_with_kids.shape[0]/Data_Carryout_takeaway_accept.shape[0]
print(f"Drivers with kids prefer carrry out and take out {acccpet_with_kids_rate}")


# In the above anaylsis , very few 6% of the people who accept the coupons for take away or carry out have kids with them

# In[149]:


Data_Carryout_takeaway['time'].value_counts()


# In[150]:


#Plotting the graph to see the Coupons sent and accepted based on time of the day 

sns.countplot(data = Data_Carryout_takeaway, x = "time", hue = "Y")
plt.xticks(rotation=45)
plt.title("Time of day impacting Coupon Acceptance Rate")
plt.xlabel("Time of the day")
plt.ylabel("Number of People")
plt.legend(title = "Coupon Accepted", labels = ["No", "Yes"])
plt.show()


# In[151]:


#Plotting the graph to see the Coupons sent and accepted based on passanger of the day 

sns.countplot(data = Data_Carryout_takeaway, x = "passanger", hue = "Y")
plt.xticks(rotation=45)
plt.title("passanger impacting Coupon Acceptance Rate")
plt.xlabel("passanger")
plt.ylabel("Number of People")
plt.legend(title = "Coupon Accepted", labels = ["No", "Yes"])
plt.show()


# In[152]:


#Plotting the graph to see the Coupons sent and accepted based on destination

sns.countplot(data = Data_Carryout_takeaway, x = "destination", hue = "Y")
plt.xticks(rotation=45)
plt.title("destination impacting Coupon Acceptance Rate")
plt.xlabel("destination")
plt.ylabel("Number of People")
plt.legend(title = "Coupon Accepted", labels = ["No", "Yes"])
plt.show()


# In[ ]:




