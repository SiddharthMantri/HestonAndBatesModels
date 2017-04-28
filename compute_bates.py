import math
import cmath
import scipy
from scipy.integrate import quad
import numpy as np
import json
from ImpliedVolatility import implied_vol

pi = math.pi
def CF_Bates(xt,vt,tau,mu,a,uj,bj,rho,sig,phi, lambd, muj, sigj):
	i = 1j
	xj = np.array(bj-(rho*sig*phi*i));
	dj = np.array(np.sqrt( xj**2 - (sig**2)*( 2*uj*phi*i - phi**2 ) ))
	gj = np.array(( xj+dj )/( xj-dj ))
	
	xx = ( 1-(gj*np.exp(dj*tau)) )/( 1-gj )
	A = i*phi*xt
	B  =  a/( sig**2 ) * ( (xj+dj) * tau - (2*np.log(xx)) )
	C  = (vt*(xj+dj))/(sig**2)* ( 1-np.exp(dj*tau) )/( 1-gj*np.exp(dj*tau)  ) 
	temp1 = lambd*tau
	temp2 = np.power(1+muj, i*phi)
	temp3 = 0.5*(sigj*sigj)*i*phi
	temp4 = (i*phi)-1
	temp5 = np.exp(temp3*temp4)
	temp6 = temp1*((temp2*temp5)-1)
	D = (-1*lambd*muj*i*phi*tau)+temp6
	# D = 0
	fj = np.exp(A + B +  C + D)
	return fj



def BatesCall(St,K,r,T,vt,kap,th,sig,rho,lda,lambd, muj, sigj):
	dphi = 0.01
	maxphi = 50
	phi = np.linspace(np.finfo(float).eps, maxphi, maxphi/0.01+1, endpoint=True)
	i = 1j


	f1 = CF_Bates(math.log(St),vt,T,0,kap*th,0.5,kap+lda-rho*sig,rho,sig,phi,lambd, muj, sigj)
	P1 = 0.5+(1/pi)*sum(np.real(np.exp(-i*phi*np.log(K))*f1/(i*phi))*dphi)
	f2 = CF_Bates(np.log(St),vt,T,0,kap*th,-0.5,kap+lda,rho,sig,phi,lambd, muj, sigj)
	P2 = 0.5+(1/pi)*sum(np.real(np.exp(-i*phi*math.log(K))*f2/(i*phi))*dphi)
	C = (St*P1) - (K*np.exp(-r*T)*P2)
	return C



# print BatesCall(100,80,0.002,0.5,0,1,0.5,1,-0.5,0,1, 1, 1)