#!/usr/bin/env python
# coding: utf-8

# # Homework for the 15/10/21                                                                                                                                                                 Audrey Hyeans  
# 
# 
# ## 2nd question

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import signal


# In[54]:


#period
T = 1

#step delta 
#delta_t = 1/(10*f)

#parameter N
N=10

#time domain where the function is define
t = np.linspace(-1.5*T,1.5*T,100)

#frequence domain where the function is define
f = np.arange(-N,N+1,1)/T

# width 
L = 1*T
M = len(t)


# In[55]:


#I take off the zero value, otherwise it's not valid
f = f[f!=0]

# Square wave function
function=np.ones(t.size)

for i in range(t.size):
    if t[i]%T>T/2:
        function[i]=-1

#I create a meshgird in order to have 2 arrays of same dimensions
tt,ff = np.meshgrid(t,f)

#coefficients
c_n_squarre_wave = 0.5*(-1j * np.pi )*ff * (np.sinc(T*ff/2))**2

#Fourier_series
F_series = np.sum(c_n_squarre_wave * np.exp(1j * ff * 2* tt*np.pi/T ), axis=0)


#figure
fig, ax = plt.subplots(1,2,figsize = (15,5))

#plotting the coefs
ax[1].stem(f,np.imag(c_n_squarre_wave[:,0]))

#plotting the series

ax[0].plot(t,np.real(F_series),
           color='black',
           label='Partial sum')

ax[0].plot(t,function, 
           color='red',
           label = 'Square wave function' )

ax[0].set_title('Partial sum and the square wave function')
ax[0].set_xlabel('Time t')

ax[1].set_title('Coefficients c_n')
ax[1].set_xlabel('frequency f')

ax[0].grid()
ax[1].grid()
ax[0].legend(loc=4)
plt.show()


# ## Third question : shift F_series

# In[52]:


#parameter to change to have different shifted F_series
a=0.25

#shifted coefficients
c_n_s_w_shifted = c_n_squarre_wave*np.exp(-1j*2*np.pi*(ff/T)*a)

#shifted Fourier_series
F_series_shifted = np.sum(c_n_s_w_shifted*np.exp(1j*2*np.pi*ff*tt/T),axis=0)

#figure
f = plt.figure(figsize = (10,5))
plt.plot(t,function, 
           color='red',
           label = 'Square wave function')

plt.title('Square wave function with the shifted function')
plt.plot(t, F_series_shifted, '--b' )
plt.xlabel('time t')
plt.grid()
plt.show()


# In[ ]:




