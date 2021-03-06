# -*- coding: utf-8 -*-
"""GA_Algorith.ipynb

####This libraries must be installed before to run
"""

import pandas as pd
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import math as math

"""###Fuctions"""

import pandas as pd
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import math as math
def col_row(Vector): 
  #Convert column vector in a row vector
  #input: shape(Vector)=n,
  #output:shape(Vector)=1,n
  v=np.zeros((1,len(Vector)))
  for i in range(0,len(Vector),1):
    v[0,i]=Vector[i]
  return v    

def vrand(y1,y2,Size):
  #Generate a random number between lower and upper limits
  ja=np.zeros((1,Size))
  nn,nna=np.shape(ja)
  for i in range(0,nna,1):
    ja[0,i]=y1*np.random.rand()+y2
  return ja

def pico(wi,wpi):
  dw_2=wi-wpi
  if wi<wpi:
    sigma=0.07
    dw3=math.exp(-((dw_2)**2)/((2*sigma**2)*wpi**2))
  if wi>wpi:
    sigma=0.09
    dw3=math.exp(-((dw_2)**2)/((2*sigma**2)*wpi**2))
  return dw3
def espectro(alfa_JH,wi,wpi,gamma_JH):
  z=pico(wi,wpi)
  Sw_JH=(alfa_JH*(9.81**2)*(2*3.1416)**-4*(wi)**-5)*(math.exp(-1.25*(wi/wpi)**-4))*(gamma_JH**z)
  return Sw_JH

def spectral_density(a,g,wi,wpi):
  spj=[]
  for x in range(0,len(wi),1):
    m=espectro(a,wi[x],wpi,g)
    spj.append(m)
  sp=pd.DataFrame(spj,columns=['SP'])
  return sp

def row_col(Vector): 
  #Convert row vector in a column vector
  #input: shape(Vector)=n,
  #output:shape(Vector)=1,n
  n,m=np.shape(Vector)
  v=np.zeros((m,1))
  for i in range(0,m,1):
    v[i,0]=Vector[0,i]
  return v    

