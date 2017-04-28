import math
import cmath
import scipy
from scipy.integrate import quad
import numpy as np
import json
from ImpliedVolatility import implied_vol

pi = math.pi
def CF_heston(xt,vt,tau,mu,a,uj,bj,rho,sig,phi):
	i = 1j
	xj = np.array(bj-(rho*sig*phi*i));
	dj = np.array(np.sqrt( xj**2 - (sig**2)*( 2*uj*phi*i - phi**2 ) ))
	gj = np.array(( xj+dj )/( xj-dj ))
	
	xx = ( 1-(gj*np.exp(dj*tau)) )/( 1-gj )
	A = i*phi*xt
	B  =  a/( sig**2 ) * ( (xj+dj) * tau - (2*np.log(xx)) )
	C  = (vt*(xj+dj))/(sig**2)* ( 1-np.exp(dj*tau) )/( 1-gj*np.exp(dj*tau))
	fj = np.exp(A + B +  C)
	return fj



def HestonCall(St,K,r,T,vt,kap,th,sig,rho,lda):
	# print St,K,r,T,vt,kap,th,sig,rho,lda
	dphi = 0.01
	maxphi = 50
	phi = np.linspace(np.finfo(float).eps, 50, 50/0.01+1, endpoint=True)
	i = 1j


	f1 = CF_heston(math.log(St),vt,T,0,kap*th,0.5,kap+lda-rho*sig,rho,sig,phi)
	P1 = 0.5+(1/pi)*sum(np.real(np.exp(-i*phi*np.log(K))*f1/(i*phi))*dphi)
	f2 = CF_heston(np.log(St),vt,T,0,kap*th,-0.5,kap+lda,rho,sig,phi)
	P2 = 0.5+(1/pi)*sum(np.real(np.exp(-i*phi*math.log(K))*f2/(i*phi))*dphi)
	C = (St*P1) - (K*np.exp(-r*T)*P2)
	return C