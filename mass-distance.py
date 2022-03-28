from astropy.io import ascii
from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt
import os
from astropy import units as u
from IPython.core.display import display, HTML
display(HTML("<style>"
    + "#notebook { padding-top:0px !important; } " 
    + ".container { width:100% !important; } "
    + ".end_space { min-height:0px !important; } "
    + "</style>"))

bands = ['J','K','H','I','V','R','B']

def massdistance(event,iso_dir,*bands):
    '''
    This function plots the mass distance relation for your event. It works by creating a file that contains all your event's information, in a table format.
    The 1195.csv event can be taken as an example. Calling on the function type "1195.csv". 
    Next, you need to choose which isochrones you want to use (from which Girardi year). The options are 1Gyr, 4Gyr, 6.4Gyr and 10Gyr. Enter the following:
    "10Gyr" e.g. 
    Finally you need to tell the function which bands you wish to use. They can be entered as follows 'K','J','H'. 
    A general example  of how to use this function is: massdistance("1195.csv", "10Gyr",'K','J','H')
    
    ~Enjoy!~
    
    '''
    event = Table.read(event, format = 'ascii.csv')
    distance_lens = list(range(10, 8000))
    # reading in your event and defining each column
    for column in event: 
        distance_source = column['distance_source'] # in pc
        theta_E = column['theta_E']  # Einstein radius in mas
        sig_theta_E = column['sig_theta_E']
        Pi_E = column['Pi_E'] # Parallax in mas (?)
        sig_Pi_E = column['sig_Pi_E']
        xmin = column['xmin'] # these are your x-axis boundaries
        xmax = column['xmax']
        Jlens = column['Jlens'] # lens magnitude
        errJlens = column['errJlens'] #error on lens magnitude
        AJlens = column['AJlens'] # Extinction
        Hlens = column['Hlens']
        errHlens = column['errHlens']
        AHlens = column['AHlens']
        Klens = column['Klens']
        errKlens = column['errKlens']
        AKlens = column['AKlens']
        SHV_Pi = column['SHV_Pi']
        SHV_Pi_err = column['SHV_Pi_err']

    
    #upper and lower einstein radius boundary
    theta1 = (theta_E - sig_theta_E)**2
    theta2 = (theta_E + sig_theta_E)**2
    
    #Reading in isochrones
    if iso_dir == "1Gyr":
        iso_dir = ascii.read("Girardi/isoc_Z0.017_Y0.30_1Gyr.dat")
    elif iso_dir == "4Gyr":
        iso_dir = ascii.read("Girardi/isoc_Z0.017_Y0.30_4Gyr.dat")
    elif iso_dir == "6.4Gyr":
        iso_dir = ascii.read("Girardi/isoc_Z0.017_Y0.30_6.4Gyr.dat")
    elif iso_dir == "10Gyr":
        iso_dir = ascii.read("Girardi/isoc_Z0.017_Y0.30_10Gyr.dat")
     
    #calling the mass and magnitudes from the chosen file
    mass0 = [column['col5'] for column in iso_dir]
    mk = [column['col15'] for column in iso_dir]
    mh = [column['col14'] for column in iso_dir]  
    mb = [column['col9'] for column in iso_dir]
    mv = [column['col10'] for column in iso_dir]
    mr = [column['col11'] for column in iso_dir]
    mi = [column['col12'] for column in iso_dir]
    mj = [column['col13'] for column in iso_dir]
    #print(mk)
    
    
    # Calculating the x axis and parallaxes 
    X = []
    para1=[]
    para2=[]
    para_shv1=[]
    para_shv2=[]
    for i in distance_lens:
        xdist = i / distance_source
        p1 = ((1000/i)-(1000/distance_source))/(8.144*(Pi_E-sig_Pi_E)**2)
        p2 = ((1000/i)-(1000/distance_source))/(8.144*(Pi_E+sig_Pi_E)**2)
        p_shv_1 = ((1000/i)-(1000/distance_source))/(8.144*(SHV_Pi-SHV_Pi_err)**2)
        p_shv_2 = ((1000/i)-(1000/distance_source))/(8.144*(SHV_Pi+SHV_Pi_err)**2)
        X.append(float(xdist))
        para1.append(float(p1))
        para2.append(float(p2))
        para_shv1.append(float(p_shv_1))
        para_shv2.append(float(p_shv_2))
    #print(X)
    # Calculating the Y axis
    Y1 = []
    Y2 = []
    for j in X: 
        gg = str(j/(1-j))
        yval1 = theta1 * (j/(1-j))
        yval2 = theta2 * (j/(1-j))
        Y1.append(float(yval1))
        Y2.append(float(yval2))
    
    #fig = plt.figure(figsize=(8, 6))
    #ax = fig.add_subplot(111)
        #Create Figure

    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    ax.tick_params(direction='in', length=6, which='major', width=3, grid_alpha=0.5, top=0, right=0)
    ax.tick_params(direction='in', length=4, which='minor', width=2, grid_alpha=0.5, top=1, right=1)

    fontsize = 25
    hfont = {'fontname':'AVHershey Simplex'}

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.5)

    for tick in ax.xaxis.get_major_ticks():
        tick.set_pad(9.)
        tick.label1.set_fontsize(fontsize)
        tick.label1.set_fontweight('bold')
        tick.label1.set_fontname(**hfont)
    for tick in ax.yaxis.get_major_ticks():
        tick.set_pad(9.)
        tick.label1.set_fontsize(fontsize)
        tick.label1.set_fontweight('bold')
        tick.label1.set_fontname(**hfont)
    
    # You can define colours here if you want.

    thetaE_color='#4ECDC4'
    parallax_color='#FF6B6B'
    Kiso_color='#13747D'


    
    #Plotting the theta E line (this will be filled in later down)
    ax.plot(distance_lens, Y1, linewidth = 0.5, color = '#D37F27', markersize = 0.3, alpha = 0.5)
    ax.plot(distance_lens, Y2,linewidth = 0.5, color = '#D37F27', markersize = 0.3, alpha= 0.5)
    # Plotting the parallax (this will be filled in later down)D37F27
    #ax.plot(distance_lens, para1, color = 'orange',markersize=0.8,alpha = 0.4)
    #ax.plot(distance_lens, para2, color = 'orange',markersize=0.8, alpha=0.4)
    ax.plot(distance_lens, para_shv1, linewidth = 0.5, color = '#657060FF',markersize=0.4,alpha = 0.3)
    ax.plot(distance_lens, para_shv2, linewidth = 0.5, color = '#657060FF',markersize=0.4, alpha=0.3)

    
    if 'K' in bands:
        distK=[]
        distKplus=[]
        distKminus=[]
        for k in mk:
            dk = 10**(0.2*(Klens-AKlens-k+5))
            dkplus = 10**(0.2*(Klens-AKlens+errKlens-k+5))
            dkminus = 10**(0.2*(Klens-AKlens-errKlens-k+5))
            distK.append(dk)
            distKplus.append(dkplus)
            distKminus.append(dkminus)
        #ax.plot(distK, mass0, color = 'green',linewidth = 3, alpha = 0.6) 
        ax.plot(distK, mass0, linewidth = 3, color = '#CD4F38FF', alpha = 0.8)
        ax.plot(distKminus, mass0,linewidth = 3, linestyle = '--', color = '#CD4F38FF', alpha = 0.8)
        ax.plot(distKplus, mass0,linewidth=3, linestyle = '--', color = '#CD4F38FF', alpha = 0.8)
        #plt.fill_betweenx(mass0,distKplus,distKminus, color='#CD4F38FF',alpha#CD4F38FF = 0.6)
       
        
        
   
    #if 'H' in bands:
        #distH=[]
        #distHplus=[]
        #distHminus=[]
        #for h in mh:
        #    dh = 10**(0.2*(Hlens-AHlens-h+5))
        #   dhplus = 10**(0.2*(Hlens-AHlens+errHlens-h+5))
        #    dhminus = 10**(0.2*(Hlens-AHlens-errHlens-h+5))
        #   distH.append(dh)
        #    distHplus.append(dhplus)
        #    distHminus.append(dhminus)           
        #ax.plot(distH, mass0, color = 'seagreen', linewidth = 5, alpha=0.8)
        #ax.plot(distHplus, mass0,linewidth =5, linestyle = '--', color = 'seagreen', alpha=0.8)
        #ax.plot(distHminus, mass0,linewidth=5, linestyle = '--', color = 'seagreen', alpha = 0.8)
        
    # More magnitudes can be added. just copy paste the above code chaning the variable to match your new magnitude.

    # These are the values+errors of parameters from the original paper (or papers)
    #BOND
    ax.errorbar(7200, 0.37, color='#2F8E9C', capsize=5, capthick=3, linewidth = 3, alpha=0.8,
                markersize=10, xerr=[[1020], [850]],
                yerr=[[0.21], [0.38]],fmt='o', zorder=3)
    #SHVARTZWALD
    ax.errorbar(3910, 0.078, color = '#386736', capsize = 5, capthick=3, linewidth=3,
               markersize = 10, xerr=[[420], [460]], yerr=[[0.016],[0.012]],fmt='.',zorder=6)
    
    #Plot any labels you need

    ax.text(6000, 0.25, r'$\theta_E$', fontsize=25, color='#D37F27', **hfont,alpha=1)
    ax.text(3800, 0.5, '$K_{Keck,lens}$', fontsize=25, color='#CD4F38FF', **hfont,alpha=1)
    #ax.text(3500, 0.8, 'Isochrone (H-band)', fontsize=25, color='seagreen', **hfont,alpha=1)
    ax.text(2900, 0.75, 'Bond+17', fontsize=25, color='#2F8E9C', **hfont, alpha=1)
    ax.text(2900, 0.8, 'Vandorou+21', fontsize=25, color='black', **hfont, alpha = 1)
    ax.text(2900, 0.7, 'Shvartzvald+17', fontsize=25, color='#386736', **hfont, alpha = 1)
    #ax.text(5950, 0.6, '$\pi_{E} \sim 0.05$', fontsize=20, color='orange', **hfont, alpha = 1)    
    ax.text(6000, 0.06, '$\pi_{E}$', fontsize=25, color='#92978F', **hfont, alpha = 1)   
    
    #MASS AND DISTANCE OF LENS    
    # This is where the isochrones are constraints (thetaE, parallax) intersect. 
    ax.errorbar(6240, 0.505, color='black', capsize=5, capthick=3, linewidth = 3.5,
                markersize=10, xerr=[[420], [420]], yerr=[[0.055], [0.055]],fmt='o', zorder=4)
    
    plt.ylabel('Mass ($M_{\odot}$)', fontsize = 30, fontweight='bold', labelpad=15, **hfont)
    plt.xlabel('Distance (pc)', fontsize = 30, fontweight='bold', labelpad=10, **hfont)
    plt.ylim(0.01, 0.9)
    plt.xlim(2500, 8300)
    plt.fill_between(distance_lens, Y1, Y2, color='#D37F27', alpha=0.5)
    plt.fill_between(distance_lens, para_shv1, para_shv2, color='#92978F', alpha=0.6, zorder=5)
   
    #plt.legend() - this is usually not needed
    #plt.savefig('1195_2021_v8.png', dpi=600) # uncomment this line to save as a png image. 
        