def Jonswap(Hsig,Tp,iter,oo):
  #This function obtain the parameters alfa, gamma from the jonswap spectrum
  #for the calculation its necesary significant wave heigh and peak period data
  #iter: number of gamma population
  #oo: number of alpha population

  #Define angular wave frequencies in Hz
  w=np.arange(0.05,0.6+0.0125,0.0125)
  n=len(w)
  #Delta omega for spectrum integration in Hz
  domega=0.005 
  #gravity m/s2
  pi=3.1416
  g=9.81
  #Sigma constants from Jonswap spectrum
  sigma1=0.07
  sigma2=0.09
  #Alpha and Gamma limits From Jonswap spectrum
  a2=0  #Alpha
  a1=0.1 #Alpha
  y1=9 #Gamma
  y2=1 #Gama
  wp=1./Tp #Peak Frequency in Hz
  e=len(w)
  wi=np.zeros((len(wp),n))
  for i in range(0,len(wp),1):
    wi[i,:]=w
  wi=np.rot90(wi)
  wi=np.flipud(wi)
  wi=np.matlib.repmat(wi,iter,1) #Adjust in the requiered matrix form
  dw=np.zeros((len(wp),n))
  for j in range(0,len(wp),1):
    dw[j,:]=w-wp[j] #Diference between frequency spectrum and peak frequency in Hz
  dw=np.rot90(dw)
  dw=np.flipud(dw)
  dw_2=dw
  dw=np.matlib.repmat(dw,iter,1) #Adjust in the requiered matrix form
  a=0
  wpi=np.zeros((len(wp),n))
  for i in range(0,len(wp),1):
    wpi[i,:]=wp[a]
    a=a+1
  wpi=np.rot90(wpi)
  wpi=np.flipud(wpi)
  wpi=np.matlib.repmat(wpi,iter,1) #Adjust in the requiered matrix form
  aa,obj=np.shape(wpi)
  jj=int((aa*obj)/e)
  #Generate gamma random population
  gamma_JH=vrand(y1,y2,jj)
  gamma_JH=np.matlib.repmat(gamma_JH,e,1)
  gamma_JH_sel=col_row(gamma_JH[0,:])
  gamma_JH=np.reshape(gamma_JH,(aa,obj),'F')
  #Generate gamma random population
  alfa_JH=vrand(a1,a2,jj)
  alfa_JH=np.matlib.repmat(alfa_JH,e,1)
  alfa_JH_sel=col_row(alfa_JH[0,:])
  alfa_JH=np.reshape(alfa_JH,(aa,obj),'F')
  alfa_C=alfa_JH

  aa,bb=np.shape(gamma_JH)
  aa2=int(aa/2)
  #Cross the 50% of population for evolution process
  gamma_C=np.zeros((aa,bb))
  gamma_C[0:aa2-1,:]=gamma_JH[aa2+1:,:]
  gamma_C[aa2+1:,:]=gamma_JH[0:aa2-1,:]
  a,b=np.shape(dw_2)
  ss=int((b*iter)/2)
  dw3=np.zeros((a,b))
  for i in range(0,a,1):
    for j in range(0,b,1):
      if dw_2[i,j]<0:
        dw3[i,j]=math.exp(-((dw_2[i,j])**2)/(2*sigma2**2)*wpi[i,j]**2)
      if dw_2[i,j]>0:
        dw3[i,j]=math.exp(-((dw_2[i,j])**2)/(2*sigma1**2)*wpi[i,j]**2)
      if dw_2[i,j]==0:
        dw3[i,j]=0.0001
        dw3[i,j]=math.exp(-((dw_2[i,j])**2)/(2*sigma1**2)*wpi[i,j]**2)
  dw3=np.matlib.repmat(dw3,iter,1)
  nas,mas=np.shape(dw3)
  Sw_JH=np.zeros((nas,mas))
  for i in range(0,nas,1):
    for j in range(0,mas,1):
      Sw_JH[i,j]=(alfa_JH[i,j]*(g**2)*(2*pi)**-4*(wi[i,j])**-5)*(math.exp(-1.25*(wi[i,j]/wpi[i,j])**-4)*(gamma_JH[i,j]**(math.exp(-0.5*(wi[i,j]/(wpi[i,j]**-1)/dw3[i,j])**2))))
  Sw_JH=np.reshape(Sw_JH,(e,jj),'F')

  Sw_JH_C=np.zeros((nas,mas))
  for i in range(0,nas,1):
    for j in range(0,mas,1):
      Sw_JH_C[i,j]=(alfa_C[i,j]*(g**2)*(2*pi)**-4*(wi[i,j])**-5)*(math.exp(-1.25*(wi[i,j]/wpi[i,j])**-4)*(gamma_C[i,j]**(math.exp(-0.5*(wi[i,j]/(wpi[i,j]**-1)/dw3[i,j])**2))))
  Sw_JH_C=np.reshape(Sw_JH_C,(e,jj),'F')
  #Determine the firts moment via spectrum integration firts generation and crossed population
  m0=col_row(sum(Sw_JH)*domega)
  Hs=4.004*np.sqrt(m0[:])
  Hs2=np.reshape(Hs,(b,iter),'F')
  m0_C=col_row(sum(Sw_JH_C)*domega)
  Hs_C=4.004*np.sqrt(m0_C[:])
  Hs2_C=np.reshape(Hs_C,(b,iter),'F')
  nc,qq=np.shape(Sw_JH)
  #Validate maximun spectrum energy respect the significat wave heigh 
  Sw_max=np.zeros((1,qq))
  Sw_max_C=np.zeros((1,qq))
  for j in range(0,qq,1):
    Sw_max[0,j]=np.max(Sw_JH[:,j])
    Sw_max_C[0,j]=np.max(Sw_JH_C[:,j])
  dif_Sw_max=np.diff(Sw_max)
  dif_Hs=np.diff(Hs)
  dif_Sw_max_C=np.diff(Sw_max_C)
  dif_Hs_C=np.diff(Hs_C)
  #Check the correlation between the first derivative of significant wave heigh and maximum energy spectrum
  R=np.corrcoef(dif_Hs,dif_Sw_max)
  R_C=np.corrcoef(dif_Hs_C,dif_Sw_max_C)
  ee,rr=np.shape(Hs2)
  ee1,rr1=np.shape(gamma_JH_sel)
  #Realize the selection gamma and alfa for evolution process
  Hs_evol=np.zeros((ee,rr))
  gamma_evol=np.zeros((ee1,rr1))
  alfa_evol=np.zeros((ee1,rr1))
  gamma_JH_sel_C=np.zeros((1,int(b*iter)))
  gamma_JH_sel_C[0,0:ss]=gamma_JH_sel[0,ss:]
  gamma_JH_sel_C[0,ss:]=gamma_JH_sel[0,0:ss]
  alfa_JH_sel_C=alfa_JH_sel
  #Check the evolution population with respect to the correlation coefficient
  for i in range(0,obj,1):
    if R[0,1]<R_C[0,1]:
      Hs_evol[i,:]=Hs2[i,:]
      alfa_evol=alfa_JH_sel
      gamma_evol=gamma_JH_sel
    if R[0,1]>R_C[0,1]:
      Hs_evol[i,:]=Hs2[i,:]
      alfa_evol=alfa_JH_sel
      gamma_evol=gamma_JH_sel
  gamma_evol=np.reshape(gamma_evol,(b,iter),'F')
  alfa_evol=np.reshape(alfa_evol,(b,iter),'F')
  aasas=col_row(Hsig)
  assas=np.rot90(aasas)
  assas=np.flipud(assas)
  Hsig2=np.matlib.repmat(assas,1,iter)
  #Check the objective function, the difference betwen the wave heigh data vs the wave heigh from simulation
  dif=Hsig2-Hs_evol
  dif=np.abs(dif)
  zzz,zzz1=np.shape(dif)
  m=np.zeros((1,b))
  place=np.zeros((1,b))
  Alfa=np.zeros((1,b))
  Gamma=np.zeros((1,b))
  dif_out=np.zeros((1,b))
  Hsig_out=np.zeros((1,b))
  #Obtain minimum from the objective function
  for i in range(0,b,1):
    m[0,i]=min(dif[i,:])
  for i in range(0,b,1):
    for j in range(0,zzz1,1):
      if dif[i,j]==m[0,i]:
        place[0,i]=j
  for i in range(0,b,1):
    Alfa[0,i]=alfa_evol[i,int(place[0,i])]
    dif_out[0,i]=dif[i,int(place[0,i])]
    Hsig_out[0,i]=Hs_evol[i,int(place[0,i])]
    Gamma[0,i]=gamma_evol[i,int(place[0,i])]
  Alfa=row_col(Alfa)
  dif_out=row_col(dif_out)
  Hsig_out=row_col(Hsig_out)
  Gamma=row_col(Gamma)
  return Alfa, dif_out, Hsig_out, Gamma

"""###Open CSV file that mus contain peak period and significat wave heigh"""

data=pd.read_csv('/content/Book1.csv')
Hsg=[]
Tp=[]
for index, row in data.iterrows():
  x=row['Hs (m)']
  y=row['Tp (s)']
  Hsg.append(x)
  Tp.append(y)
Hsg=np.array(Hsg)
Tp=np.array(Tp)

"""###Practica"""

iter=8000
oo=100
Alfa_,dif_out_,Hsig_out_,Gamma_out_=Jonswap(Hsg,Tp,iter,oo)
