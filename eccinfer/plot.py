from os import name
import numpy as np
from numpy.core.fromnumeric import size
from scipy.optimize.optimize import main
from scipy.stats import beta 
import matplotlib.pyplot as plt
from orbitize import priors, read_input, kepler, results
import emcee
from scipy.optimize import minimize
import glob
import corner
from pdb import set_trace


def load_posteriors(fnames):
    '''
    Loads the posteriors for the beta parameters that are saved 
    as npy files.

    args:
        fnames: filenames
    returns:
        posts
    '''
    posts={f[13:-4]:np.load(f) for f in fnames}
    return posts

def truth_v_inferred(post,savename,gridspec=False):
    '''

    '''
    a = 2.3
    b = 1.7

    rng  = np.linspace(0.0001,0.9999,10000)
    func = beta(a,b)

    if gridspec:
        
        fig=plt.figure(figsize=(20,20))

        fig.patch.set_facecolor('navy')

        gs = fig.add_gridspec(nrows=5,ncols=4,hspace=0.1,wspace=0.1)

        fig_ax1=fig.add_subplot(gs[0:2,:])

        fig_ax1.set_facecolor('midnightblue')

        fig_ax1.plot(rng,func.pdf(rng),c='yellow',linestyle='dashed',linewidth=3)
        fig_ax1.set_title('Underlying Distribution',size=20, c='white')
        fig_ax1.set_xlabel('Eccentricity',size=15,c='white')
        fig_ax1.set_ylabel('Probability Density',size=15,c='white')

        fig_ax1.spines['bottom'].set_color('white')
        fig_ax1.spines['top'].set_color('white')
        fig_ax1.spines['left'].set_color('white')
        fig_ax1.spines['right'].set_color('white')
        fig_ax1.xaxis.label.set_color('white')
        fig_ax1.tick_params(axis='x', colors='white')
        fig_ax1.tick_params(axis='y', colors='white')

        fig_ax1.annotate(f'a = {a}, b = {b}', (0.5,6),c='yellow',size=15)



        
        fig_ax1.set_ylim([0,7])
        fig_ax1.set_xlim([0,1])

        for j,val in enumerate([5,10,20,50]):
            
            for i,sig in enumerate([20,5,1]):
                
                print(i,j)
  
                ax=fig.add_subplot(gs[i+2,j])
                ax.set_facecolor('midnightblue')

                ax.spines['bottom'].set_color('white')
                ax.spines['top'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.xaxis.label.set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                sim_name=f'{val}_{sig}'

                beta_post=post[sim_name]
                
                med_a=np.median(beta_post[:,0])
                med_b=np.median(beta_post[:,1])

                med_func = beta(med_a,med_b)

                ax.plot(rng,med_func.pdf(rng),c='yellow',linewidth=5,alpha=0.8)
                ax.annotate(f'N = {val}, $\\sigma$ = {sig/100}', (0.5,6),c='yellow',size=15)

                nrandom=50
                for k in range(nrandom):
                    idx=np.random.randint(0,beta_post.shape[0]-1)
                    rnd_a,rnd_b=beta_post[idx]
                    rnd_func=beta(rnd_a,rnd_b)
                    ax.plot(rng,rnd_func.pdf(rng),c='pink',alpha=0.2)
                
                ax.set_ylim([0,7])
                ax.set_xlim([0,1])

        fig.supxlabel('Eccentricity',size=20,c='white')
        fig.supylabel('Probability Density',size=20,c='white')
        
        plt.savefig(savename)

    
    else:

        fig=plt.figure(figsize=(12,6))
        
        plt.plot(rng,func.pdf(rng),label='Underlying Distribution',c='red',linestyle='dashed',linewidth=3)

        med_a=np.median(post[:,0])
        med_b=np.median(post[:,1])

        med_func = beta(med_a,med_b)

        plt.plot(rng,med_func.pdf(rng),label='Recovered Distribution',c='black',linewidth=5,alpha=0.8)

        nrandom=15
        for i in range(nrandom):
            idx=np.random.randint(0,post.shape[0]-1)
            rnd_a,rnd_b=post[idx]
            rnd_func=beta(rnd_a,rnd_b)
            plt.plot(rng,rnd_func.pdf(rng),c='grey',alpha=0.2)
        
        plt.xlabel('Eccentricity')
        plt.ylabel('Normalised PDF')

        plt.title('Recovering eccentricity distributions')
        plt.ylim([0,7])
        plt.xlim([0,1])
        plt.legend()
        plt.savefig(savename)

def plot_single(fname,a,b):
    rng  = np.linspace(0.0001,0.9999,10000)
    func = beta(a,b)
    plt.plot(rng,func.pdf(rng),c='black',linestyle='dashed',linewidth=3,label='True')
    beta_samples=np.load(fname)
    nrandom=15
    for i in range(nrandom):
        idx=np.random.randint(0,beta_samples.shape[0]-1)
        rnd_a,rnd_b=beta_samples[idx]
        rnd_func=beta(rnd_a,rnd_b)
        plt.plot(rng,rnd_func.pdf(rng),c='grey',alpha=0.2)
    
    med_a,med_b=np.median(beta_samples,axis=0)[0],np.median(beta_samples,axis=0)[1]
    med_func=beta(med_a,med_b)
    plt.plot(rng,med_func.pdf(rng),c='red',linewidth=5,alpha=0.8,label='recovered')
    plt.ylim([0,7])
    plt.xlim([0,1])
    plt.title('50 systems, 4 points')
    plt.legend()
    plt.savefig('inferred_distribution')

if __name__=='__main__':
    fname='../results/warm_jupiter/samples.npy'
    a=0.867
    b=3.03
    plot_single(fname,a,b)




