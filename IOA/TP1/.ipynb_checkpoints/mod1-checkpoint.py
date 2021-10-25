#=============================================================
# Introduction to Ocean and Climate
# Master 1 Marine Physics

# This file contains modules needed for the first computer class:
#
#   * distribution of insolation, eccentricity, obliquity, seasons, ...
#   * ERBE data, OLR, insolation, albedo, ...
#   * simple EBM, multiple equilibria, bifurcations, snow ball Earth, ...
#
# last modif: 19 Sept 2018 / author: oarzel@univ-brest.fr
#
#=============================================================

import numba as nb

def calendar_season(iday,days,months,days_per_month):

    import numpy as np

    month0=1+np.floor(months[iday])
    if month0>1:
        day0=np.floor(days[iday])-sum(days_per_month[j] for j in range(int(month0-1)))
    else:
        day0=np.floor(days[iday])
    return [day0,month0]

#=============================================================

def orbitalparam(kyear):

    import numpy as np
    from matplotlib import pyplot as plt
    from scipy.interpolate import CubicSpline
    # === Load orbital parameters (given each kyr for 0-5Mya) ===
    # This matrix contains data from Berger and Loutre (1991), 
    filedat='data/orbital_values.dat'
    M=np.loadtxt(filedat)
    kyear0=-M[:,0] # kyears before present for data (kyear0>=0);
    ecc0=M[:,1] # eccentricity
    # add 180 degrees to omega (see lambda definition, Berger 1978 Appendix)
    omega0=M[:,2]+180 # longitude of perihelion (precession angle)
    omega0=np.unwrap(omega0*np.pi/180)*180/np.pi # remove discontinuities (360 degree jumps)
    epsilon0=M[:,3] # obliquity angle
    # Interpolate to requested dates
    cs1 = CubicSpline(kyear0,ecc0)
    cs2 = CubicSpline(kyear0,omega0)
    cs3 = CubicSpline(kyear0,epsilon0)
    ecc=cs1(kyear)
    omega=cs2(kyear)
    epsilon=cs3(kyear)
    #print ("ecc =",ecc, ", epsilon =", epsilon, "omega=", omega)
    return [ecc, epsilon, omega];

#=============================================================

def orbital_timeseries(t,lat0):

    import numpy as np
    from matplotlib import pyplot as plt
    from mod1 import orbitalparam, solar_grid
    import math
    
    sun_grid = solar_grid()
    lat=sun_grid['lat'];nlat=len(lat)
    days=sun_grid['days'];nday=len(days)
    days_per_month=sun_grid['days_per_month']

    ecc, epsilon, omega = orbitalparam(t)

    fig1=plt.figure(figsize=(10,8))
    plt.subplots_adjust(hspace = .5)
    p1=plt.subplot(4,1,1)
    plt.plot(t,ecc,'b')
    plt.ylabel('e',fontsize=20)
    plt.title('eccentricity',fontsize=20)
    plt.xticks([])
    plt.grid(True)
    plt.gca().invert_xaxis()
    p2=plt.subplot(4,1,2)
    plt.plot(t,epsilon,'r')
    plt.ylabel('$\epsilon$',fontsize=20)
    plt.title('obliquity',fontsize=20)
    plt.xticks([])
    plt.grid(True)
    plt.gca().invert_xaxis()
    p3=plt.subplot(4,1,3)
    p=ecc*np.sin(omega*np.pi/180.0)
    plt.plot(t,p,'k')
    plt.ylabel('e sin($\omega$)',fontsize=20)
    plt.title('precession index',fontsize=20)
    plt.xticks([])
    plt.grid(True)
    plt.gca().invert_xaxis()
    
    epsilon=epsilon*np.pi/180
    omega=omega*np.pi/180
    S0=1365 # Solar constant (W/m2)
    iphi = np.argmin(abs(lat-lat0))
    lat=lat*np.pi/180
    earth_period=365.2422 # Earth period of revolution in days
    ind=[0,1]
    vernal_equinox_day=sum(days_per_month[i] for i in ind)+21; # 80th day of the year = 21st March

    nt=len(t)
    shm_summer=np.zeros(nt)
    # average summer JJA insolation at 65N
    for it in range(nt):
        # estimate lambda from calendar day using an approximation from Berger 1978 section 3
        delta_lambda_m=(days-vernal_equinox_day)*2*np.pi/365.2422
        beta=math.pow(1-ecc[it]**2,0.5)
        lambda_m0=-2.0*( (0.5*ecc[it]+0.125*ecc[it]**3)*(1+beta)*np.sin(-omega[it])-0.25*ecc[it]**2*(0.5+beta)*np.sin(-2*omega[it])+0.125*ecc[it]**3*(1.0/3+beta)*(np.sin(-3*omega[it])) )
        lambda_m=lambda_m0+delta_lambda_m
        lams=lambda_m+(2*ecc[it]-0.25*ecc[it]**3)*np.sin(lambda_m-omega[it])+(5.0/4)*ecc[it]**2*np.sin(2.0*(lambda_m-omega[it]))+(13/12)*ecc[it]**3*np.sin(3.0*(lambda_m-omega[it]))
        delta=np.arcsin(np.sin(epsilon[it])*np.sin(lams)) # declination angle

        shm=np.zeros(nday)
        for iday in range(nday):
            h_sunset=np.arccos(-np.tan(lat[iphi])*np.tan(delta[iday])) # West
            if ( (abs(lat[iphi]) >= np.pi/2 - abs(delta[iday])) & (lat[iphi]*delta[iday]> 0)):
                h_sunset=np.pi
            if ( (abs(lat[iphi]) >= np.pi/2 - abs(delta[iday])) & (lat[iphi]*delta[iday]<= 0)):
                h_sunset=0.

            # Earth-Sun distance and daily mean insolation
            a=149.6e9 # major semi axis (wikipedia)
            b=a*np.sqrt(1-ecc[it]**2) # minor axis
            rm=np.sqrt(a*b) # mean earth-sun distance
            theta=lams-omega[it] # theta(1) indicates the Earth s position at January first ! theta = true anomaly
            rr=a*(1-ecc[it]**2)/(1+ecc[it]*np.cos(theta)) # earth sun distance as a function theta (true anomaly)
            # mean daily insolation
            fact=h_sunset*np.sin(lat[iphi])*np.sin(delta[iday])+np.cos(lat[iphi])*np.cos(delta[iday])*np.sin(h_sunset);
            shm[iday]=(S0/np.pi)*(rm/rr[iday])**2*fact

        # summer insolation TOA
        i0=sum(days_per_month[i] for i in range(0,5))+1
        i1=sum(days_per_month[i] for i in range(0,8))
        shm_summer[it]=np.mean(shm[i0:i1]);


    p4=plt.subplot(4,1,4)
    plt.plot(t,shm_summer,'k')
    plt.ylabel('W/m2',fontsize=20)
    plt.xlabel('time (kyr BP)',fontsize=20)
    if lat0 >0:
        tcar="Daily mean summer insolation at {}N".format(lat0)
        tcarp="orbital_elements_timeseries_{}N.png".format(lat0)
    elif lat0==0:
        tcar="Daily mean summer insolation at the equator"
        tcarp="Daily_mean_summer_insolation_at_the_equator.png"
    else:
        tcar="Daily mean summer insolation at {}S".format(abs(lat0))
        tcarp="orbital_elements_timeseries_{}S.png".format(abs(lat0))
    plt.title(tcar.title(),fontsize=20)
    plt.gca().invert_xaxis()
    plt.grid(True)
    plt.show(block=False)
    #plt.savefig(tcarp,dpi=100)

#=============================================================

def area_planet(lon,lat):

    import numpy as np

    nlon=len(lon)
    nlat=len(lat)
    
    lat_g=np.zeros(nlat+1)
    lon_g=np.zeros(nlon+1)
    lat_g[1:nlat]=(lat[0:nlat-1]+lat[1::])/2
    lat_g[0]=-90
    lat_g[nlat]=90
    lon_g[1:nlon]=(lon[0:nlon-1]+lon[1::])/2
    lon_g[0]=0
    lon_g[nlon]=360
    dlon=np.diff(lon_g)*np.pi/180
    dlat=np.diff(lat_g)*np.pi/180
    area=np.zeros((nlon,nlat))
    earth_radius=6.37e+06
    for j in range(nlat):
        for i in range(nlon):
            area[i,j]=dlon[i]*dlat[j]*earth_radius**2*np.cos(lat[j]*np.pi/180.)

    return area

#============================================================

def planet_average(var,yt,lon,lat):

    import numpy as np
    from mod1 import area_planet
    
    area=area_planet(lon,lat)

    ns=np.size(np.shape(var))

    j0=lat.tolist().index(yt[0])
    j1=lat.tolist().index(yt[-1])+1

    if ns==1:

        ny = np.size(var)
        varm=0.0
        areasum=0.0
        for j in range(j0,j1,1):
            if not np.isnan(var[j]):
                areasum+=area[1,j]
                varm+=var[j]*area[1,j]
        varm=varm/areasum
        
    elif ns==2:
        
        nx, ny = np.shape(var)
        varm=0.0
        areasum=0.0
        for i in range(nx):
            for j in range(j0,j1,1):
                if not np.isnan(var[i,j]):
                    areasum+=area[i,j]
                    varm+=var[i,j]*area[i,j]
        varm=varm/areasum

    elif ns==3:

        nx, ny, nt = np.shape(var)
        varm=np.zeros(nt)
        for it in range(nt):
            areasum=0.0
            for i in range(nx):
                for j in range(j0,j1,1):
                    if not np.isnan(var[i,j,it]):
                        areasum+=area[i,j]
                        varm[it]+=var[i,j,it]*area[i,j]
            varm[it]=varm[it]/areasum

    return varm

#=============================================================

def ephemeride(day,month,year,longitude,latitude,td_utc,sunrise):

    from math import floor, ceil, pi, atan, tan, sin, asin, cos, acos

    # 1. first calculate the day of the year

    N1 = floor(275 * month / 9)
    N2 = floor((month + 9) / 12)
    N3 = (1 + floor((year - 4 * floor(year / 4) + 2) / 3))
    N = N1 - (N2 * N3) + day - 30

    d2r=pi/180.0
    
    # 2. convert the longitude to hour value and calculate an approximate time
    lngHour = longitude / 15
    t = N + ((6 if sunrise else 18) - lngHour)/24
    
    # 3. calculate the Sun's mean anomaly (degrees)
    M = (0.9856 * t) - 3.289

    # 4. calculate the Sun's true longitude (degrees)
    L = M + (1.916 * sin(M*d2r)) + (0.020 * sin(2*M*d2r)) + 282.634
    L +=  -360 if L > 360 else 360 if L < 360 else 0

    # 5. calculate the Sun's right ascension
    RA = atan(0.91764 * tan(L*d2r))/d2r
    RA +=  -360 if RA > 360 else 360 if RA < 360 else 0
    RA += (floor(L/90) - floor(RA/90)) * 90
    RA = RA / 15

    # 6. calculate the Sun's declination
    sinDec = 0.39782 * sin(L*d2r)
    cosDec = cos(asin(sinDec))

    # 7. calculate the Sun's local hour angle --> sunrise equation + zenith correction
    zenith=90.83333333*d2r
    cosH = (cos(zenith) - (sinDec * sin(latitude*d2r))) / (cosDec * cos(latitude*d2r))

    if sunrise and cosH > 1:
        print("the sun never rises on this location (on the specified date)"); sys.exit()
    elif not sunrise and cosH < -1:
        print("the sun never sets on this location (on the specified date)"); sys.exit()
    H = ((360 - (acos(cosH)/d2r)) if sunrise else (acos(cosH)/d2r))/15
	
    # 8. calculate local mean time of rising/setting
    T = H + RA - (0.06571 * t) - 6.622

    # 9. adjust back to UTC
    local = T - lngHour + td_utc
    local += 24 if local < 0 else -24 if local > 24 else 0

    # 10. convert to HMS
    hours=floor(local)
    minutes=floor((local-hours)*60)
    seconds=floor(((local-hours)*60-minutes)*60)

    if sunrise:
        print("Sunrise : ", hours ,"h", minutes ,"m", seconds ,"s")
    else:
        print("Sunset : ", hours ,"h", minutes ,"m", seconds ,"s")

#=============================================================

def solar_grid():

    import numpy as np
    
    nlat=180
    lat=np.linspace(-89.5,89.5,nlat)
    latrad=lat*np.pi/180
    days_per_month=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    nday=sum(days_per_month) # number of calendar days for a normal year
    days=np.linspace(1,nday,nday)
    dlon=360.0/nday
    lon=np.linspace(0.5*dlon,(nday-0.5)*dlon,360)
    # days_mid: day number in the middle of each month (used to build figures)
    days_mid=np.zeros(12)
    a=0
    for i in range(12):
        days_mid[i]=0.5*days_per_month[i]+a
        a=sum(days_per_month[j] for j in range(i+1))

    resu={'lat':lat,'lon':lon,'days':days,'days_mid':days_mid,'days_per_month':days_per_month}
    
    return resu


#=============================================================

def insolation(kyear,ifig):
    
    #
    # This program computes the daily average insolation as a function
    # of day and latitude at any point during the past 5 million years.
    #
    # Astronomical parameters (eccentricity, obliquity, longitude of perihelion) are
    # determined by either 1/ choosing an epoch through the parameter kyear (0 is present
    # day conditions, -1 is 1 thousand years ago, ... -5000 is 5 millions years back
    # in time, the oldest epoch available in this program) or 2/ imposing those parameters
    # as follows resu =insolation([ecc,obl,omega],day_type) where ecc is the
    # eccentricity (deg), obl is the obliquity (deg), omega is the longitude of
    # perihelion measured from the Vernal equinox (deg).
    #
    # example: daily mean insolation for present-day conditions
    #          resu=insolation(0)
    #          which is equivalent to
    #          resu=insolation([0.017236 23.4454 281.3681])
    #
    # last modification: 14 September 2018
    #
    # Author: Olivier.Arzel@univ-brest.fr
    #
    # References: 
    #   Berger A. and Loutre M.F. (1991). Insolation values for the climate of
    #     the last 10 million years. Quaternary Science Reviews, 10(4), 297-317.
    #   Berger A. (1978). Long-term variations of daily insolation and
    #     Quaternary climatic changes. Journal of Atmospheric Science, 35(12),
    #     2362-2367.
    #
    #-------------------------------------------------------------------------------------

    import numpy as np
    import matplotlib.pyplot as plt
    from mod1 import orbitalparam,calendar_season,solar_grid
    
    sun_grid = solar_grid()
    lat=sun_grid['lat'];nlat=len(lat)
    yt=lat # average over the entire planet
    lon=sun_grid['lon']
    days=sun_grid['days'];nday=len(days)
    days_mid=sun_grid['days_mid']
    days_per_month=sun_grid['days_per_month']

    if np.size(kyear)==3:
        ecc=kyear[0]
        epsilon=kyear[1]*np.pi/180
        omega=kyear[2]*np.pi/180
    else:
        ecc, epsilon, omega = orbitalparam(kyear)
        epsilon=epsilon*np.pi/180
        omega=omega*np.pi/180
    
    S0=1365 # Solar constant (W/m2)
    latrad=lat*np.pi/180
    earth_period=365.2422 # Earth period of revolution in days
    ind=[0,1]
    vernal_equinox_day=sum(days_per_month[i] for i in ind)+21; # 80th day of the year = 21st March
    # day_type: 1/ calendar days, 2/ equinoctial type (from solar longitude)
    day_type=1

    print ("insolation at ", kyear ," kyr before present")
    print ("eccentricity=", ecc)
    print ("obliquity=", epsilon*180.0/np.pi)
    print ("longitude of perihelion=", omega*180.0/np.pi)
    print ("solar constant=", S0 ,"W/m2")
    
    # To determine an expression for the true longitude lambda we first need
    # to have an expression for the orbital angular velocity. Because of the elliptical shape
    # of the Earth s orbit, a nonlinear relationship appears between the angular velocity and
    # the true anomaly (angle substented at the Sun by the orbital arc from perihelion
    # to Earth position). Celestial mechanics (Kepler s second law among others) must be invoked to determine
    # the relationship between the true longitude (or solar longitude) and astronomical elements
    # (eccentricity, longitude of perihelion, and calendar days)
    # An alternative is to use an "equinoctial calendar" which starts from spring equinox.
    # The true longitude in this case increases linearly with the "solar time" (day_type=2)

    if np.abs(day_type)==1: # calendar days
        # estimate lambda from calendar day using an approximation from Berger 1978 section 3
        delta_lambda_m=(days-vernal_equinox_day)*2*np.pi/365.2422
        ecc2=np.array(np.power(ecc,2))
        ecc3=np.array(np.power(ecc,3))
        beta=np.array(np.power(1-ecc2,0.5))
        lambda_m0=-2.0*( (0.5*ecc+1.0/8*ecc3)*(1+beta)*np.sin(-omega)-1.0/4*ecc2*(1/2+beta)*np.sin(-2*omega)+1.0/8*ecc3*(1/3+beta)*np.sin(-3*omega) )
        lambda_m=lambda_m0+delta_lambda_m
        lams=lambda_m+(2*ecc-1.0/4*ecc3)*np.sin(lambda_m-omega)+(5.0/4)*ecc2*np.sin(2*(lambda_m-omega))+(13.0/12)*ecc3*np.sin(3*(lambda_m-omega))
    elif np.abs(day_type)==2: #solar longitude (1-360)
        lams=days*2*np.pi/360; # lams=0 for spring equinox

    delta=np.arcsin(np.sin(epsilon)*np.sin(lams)) # declination angle

    h_sunrise=np.zeros((nlat,nday))
    h_sunset=np.zeros((nlat,nday))
    LOD=np.zeros((nlat,nday))

    for iphi in range(nlat):
        for iday in range(nday):
            if ( (abs(latrad[iphi]) >= np.pi/2 - abs(delta[iday])) & (latrad[iphi]*delta[iday] > 0)):
                h_sunrise[iphi,iday]=-np.pi
                h_sunset[iphi,iday]=np.pi
            elif ( (abs(latrad[iphi]) >= np.pi/2 - abs(delta[iday])) & (latrad[iphi]*delta[iday]<= 0)):
                h_sunset[iphi,iday]=0
                h_sunrise[iphi,iday]=0
            else:
                # we add a correction to take into account the refraction of solar rays by the atmosphere
                #aref=-0.83*np.pi/180.0
                aref=0.0;
                h_sunrise[iphi,iday]=-np.arccos(np.sin(aref)-np.tan(latrad[iphi])*np.tan(delta[iday])) # at thetas=pi/2 East
                h_sunset[iphi,iday]=+np.arccos(np.sin(aref)-np.tan(latrad[iphi])*np.tan(delta[iday])) # at thetas=pi/2 East
            LOD[iphi,iday]=(12.0/np.pi)*(h_sunset[iphi,iday]-h_sunrise[iphi,iday])
        
    # sunrise and sunset times relative to solar noon
    # solar noon: highest point of the sun in the sky
    time_sunrise=(12.0/np.pi)*(np.real(h_sunrise))
    time_sunset=(12.0/np.pi)*(np.real(h_sunset))

    # sunrise and sunset times relative to solar noon
    # solar noon: highest point of the sun in the sky
    time_sunrise=(12.0/np.pi)*(np.real(h_sunrise))
    time_sunset=(12.0/np.pi)*(np.real(h_sunset))

    # days_mid: day number in the middle of each month (used to build figures)
    days_mid=np.zeros(12)
    a=0
    for i in range(12):
        days_mid[i]=0.5*days_per_month[i]+a
        a=sum(days_per_month[j] for j in range(i+1))

    months=np.linspace(0,12,nday)

    # LOD at Brest as a function of seasons
    Brest_lat=48.4 # latitude 48.4N
    iphi0 = np.argmin(abs(lat-Brest_lat))
    LOD_Brest=LOD[iphi0,:]
    Sunrise_Brest=time_sunrise[iphi0,:]
    Sunset_Brest=time_sunset[iphi0,:]

    iday=np.argmax(LOD_Brest)
    day0, month0 = calendar_season(iday,days,months,days_per_month);
    print ("Summer solstice is on MONTH ", month0 ," DAY ", day0)
    print ("True longitude at summer solstice is ", lams[iday]*180/np.pi ,"degrees")

    # Earth-Sun distance and daily mean insolation
    a=149.6e9 # major semi axis
    b=a*np.sqrt(1-ecc2) # minor axis
    rm=np.sqrt(a*b) # mean earth-sun distance
    theta=lams-omega # theta(1) indicates the Earth s position at January first ! theta = true anomaly
    rr=a*(1-ecc2)/(1+ecc*np.cos(theta)) # earth sun distance as a function theta (true anomaly)
    rr2=np.array(np.power(rr,2))

    # mean daily insolation
    shm=np.zeros((nlat,nday))
    for iphi in range(nlat):
        for iday in range(nday):
            fact=h_sunset[iphi,iday]*np.sin(latrad[iphi])*np.sin(delta[iday])+np.cos(latrad[iphi])*np.cos(delta[iday])*np.sin(h_sunset[iphi,iday])
            shm[iphi,iday]=(S0/np.pi)*(rm*rm/rr2[iday])*fact

    # annual mean insolation
    shf_annual=np.mean(shm,1)

    # figures

    if (ifig):
        fig1=plt.figure(figsize=(5,4))
        plt.plot(days,delta*180.0/np.pi,'k')
        plt.xlabel('days')
        plt.ylabel('declination of the sun (degrees)')
        plt.show(block=False)
        #plt.savefig('declination_sun.png',dpi=200,bbox_inches='tight')

        '''
        fig2=plt.figure(figsize=(8,8))
        plt.subplots_adjust(hspace = .5)
        p1=plt.subplot(3,1,1)
        c=plt.contourf(days,lat,time_sunrise,24,cmap=plt.cm.coolwarm)
        plt.contour(days,lat,time_sunrise,[-12,-11.9],colors='w',linewidths=2,linestyles='solid')
        plt.contour(days,lat,time_sunrise,[-0.1,0.0],colors='w',linewidths=2,linestyles='solid')
        plt.colorbar(c,orientation='vertical')
        plt.xlabel('days')
        plt.ylabel('latitude')
        plt.title('sunrise time')
        p2=plt.subplot(3,1,2)
        c=plt.contourf(days,lat,time_sunset,24,cmap=plt.cm.coolwarm)
        plt.contour(days,lat,time_sunset,[11.9,12.0],colors='w',linewidths=2,linestyles='solid')
        plt.contour(days,lat,time_sunset,[0.,0.1],colors='w',linewidths=2,linestyles='solid')
        plt.colorbar(c,orientation='vertical')
        plt.xlabel('days')
        plt.ylabel('latitude')
        plt.title('sunset time')
        p3=plt.subplot(3,1,3)
        c=plt.contourf(days,lat,np.real(LOD),24,cmap=plt.cm.coolwarm)
        plt.contour(days,lat,np.real(LOD),[23.9,24.0],colors='w',linewidths=2,linestyles='solid')
        plt.contour(days,lat,np.real(LOD),[12],colors='w',linewidths=2,linestyles='solid')
        plt.contour(days,lat,np.real(LOD),[0,0.01],colors='w',linewidths=2,linestyles='solid')
        plt.colorbar(c,orientation='vertical')
        plt.xlabel('days')
        plt.ylabel('latitude')
        plt.title('length of the day (hours)')
        plt.show(block=False)
        plt.savefig('LOD.png',dpi=200,bbox_inches='tight')

        fig3=plt.figure(figsize=(10,5))
        plt.plot(days,LOD_Brest,'k',label='LOD')
        plt.plot(days,Sunrise_Brest,'b',label='Sunrise')
        plt.plot(days,Sunset_Brest,'r',label='Sunset')
        ll=plt.legend(loc='upper left')
        plt.xlabel('days')
        plt.ylabel('hours')
        plt.title('Sunrise, sunset and length of the day in Brest')
        plt.xticks(days_mid,('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'))
        plt.show(block=False)
        plt.savefig('LOD_Brest.png',dpi=200,bbox_inches='tight')
        '''

        fig4=plt.figure(figsize=(10,5))
        var=np.real(shm)
        mie=0;mae=np.amax(shm)
        scale=np.linspace(mie,mae,51)
        c=plt.contourf(days,lat,var,scale)
        plt.title('Mean daily insolation (W/m2)')
        plt.ylabel('latitude')
        plt.xticks(days_mid,('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'))
        plt.colorbar(c,orientation='vertical')
        plt.set_cmap('coolwarm')
        plt.contour(days,lat,var,[-0.5,0.5],colors='w',linewidths=2)
        plt.show(block=False)
        #plt.savefig('Mean_daily_insolation.png',dpi=200,bbox_inches='tight')

        fig5=plt.figure(figsize=(10,5))
        plt.plot(lat,np.real(shf_annual),'k')
        plt.xlabel('Latitude')
        plt.ylabel('W/m2')
        plt.title('Annual mean incoming solar radiation TOA')
        plt.show(block=False)
        #plt.savefig('Annual_mean_insolation.png',dpi=200,bbox_inches='tight')

    # dictionnary with space and time information
    resu = {'lat':lat,'lon':lon,'days':days,'days_mid':days_mid,'days_per_month':days_per_month,'lams':lams,'sunrise_Brest':Sunrise_Brest,'sunset_Brest':Sunset_Brest,'solar':shm,'solar_am':shf_annual,'LOD':LOD,'LOD_Brest':LOD_Brest}
    return resu

#=============================================================

def plot_y(*args):

    import numpy as np
    from matplotlib import pyplot as plt
    from mod1 import solar_grid
    
    sun_grid = solar_grid()
    lat=sun_grid['lat'];nlat=len(lat)
    
    nv=len(args)

    nv2=int((nv)/2)
    
    var=np.zeros((nlat,nv2))

    for i in range(nv2):
        var[:,i]=np.mean(args[i],axis=1)

    if nv2==1:
        tcar1=args[1]
    elif nv2==2:
        tcar1=args[2]
        tcar2=args[3]
    elif nv2==3:
        tcar1=args[3]
        tcar2=args[4]
        tcar3=args[5]

    fig2=plt.figure(figsize=(10,5))
    plt.plot(lat,var[:,0],'b',label=tcar1)
    if nv2==2:
        plt.plot(lat,var[:,1],'r',label=tcar2)
    if nv2==3:
        plt.plot(lat,var[:,2],'g',label=tcar3)
    ll=plt.legend(loc='upper left',fontsize=14)
    plt.xlabel('Latitude',fontsize=14)
    plt.ylabel('W/m2',fontsize=14)
    plt.title('Annual mean incoming solar radiation TOA',fontsize=14)
    plt.show(block=False)

#=============================================================

def plot_yt(var,tcar):

    import numpy as np
    from matplotlib import pyplot as plt
    from mod1 import solar_grid

    sun_grid = solar_grid()
    lat=sun_grid['lat']
    lon=sun_grid['lon']
    days=sun_grid['days']
    days_mid=sun_grid['days_mid']

    var=np.real(var)
    mie=np.amin(var);mae=np.amax(var)
    mabs=np.amax([np.abs(mie),mae])
    colc=True
    if (colc):
        scale=np.linspace(-mabs,mabs,51)
    else:
        scale=np.linspace(mie,mae,51)

    fig1=plt.figure(figsize=(10,5))
    c=plt.contourf(days,lat,var,scale,cmap=plt.cm.jet)
    plt.contour(days,lat,var,[0],colors='w',linewidths=2)
    plt.title(tcar,fontsize=14)
    plt.ylabel('Latitude',fontsize=14)
    plt.xticks(days_mid,('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'),fontsize=14)
    plt.colorbar(c,orientation='vertical')
    plt.show(block=False)

#=============================================================

def plot_xy(var,tcar,x,y):

    import numpy as np
    from matplotlib import pyplot as plt

    var=np.real(var)
    mie=np.amin(var);mae=np.amax(var)
    scale=np.linspace(mie,mae,51)
    fig1=plt.figure(figsize=(10,5))
    c=plt.contourf(x,y,np.transpose(var),scale)
    plt.colorbar(c,orientation='vertical')
    plt.title(tcar)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show(block=False)

#=============================================================

def read_ERBE(data_dir):
    
    import numpy as np

    solar_am=np.loadtxt('{}/solar_insolation_am.dat'.format(data_dir))
    asr_am=np.loadtxt('{}/absorbed_solar_radiation_am.dat'.format(data_dir))
    olr_am=np.loadtxt('{}/OLR_am.dat'.format(data_dir))
    solar_reflected_am=np.loadtxt('{}/reflected_SW_radiation_am.dat'.format(data_dir))
    planetary_albedo_am=np.loadtxt('{}/planetary_albedo_am.dat'.format(data_dir))
    lon_erbe=np.loadtxt('{}/lon_erbe.dat'.format(data_dir));nlon=np.size(lon_erbe)
    lat_erbe=np.loadtxt('{}/lat_erbe.dat'.format(data_dir));nlat=np.size(lat_erbe)
    
    nt=48
    var=np.loadtxt('{}/reflected_SW_radiation_Feb1985_Jan1989.dat'.format(data_dir))
    reflected_SW_monthly=np.reshape(var,(nt,nlat,nlon))
    var=np.loadtxt('{}/solar_insolation_Feb1985_Jan1989.dat'.format(data_dir))
    solar_insolation_monthly=np.reshape(var,(nt,nlat,nlon))
    var=np.loadtxt('{}/planetary_albedo_Feb1985_Jan1989.dat'.format(data_dir))
    planetary_albedo_monthly=np.reshape(var,(nt,nlat,nlon))
    var=np.loadtxt('{}/OLR_Feb1985_Jan1989.dat'.format(data_dir))
    OLR_monthly=np.reshape(var,(nt,nlat,nlon))
    var=np.loadtxt('{}/absorbed_solar_radiation_Feb1985_Jan1989.dat'.format(data_dir))
    ASR_monthly=np.reshape(var,(nt,nlat,nlon))

    #np.shape(OLR_monthly[1,:,:])
    #plt.contourf(lon_erbe,lat_erbe,OLR_monthly[1,:,:])
    #plt.show()

    ERBE = {'solar_am':solar_am,'olr_am':olr_am,'asr_am':asr_am,'solar_reflected_am':solar_reflected_am,'alpha_p_am':planetary_albedo_am,'lon_erbe':lon_erbe,'lat_erbe':lat_erbe,'solar_reflected_mon':reflected_SW_monthly,'solar_mon':solar_insolation_monthly,'alpha_p_mon':planetary_albedo_monthly,'olr_mon':OLR_monthly,'asr_mon':ASR_monthly}
    
    return ERBE

#=============================================================

def ebm(epsilon,S0,alpha_type,ho,Tsi,tpert,radp,ifig):

    import os
    import numpy as np
    from matplotlib import pyplot as plt
    from mod1 import qnet_toa

    rhoa=1.0 # air density (kg/m3)
    cpa=1.0e3 # specific heat capacity of air (J/K/kg)
    rdry=287.0 # J/K/kg
    g0=9.806 # acceleration of Earth's gravity at the surface (m/s2) 
    Te=255.0 # ref atmospheric temp. here taken as emission temp.
    ha=rdry*Te/g0 # atmospheric scale height (m)
    rhow=1030.0 # seawater density (kg/m3)
    cpo=4.0e3 # specific heat capacity of air (J/K/kg)
    Ca=rhoa*cpa*ha # atmospheric heat capacity (J/K/m2)
    Co=rhow*cpo*ho # seawater heat capacity (J/K/m2)
    C=Ca+Co # total ocean+atmos heat capacity
    spy=365*86400 # seconds per year
    dt=0.01*spy # model timestep
    zerodk=273.15 # 0 degrees Celcius
    sigma=5.67e-8 # Stefan-Boltzmann constant (W/m2/K4)
    time_max=10.0  # model time integration (years)
    
    #print('Atmospheric scale height = '+str(ha)+' m')
    #print('Water  depth = '+str(ho)+' m')
    #print('ATMOS heat capacity = '+str(Ca*1.0e-7)+' 10^7 J/K/m2')
    #print('OCEAN heat capacity = '+str(Co*1.0e-7)+' 10^7 J/K/m2')
    #print('TOTAL heat capacity = '+str(C*1.0e-7)+' 10^7 J/K/m2')

    nt=int(np.floor(time_max*spy/dt))
    time=np.linspace(0,time_max,nt)
    T=np.zeros(nt)
    T[0]=Tsi+tpert
    for it in range(nt-1):
        asr,olr,qnet=qnet_toa(T[it],epsilon,S0,alpha_type,radp)
        T[it+1]=T[it]+dt*qnet/C

    if (ifig):
        plt.figure(figsize=(12,8))
        plt.subplot(2,2,1)
        plt.plot(time,T-Tsi,'r')
        plt.xlabel('Time (years)',fontsize=14)
        plt.ylabel('degrees Celcius',fontsize=14)
        plt.title('Surface Temperature Anomaly',fontsize=14)
        plt.subplot(2,2,2)
        plt.plot(time,T,'b')
        plt.xlabel('Time (years)',fontsize=14)
        plt.title('Surface Temperature',fontsize=14);
        plt.show(block=False)

    #planck_feedback = -4.0*sigma*epsilon*T[0]**3
    #tau_eq=-(C/planck_feedback)/spy
    #print('Radiative Equilibrium Timescale = '+str(tau_eq)+' years')

    resu={'T':T,'time':time,'C':C}
    
    return resu

#=============================================================

def albedo(T,alpha_type):

    import numpy as np

    n=np.size(T)
    if n==1:
        Tv=np.array([T])
    else:
        Tv=T
    
    alpha=np.zeros(n)
    dalpha_dT=np.zeros(n)
    if alpha_type=='uniform':
        alpha=0.3
        dalpha_dT=0.0
    elif alpha_type=='linear':
        Tmin=210.0 # same as in ebm_fixed_points
        Tmax=330.0 #
        alpha=0.7-0.4*(Tv-Tmin)/(Tmax-Tmin)
        dalpha_dT=-0.4/(Tmax-Tmin)
        #Tmin=273.15-30.0 # same as in ebm_fixed_points
        #Tmax=273.15+10.0
        #alpha=0.3+0.3*(Tmax-T)/(Tmax-Tmin)
        #dalpha_dT=-0.3/(Tmax-Tmin)
    elif alpha_type=='nonlinear':
        alpha_i=0.7 # albedo of very cold ice-covered planet
        alpha_o=0.289 # albedo of warm ice-free planet
        To=293.0 # threshold temperature above which our model assumes the planet is ice-free
        Ti=260.0 # threshold temperature below which our model assumes the planet is completely ice covered. 
        for i in range(n):
            if (Tv[i] <= Ti):
                alpha[i]=alpha_i
                dalpha_dT[i]=0.0
            elif (Tv[i]>=To):
                alpha[i]=alpha_o
                dalpha_dT[i]=0.0
            else:
                alpha[i]= alpha_o + (alpha_i-alpha_o)*((Tv[i]-To)/(Ti-To))**2
                dalpha_dT[i]=2.0*(alpha_i-alpha_o)*(Tv[i]-To)/(Ti-To)**2
        
    return alpha,dalpha_dT

#=============================================================

def qnet_toa(T,epsilon,S0,alpha_type,radp):
    
    import numpy as np
    from mod1 import albedo

    alpha,dalpha_dT=albedo(T,alpha_type)
    sigma=5.67e-8
    asr=(1-alpha)*S0/4
    olr=epsilon*sigma*np.power(T,4)
    qnet=asr-olr+radp

    return [asr,olr,qnet]

#=============================================================

def peakdet(v, delta, x = None):

    import numpy as np
    import sys
    
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    
    Returns two arrays
    
    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %      
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.
    
    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.
    
    """
    maxtab = []
    mintab = []
       
    if x is None:
        x = np.arange(len(v))
    
    v = np.asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not np.isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN
    
    lookformax = True
    
    for i in np.arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return np.array(maxtab), np.array(mintab)

#=============================================================

def ebm_fixed_points(epsilon,S0,alpha_type,radp):

    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.optimize
    from mod1 import qnet_toa
    #from scipy.signal import find_peaks
    from mod1 import peakdet
    
    # temperature range
    t0=180
    t1=350
    n=1000
    temp=np.linspace(t0,t1,n)
    asr,olr,qnet=qnet_toa(temp,epsilon,S0,alpha_type,radp)

    # Identify first the intervals where roots possibly exist
    # This step is necessary when dealing with the Newton method applied
    # to nonlinear equations...
    #b, _ = find_peaks(abs(qnet))
    
    aa, bb = peakdet(abs(qnet),0.1);b=aa[1:,0].astype(int)
    
    lb=len(b)
    if (b.size==0):
        lb=lb+1
        t_int=[float(temp[0])]+[float(temp[-1])]
        ni=lb
    else:
        t_int=[float(temp[0])]+temp[b].tolist()+[float(temp[-1])]
        ni=lb+1 # number of intervals [ta tb]
    
    # Newton-Raphson convergence method with small tolerance
    def newton_raphson(t_int,ni,epsilon,S0,alpha_type):
        teq_stable=[]
        teq_unstable=[]
        tol=1e-2 # precision on roots (tolerance)
        delta=1e-3 # delta temperature to compute derivative of qnet
        nmax=1000 # usually converges for niter < 10
        nc=10 # number of possible corrections on I.C.
        for i in range(ni):
            tnmid=0.5*(t_int[i]+t_int[i+1])
            tn=tnmid # initial guess
            dra=1    # dummy value
            niter=0
            icp=1
            icm=1
            while (abs(dra) > tol) & (niter < nmax):
                asr,olr,qnet=qnet_toa(tn,epsilon,S0,alpha_type,radp)
                asr,olr,qnetp=qnet_toa(tn+delta,epsilon,S0,alpha_type,radp)
                asr,olr,qnetm=qnet_toa(tn-delta,epsilon,S0,alpha_type,radp)
                dp=(qnetp-qnetm)/(2*delta)
                dra=-qnet/dp
                tn=tn+dra
                niter=niter+1
                if (tn > t_int[i+1]): # tn out of range
                    tn=tnmid+icp*(t_int[i+1]-tnmid)/nc
                    dra=1
                    icp=icp+1
                if (tn < t_int[i]): # tn out of range
                    tn=tnmid-icm*(t_int[i+1]-tnmid)/nc
                    dra=1
                    icm=icm+1
            if (niter<nmax) & (tn > 0):
                if (dp < 0): # stable solution
                    teq_stable.append(tn)
                elif (dp > 0): # unstable solution
                    teq_unstable.append(tn)
        return teq_stable, teq_unstable

    teq_stable, teq_unstable = newton_raphson(t_int,ni,epsilon,S0,alpha_type)

    return teq_stable, teq_unstable

#=============================================================

def feedback_factors(temp,alpha_type,epsilon,S0):
    
    import numpy as np
    from mod1 import albedo

    sigma=5.67e-8
    
    alpha,dalpha_dT=albedo(temp,alpha_type)

    print('Equilibrium temperature = '+str(temp)+' K')

    lambda_a=-0.25*S0*dalpha_dT
    lambda_o=-4*epsilon*sigma*temp**3
    lambda_all=lambda_a+lambda_o
    
    print('Planck feedback = '+str(lambda_o)+' W/m2/K')
    print('Albedo feedback = '+str(lambda_a)+' W/m2/K')
    print('Net feedback ='+str(lambda_all)+' W/m2/K')

    resu={'lambda_o':lambda_o,'lambda_a':lambda_a,'lambda_all':lambda_all}
    return resu

#=============================================================

def feedback_factors_EBM_1D(resu,ifig):

    import numpy as np
    from scipy.stats import linregress
    from matplotlib import pyplot as plt

    ny,ntp=np.shape(resu['sat'])
    b_asr=np.zeros(ny)
    b_olr=np.zeros(ny)
    var1=resu['sat']-np.transpose(np.tile(resu['sat'][:,0],(ntp,1)))
    var2=resu['ASR']-np.transpose(np.tile(resu['ASR'][:,0],(ntp-1,1)))
    var3=resu['OLR']-np.transpose(np.tile(resu['OLR'][:,0],(ntp-1,1)))
    for j in range(ny):
        Basr, Aasr, r_value, p_value, std_err = linregress(var1[j,:-1],var2[j,:])
        Bolr, Aolr, r_value, p_value, std_err = linregress(var1[j,:-1],var3[j,:])
        b_asr[j]=Basr
        b_olr[j]=Bolr

    if ifig:
        plt.figure(figsize=(8,5))
        plt.plot(resu['lat'],b_olr,'r',label=r'Planck feedback: $\lambda_o$')
        plt.plot(resu['lat'],b_asr,'b',label=r'Ice-albedo feedback: $\lambda_a$')
        plt.legend(loc='best',fontsize=14)
        plt.xlabel('Latitude',fontsize=14)
        plt.xlim(-90,90)
        plt.ylabel(r'W m$^{-2}$ K$^{-1}$',fontsize=14)
        plt.title('Climate feedback parameters',fontsize=14)
        plt.show(block=False)

    # computation of global average feedback factors must be done with
    # global averages of OLR, ASR, and SAT to yield correct estimation of
    # climate sensitivity - It should not be made from the spatial averages
    # of the previous coefficients since
    # <lambda Delta T> not equal to <lambda> <Delta T> ...

    var1=resu['satmean']-resu['satmean'][0]
    var2=resu['ASRm']-resu['ASRm'][0]
    var3=resu['OLRm']-resu['OLRm'][0]
    Basr, Aasr, r_value, p_value, std_err = linregress(var1,var2)
    Bolr, Aolr, r_value, p_value, std_err = linregress(var1,var3)

    lambda_tot = Basr - Bolr
    return Basr, Bolr, lambda_tot

#=============================================================

def ebm_bifurcation_diagram(S0,epsilon,alpha_type,radp):

    import os
    import numpy as np
    from matplotlib import pyplot as plt
    from mod1 import ebm_fixed_points

    zerodk=273.15

    n1=np.size(S0)
    n2=np.size(epsilon)
    n=max(n1,n2)
    tstab=np.zeros((n,3))
    tunstab=np.zeros((n,3))
    S0=S0*np.ones(n)
    epsilon=epsilon*np.ones(n)

    for i in range(n):
        teq_stab,teq_unst=ebm_fixed_points(epsilon[i],S0[i],alpha_type,radp)
        tstab[i,:len(teq_stab)]=teq_stab
        tunstab[i,:len(teq_unst)]=teq_unst
    
    tstab[tstab==0]=float('nan')
    tunstab[tunstab==0]=float('nan')

    fig1=plt.figure(figsize=(10,6))
    if n1 > n2:
        plt.plot(S0,tstab[:,0]-zerodk,'k',label='stable branch')
        plt.plot(S0,tunstab[:,0]-zerodk,'k--',label='unstable branch')
        plt.plot(S0,tstab[:,1:2]-zerodk,'k')
        plt.plot(S0,tunstab[:,1:2]-zerodk,'k--')
        plt.xlabel('solar constant S0 (W/m2)',fontsize=14)
        plt.title('Bifurcation diagram: sensitivity to S0',fontsize=14)
        ll=plt.legend(loc='upper left')
    else:
        plt.plot(epsilon,tstab[:,0]-zerodk,'k',label='stable branch')
        plt.plot(epsilon,tunstab[:,0]-zerodk,'k--',label='unstable branch')
        plt.plot(epsilon,tstab[:,1:2]-zerodk,'k')
        plt.plot(epsilon,tunstab[:,1:2]-zerodk,'k--')
        plt.xlabel('emissivity $\epsilon$',fontsize=14)
        plt.title('Bifurcation diagram: sensitivity to $\epsilon$',fontsize=14)
        ll=plt.legend(loc='upper right',fontsize=14)
    plt.ylabel('equilibrium temperature (deg. Celcius)',fontsize=14)
    plt.show(block=False)

#=============================================================

def ebm_annual(param):

    import numpy as np
    from matplotlib import pyplot as plt
    from mod1 import inferred_energy_transport
    import numba as nb

    time_kyr=param['time_kyr']
    falb=param['falb']
    folr=param['folr']
    fkdif=param['fkdif']
    A=param['A']
    B=param['B']
    esun=param['esun']
    epsilon_p=param['epsilon_p']
    epsilon_a=param['epsilon_a']
    epsilon_o=param['epsilon_o']
    D=param['D']
    nyears=param['nyears']
    dt_days=param['dt']
    S0=param['S0']
    radp=param['radp']
    ffig=param['ifig']
    #hs=param['hs']
    #laths=param['laths']
    fdiftype=1; # 1: 'implicit', 0: 'explicit'
    restart=param['restart']
    resu=param['resu_solar']
    lambda_T=param['lambda_T']
    ho=param['ho']
    aoht=param['aoht']

    S0_present_day=1365.0 # same as in routine insolation
    solar=(S0/S0_present_day)*resu['solar_am'] # annual mean solar forcing
    lat=resu['lat']
    ny=np.size(lat) # degrees

    latv=np.zeros(ny+1)
    latv=np.linspace(-90.0,90.0,ny+1)
    n_oht=1
    ymax=1./np.sqrt(3.0*np.float(n_oht))
    apoht=aoht/(ymax*(1-ymax*ymax)**n_oht)
    ohtc=np.zeros(ny) # W/m2 [Ocean Heat Transport Convergence]
    poht=np.zeros(ny+1) # Watts [Poleward Ocean Heat Transport]
    for j in range(ny+1):
        y=np.sin(latv[j]*np.pi/180.0)
        poht[j]=apoht*y*(1-y*y)**n_oht # Watts

    # aquaplanet: width of the ocean = 2*pi in longitude
    dlambda = 2*np.pi
    # poht(phi) = 2*pi*a*rhow*cpo*ho*[vT]*cosphi
    # rhow*cpo*ho*[vT]*cosphi = poht[j]/(2*pi*a)
    ray=6.37e+06
    ohtc=np.zeros(ny) # Watts/m2
    for j in range(ny):
        dphi = (latv[j+1]-latv[j])*np.pi/180.0
        cosphi=np.cos(lat[j]*np.pi/180.0)
        ohtc[j]=(poht[j]-poht[j+1])/(dlambda*ray*ray*dphi*cosphi)

    # point heat source
    hs=0
    laths=45.5
    hsf=np.zeros(ny)
    if (hs != 0.0):
        if (laths >= 0):
            jlaths=np.int(np.where(lat == laths)[0])
        hsf[jlaths]=hs
        
    # timestep and number of timestep for nyears model integration
    dt=dt_days*86400.0 # timestep in seconds
    spy=365.0*86400.0 # seconds per year
    nt=int(nyears*spy/dt) # number of time steps

    # grid
    earth_radius=6.37e+06
    dlat=lat[2]-lat[1]
    dy=earth_radius*dlat*np.pi/180.0
    cosphi=np.cos(lat*np.pi/180.0)
    beta=dt/(cosphi*dy**2) # coeff for implicit diffusion

    # heat capacity
    cpa=1004.0 # specific heat capacity of dry air (J/K/kg)
    ps=1.0e+05 # surface pressure (Pa)
    g0=9.806 # reference gravity at Earth surface
    rhow=1030.0 # reference seawater density (kg/m3)
    cpo=3996.0 # specific heat capacity of water (J/K/kg)
    Ca=cpa*ps/g0 # J/K/m2 [Atmospheric Heat Capacity]
    Co=rhow*cpo*ho # J/K/m2 [Oceanic Heat Capacity]

    # Initial Conditions (surface temperatures SAT and SST in degrees Celcius)
    sst_init=np.zeros(ny)
    sat_init=np.zeros(ny)
    if (restart == 0):
        t0=12.0
        t2=-40.0
        for j in range(ny):
            p2_legendre=0.5*(3.0*np.sin(lat[j]*np.pi/180.0)**2 - 1.0)
            sat_init[j]=t0+t2*p2_legendre
            sst_init[j]=t0+t2*p2_legendre
    else:
        sst_init=param['ssti']
        sat_init=param['sati']

    def eddy_diff(temp,lat,D,C,fkdif):
        # Atmospheric Eddy diffusivity (m2/s)
        # is either constant or function of the meridional SAT gradient (Vallis formulation)
        earth_radius=6.37e+06
        ny=lat.size
        dlat=lat[2]-lat[1]
        kbg=2.0e+06 # background eddy diffusivity
        K=np.power(earth_radius,2.0)*(D/C)*np.ones(ny+1) # m^2/s
        if fkdif==1:
            dphi=np.deg2rad(dlat)
            K=kbg*np.ones(ny+1)
            for j in range(1,ny-1,1):
                K[j]+=0.5*D*np.abs(temp[j]-temp[j-1])/dphi # m^2/s
        return K

    '''
    @nb.jit(nopython=True)
    def cfl_criteria(dt,K,dy,fdiftype):
        # CFL criteria    
        if (np.max(K) > 0) and (fdiftype==0):
            dt_max=dy**2/(2.0*np.max(K))
            if (dt > dt_max):
                print('Time step = ', dt ,' seconds > CFL(K) ', dt_max ,' seconds')
                return
    '''
    
    def diff_T(temp,lat,beta,K,diff_method,dt):
        # diffusion term in the atmosphere
        # explicit OR implicit method (implicit much better)
        ny=lat.size
        dlat=lat[2]-lat[1]
        earth_radius=6.37e+06
        dphi=dlat*np.pi/180.0
        dy=dphi*earth_radius
        latv=np.zeros(ny+1)
        latv=np.linspace(-90.0,90.0,ny+1)
        cosphi=np.cos(lat*np.pi/180.0)
        cosphiv=np.cos(latv*np.pi/180.0)
        tdif=np.zeros(ny)
        if diff_method==0:
            tdif[0]=K[1]*cosphiv[1]*(temp[1]-temp[0])/(cosphi[0]*dy**2)
            tdif[-1]=K[-2]*cosphiv[-2]*(temp[-2]-temp[-1])/(cosphi[-1]*dy**2)
            for j in range(1,ny-1,1):
                fluxout=K[j+1]*cosphiv[j+1]*(temp[j+1]-temp[j])
                fluxin=K[j]*cosphiv[j]*(temp[j]-temp[j-1])
                tdif[j]=(fluxout-fluxin)/(cosphi[j]*dy**2)
        elif diff_method==1:
            tempi=temp
            beta_diag=np.zeros(ny)
            beta_up=np.zeros(ny-1)
            beta_down=np.zeros(ny-1)
            mat_diff=np.zeros((ny,ny))
            rhs_ta=np.zeros(ny)
            beta_diag[0]=1.0+beta[0]*(cosphiv[1]*K[1])
            beta_diag[ny-1]=1.0+beta[ny-1]*(cosphiv[ny-1]*K[ny-1])
            beta_diag[1:ny]=1.0+beta[1:ny]*(cosphiv[2:ny+1]*K[2:ny+1]+cosphiv[1:ny]*K[1:ny])
            rhs_ta=temp
            for j in range(ny-1):
                beta_down[j]=-beta[j+1]*cosphiv[j+1]*K[j+1]
                beta_up[j]=-beta[j]*cosphiv[j+1]*K[j+1]
            mat_diff=np.diag(beta_diag)+np.diag(beta_down,-1)+np.diag(beta_up,1)
            #inv_mat=np.linalg.pinv(mat_diff, rcond=1e-15) # SVD decomposition: more elegant and robust but slow
            inv_mat=np.linalg.inv(mat_diff)
            tempn=np.dot(inv_mat,rhs_ta)
            tdif=(tempn-tempi)/dt
        return tdif

    def olr_ebm_annual(folr,A,B,epsilon,Ts,radp):
        # Compute OLR given sea surface temperature
        # OLR is either a linear function of SST (linear fit to observations)
        # or follows the standard Stefan-Boltzman law in T^4
        # In this latter case the atmospheric emissivity must be specified.
        ny=Ts.size
        olr=np.zeros(ny)
        if folr==0:
            olr=A+B*Ts # fit to observations (epsilon = 1)
        elif folr==1:
            zerodk=273.15
            sigma=5.67e-08
            olr=epsilon*sigma*np.power(Ts+zerodk,4.0)
        olr+=-radp
        return olr

    def albedo_ebm_annual(falb,Ts,lat):
        # Compute planetary albedo
        # The albedo can be uniform (falb=0), latitude dependent (falb=1), or
        # latitude and temperature dependent (falb=2),
        # or only temperature dependent (falb=3, as in Saravanan McWilliams 1995)
        # The ice-albedo feedback is present when it is function of temperature, it
        # is absent otherwise.
        ny=lat.size
        albedo=np.empty_like(Ts) #np.zeros(ny)
        iceline=np.zeros(2)
        zerodk=273.15
        Tf=-10.0 # freezing temperature below which ice is present (high albedo)
        a0=0.3
        a2=0.078
        ai=0.62 # ice albedo
        if falb==0:
            alpha_p=0.3 # planetary albedo
            albedo=alpha_p*np.ones(ny)
        elif falb==1:
            p2_legendre=0.5*(3.0*np.sin(lat*np.pi/180.0)**2 - 1.0)
            a0=0.321
            a2=0.241
            albedo=a0 + a2*p2_legendre
        if falb==2:
            a0=0.3
            a2=0.078
            ai=0.62 # ice albedo
            p2_legendre=0.5*(3.0*np.sin(lat*np.pi/180.0)**2 - 1.0)
            albedo=a0 + a2*p2_legendre
            ind_ice=np.where(Ts<Tf)[0]
            albedo[ind_ice]=ai
        elif falb==3:
            toce=295.0
            tice=240.0
            ai=0.65
            ao=0.25
            Tf=tice-zerodk
            for j in range(ny):
                albedo[j]=ai
                if (Ts[j]+zerodk > toce):
                    albedo[j]=ao
                if (Ts[j]+zerodk > tice) and( Ts[j]+zerodk < toce):
                    albedo[j]=ao+(ai-ao)*(toce-zerodk-Ts[j])/(toce-tice)
        # latitude of sea ice edge ?
        lat_in=0.0
        lat_is=0.0
        for j in range(ny):
            if (lat[j] > 0):
                jeq=j
                break
        for j in range(ny-1,jeq-1,-1):
            if (Ts[j] > Tf):
                lat_in=lat[j]+0.5
                break
        for j in range(jeq):
            if (Ts[j] > Tf):
                lat_is=lat[j]-0.5
                break
        iceline[0]=lat_is
        iceline[1]=lat_in
        return albedo, iceline
    
    def mainloopebm(ny,nt,lat,dt,Ca,Co,D,beta,radp,solar,sst_init,sat_init,hsf,falb,fkdif,fdiftype,esun,epsilon_p,epsilon_a,epsilon_o,ohtc):
        # Main Loop of the EBM
        # A predictor-corrector method is used
        # see https://en.wikipedia.org/wiki/Predictor%E2%80%93corrector_method
        sigma=5.67e-8
        zerodk=273.15
        iceline=np.zeros((2,nt))
        K=np.zeros((ny+1,nt))
        rhs_solar=np.zeros((ny,nt))
        rhs_olr=np.zeros((ny,nt))
        rhs_br=np.zeros((ny,nt))
        rhs_lws=np.zeros((ny,nt))
        rhs_qsens=np.zeros((ny,nt))
        dyn_contrib=np.zeros((ny,nt))
        sat=np.zeros((ny,nt+1))
        sst=np.zeros((ny,nt+1))
        satnm1=sat_init
        sstnm1=sst_init
        sat[:,0]=sat_init
        sst[:,0]=sst_init
        for it in range(nt):
            
            # predictor
            albedo, icelatnm1 = albedo_ebm_annual(falb,sstnm1,lat)
            rhs_solarnm1=solar*(1.0-albedo)
            rhs_olrnm1=olr_ebm_annual(folr,A,B,epsilon_p,satnm1,radp)
            rhs_brnm1= epsilon_a*sigma*(satnm1+zerodk)**4.0
            rhs_lwsnm1 = epsilon_o*sigma*(sstnm1+zerodk)**4
            rhs_qsensnm1 = lambda_T*(satnm1-sstnm1)
            Knm1=eddy_diff(satnm1,lat,D,Ca,fkdif)
            rhs_diffnm1=diff_T(satnm1,lat,beta,Knm1,fdiftype,dt) # diffusion term K/s
            rhs_satnm1 = (esun*rhs_solarnm1-rhs_olrnm1 + rhs_lwsnm1 - rhs_brnm1 - rhs_qsensnm1 + hsf)/Ca + rhs_diffnm1
            rhs_sstnm1 = (rhs_qsensnm1 + (1.-esun)*rhs_solarnm1 - rhs_lwsnm1 + rhs_brnm1 + ohtc)/Co
            satn = satnm1 + dt*rhs_satnm1
            sstn = sstnm1 + dt*rhs_sstnm1
            
            # corrector
            albedo, icelatn = albedo_ebm_annual(falb,sstn,lat)
            rhs_solarn=solar*(1.0-albedo)
            rhs_olrn=olr_ebm_annual(folr,A,B,epsilon_p,satn,radp)
            rhs_brn= epsilon_a*sigma*(satn+zerodk)**4.0
            rhs_lwsn = epsilon_o*sigma*(sstn+zerodk)**4.0
            rhs_qsensn = lambda_T*(satn-sstn)
            Kn=eddy_diff(satnm1,lat,D,Ca,fkdif)
            rhs_diffn=diff_T(satnm1,lat,beta,Kn,fdiftype,dt) # diffusion term K/s
            rhs_satn = (esun*rhs_solarn-rhs_olrn + rhs_lwsn - rhs_brn - rhs_qsensn + hsf)/Ca + rhs_diffn
            rhs_sstn = (rhs_qsensn + (1.-esun)*rhs_solarn - rhs_lwsn + rhs_brn + ohtc)/Co
            satn = satnm1 + 0.5*dt*(rhs_satn+rhs_satnm1)
            sstn = sstnm1 + 0.5*dt*(rhs_sstn+rhs_sstnm1)

            satnm1=satn
            sstnm1=sstn
            rhs_solar[:,it]=rhs_solarnm1
            rhs_olr[:,it]=rhs_olrnm1
            rhs_br[:,it]=rhs_brnm1
            rhs_lws[:,it]=rhs_lwsnm1
            rhs_qsens[:,it]=rhs_qsensnm1
            sat[:,it+1]=satn
            sst[:,it+1]=sstn
            K[:,it]=Knm1
            iceline[:,it]=icelatnm1
            dyn_contrib[:,it]=Ca*rhs_diffnm1
            satmax=np.max(np.abs(satn));tyr=it*dt/(365.*86400.)
            if (satmax > 1.0e03):
                print('**********************************************')
                print('STOP: CLIMATE SOLUTION DOES NOT CONVERGE')
                print('      max |SAT| = '+ '%0.0f' %satmax +' deg.C at year '+ '%0.1f' %tyr)
                print('      TIME STEP MUST BE DECREASED')
                print('**********************************************')
                break
        return rhs_solar, rhs_olr, sat, sst, rhs_diffn, K, iceline, rhs_qsens, rhs_br, rhs_lws
    
    rhs_solar, rhs_olr, sat, sst, rhs_diff, K, iceline,rhs_qsens, rhs_br, rhs_lws =mainloopebm(ny,nt,lat,dt,Ca,Co,D,beta,radp,solar,sst_init,sat_init,hsf,falb,fkdif,fdiftype,esun,epsilon_p,epsilon_a,epsilon_o,ohtc)
    
    # Poleward Energy Transport (PW) inferred from imbalance at TOA
    pet,phtd=inferred_energy_transport(rhs_solar[:,-1],rhs_olr[:,-1],sat[:,-1],lat,rhs_diff,Ca);

    # Net surface heat flux toward ocean
    qnet = rhs_qsens + (1.-esun)*rhs_solar + rhs_br - rhs_lws
    
    # Global averages
    sat_ave=np.zeros(nt)
    sst_ave=np.zeros(nt)
    ASR_ave=np.zeros(nt)
    OLR_ave=np.zeros(nt)
    QNET_ave=np.zeros(nt)
    cosphi=np.cos(lat*np.pi/180.0)
    for it in range(nt):
        sat_ave[it]=sum(sat[:,it]*cosphi)/sum(cosphi)
        sst_ave[it]=sum(sst[:,it]*cosphi)/sum(cosphi)
        ASR_ave[it]=sum(rhs_solar[:,it]*cosphi)/sum(cosphi)
        OLR_ave[it]=sum(rhs_olr[:,it]*cosphi)/sum(cosphi)
        QNET_ave[it]=sum(qnet[:,it]*cosphi)/sum(cosphi)

    # figures
    time=np.linspace(0,nt*dt/(365.0*86400),nt+1)
    if (ffig==1):

        plt.figure(figsize=(6,10))
        plt.subplots_adjust(hspace=0.3)
        plt.subplot(3,1,1)
        plt.plot(time[:-1],sat_ave,'b',label='SAT')
        plt.plot(time[:-1],sst_ave,'r',label='SST')
        plt.legend(loc='best',fontsize=14)
        plt.title('Average SAT and SST (deg.C)',fontsize=14)
        plt.xlim(0,nyears)
        plt.subplot(3,1,2)
        plt.plot(time[:-1],ASR_ave-OLR_ave,'k')
        plt.title('Average radiative forcing at TOA (>0 downward) (W/m2)',fontsize=14)
        plt.xlim(0,nyears)
        plt.subplot(3,1,3)
        plt.plot(time[:-1],QNET_ave,'k')
        plt.title('Average surface heat flux (>0 downward) (W/m2)',fontsize=14)
        plt.xlabel('Time (years)',fontsize=14)
        plt.xlim(0,nyears)

        plt.figure(figsize=(6,5))
        plt.plot(time[:-1],iceline[0,:],'b')
        plt.plot(time[:-1],iceline[1,:],'b')
        plt.xlabel('Time (years)')
        plt.xlim(0,nyears)
        plt.ylim(-90,90)
        plt.title('Latitude of sea ice edge')

        plt.figure(figsize=(6,4))
        plt.plot(lat,sat[:,-1],'b',label='SAT')
        plt.plot(lat,sst[:,-1],'r',label='SST')
        plt.legend(loc='best',fontsize=14)
        plt.title('SAT and SST (deg.C)')
        plt.plot([iceline[0,-1],iceline[0,-1]],[-100,100],'k--')
        plt.plot([iceline[1,-1],iceline[1,-1]],[-100,100],'k--')
        mie=np.amin([np.amin(sat[:,-1]),np.amin(sst[:,-1])])-2.
        mae=np.amax([np.amax(sat[:,-1]),np.amax(sst[:,-1])])+2.
        plt.ylim(mie,mae)
        plt.xlim(-90,90)
        plt.xlabel('Latitude')
    
        plt.figure(figsize=(6,6))
        plt.plot(lat,rhs_solar[:,-1],'r',label='ASR')
        plt.plot(lat,rhs_olr[:,-1],'b',label='OLR')
        plt.legend(loc='best')
        plt.title('Energy balance at TOA (W/m2)')
        plt.xlim(-90,90)
        plt.xlabel('Latitude')
        plt.legend(loc='best')

        plt.figure(figsize=(6,6))
        plt.plot(lat,(1.-esun)*rhs_solar[:,-1],'r',label='SOLAR')
        plt.plot(lat,rhs_br[:,-1],'b',label='QLWDA')
        plt.plot(lat,-rhs_lws[:,-1],'g',label='QLWUO')
        plt.plot(lat,rhs_qsens[:,-1],'orange',label='QSENS')
        plt.plot(lat,qnet[:,-1],'k',linewidth=2,label='QNET')
        plt.plot(lat,np.zeros(ny),'k--')
        plt.title('Energy balance at the surface (W/m2)')
        plt.xlim(-90,90)
        plt.xlabel('Latitude')
        plt.legend(loc='best')
        
        plt.figure(figsize=(6,6))
        plt.plot(lat,qnet[:,-1],'r',linewidth=2,label='QNET')
        plt.plot(lat,ohtc,color='b',label='OHTC')
        plt.plot(lat,qnet[:,-1]+ohtc,'k--',label='QNET+OHTC')
        plt.xlim(-90,90)
        plt.xlabel('Latitude')
        plt.legend(loc='best')

        plt.figure(figsize=(6,4))
        latv=np.zeros(ny+1)
        latv=np.linspace(-90.0,90.0,ny+1)
        plt.plot(latv,pet,'r',label='from ASR-OLR')
        plt.plot(latv,phtd,'b',label='Atmospheric Heat Transport')
        plt.plot(latv,poht*1.0e-15,'g',label='Ocean Heat Transport')
        plt.plot(latv,phtd+poht*1.0e-15,'k',label='Atmospheric+Oceanic Heat Transport')
        plt.plot([-90,90],[0,0],linestyle='dashed',color='k')
        plt.xlim(-90,90)
        plt.legend(loc='best')
        plt.title('Poleward Energy transport',fontsize=14)
        plt.ylabel('PW',fontsize=14)
        plt.xlabel('Latitude',fontsize=14)
        plt.show(block=False)

    print('solar constant = '+str(S0)+' W/m2')
    print('global average SAT = '+str(sat_ave[-1])+' deg.C')
    print('global average SST = '+str(sst_ave[-1])+' deg.C')
    print('global average OLR = '+str(OLR_ave[-1])+' W/m2')
    print('global average ASR = '+str(ASR_ave[-1])+' W/m2')
    
    #print('time step = '+str(dt)+' seconds')
    #print('water depth = '+str(water_depth)+' m')
    #print('heat capacity = ', C*1.0e-07 ,' 10^7 J/m2/K')
    if (np.max(iceline)==0):
        print('Snowball Earth !!')
    elif (np.min(np.abs(iceline))==90.0):
        print('Ice free Earth !!')
    else:
        print('Iceline: SH = '+str(iceline[0,-1])+' deg. lat. / NH = '+str(iceline[1,-1])+' deg. lat.')
    print(' ')
    
    struct_ebm = {'lat':lat,'time':time,'sat':sat,'sst':sst,'ASR':rhs_solar,'OLR':rhs_olr,'PHT':pet,'PHTD':phtd,'ASRm':ASR_ave,'OLRm':OLR_ave,'K':K,'iceline':iceline,'satmean':sat_ave,'sstmean':sst_ave,'ohtc':ohtc,'poht':poht}
    
    return struct_ebm

#=============================================================

def effect_D_ebm(Darray,param):

    import numpy as np
    from matplotlib import pyplot as plt
    from mod1 import ebm_annual

    model_list = []
    Tmean_list = []
    deltaT_list = []
    Hmax_list = []
    yis_list = []
    yin_list = []
    for D in Darray:
        param['D']=D
        print('D = '+str(D) ,' W/m2/K')
        resu=ebm_annual(param)
        satmean=resu['satmean'][-1]
        deltaT = np.max(resu['sat'][:,-1])-np.min(resu['sat'][:,-1])
        HT = resu['PHT'] # ocean+atmos poleward heat transport
        Hmax = np.max(np.abs(HT))
        y_ice_south=resu['iceline'][0,-1]
        y_ice_north=resu['iceline'][1,-1]
        Tmean_list.append(satmean)
        deltaT_list.append(deltaT)
        Hmax_list.append(Hmax)
        yis_list.append(y_ice_south)
        yin_list.append(y_ice_north)

    color1 = 'b'
    color2 = 'r'
    fig = plt.figure(figsize=(8,6))
    ax1 = fig.add_subplot(111)
    ax1.plot(Darray, deltaT_list, color=color1, label='$\Delta T$')
    ax1.plot(Darray, Tmean_list, '--', color=color1, label='$\overline{T}$')
    ax1.set_xlabel('D (W m$^{-2}$ K$^{-1}$)', fontsize=14)
    ax1.set_xticks(np.arange(Darray[0], Darray[-1], 0.2))
    ax1.set_ylabel('Temperature ($^\circ$C)', fontsize=14,  color=color1)
    for tl in ax1.get_yticklabels():
        tl.set_color(color1)
    ax1.legend(loc='center right')
    ax2 = ax1.twinx()
    ax2.plot(Darray, Hmax_list, color=color2)
    ax2.set_ylabel('Maximum Poleward heat transport', fontsize=14, color=color2)
    for tl in ax2.get_yticklabels():
        tl.set_color(color2)
    ax1.set_title('Effect of diffusivity on EBM with albedo feedback', fontsize=16)
    ax1.grid()

    fig = plt.figure(figsize=(8,6))
    plt.plot(Darray,yis_list,'b')
    plt.plot(Darray,yin_list,'r')
    plt.xlabel('D (W m$^{-2}$ K$^{-1}$)', fontsize=14)
    plt.ylabel('Latitude', fontsize=14)
    plt.title('Latitude of the sea ice edge', fontsize=14)
    plt.show(block=False)

#=============================================================

def inferred_energy_transport(ASR,OLR,temp,lat,rhs_diff,C):

    import numpy as np
    
    ny=np.size(lat)
    dlat=lat[2]-lat[1]
    dphi=dlat*np.pi/180.0
    cosphi=np.cos(lat*np.pi/180.0)
    netflxdn=ASR-OLR # net downward radiation flux at TOA: ASR - OLR

    # radiative imbalance at TOA
    rad_imbal=sum(netflxdn*cosphi)/sum(cosphi)
    print('Radiative imbalance at TOA = ', rad_imbal ,' W/m2')

    # remove global mean
    if (rad_imbal!=0):
        netflxdn+=-rad_imbal

    pht=np.zeros(ny+1)
    for j in range(ny):
        pht[j+1]=np.sum(netflxdn[0:j]*cosphi[0:j]*dphi);

    earth_radius=6.37e+06
    pht=1.e-15*2.0*np.pi*pht*earth_radius**2 # units PW

    # diffusive heat transport
    phtd=np.zeros(ny+1)
    for j in range(ny):
        phtd[j+1]=-np.sum(rhs_diff[0:j]*cosphi[0:j]*dphi);

    phtd=C*1.e-15*2.0*np.pi*phtd*earth_radius**2 # units PW

    return pht,phtd

#=============================================================

def plot_map(data,lon,lat,tcar):

    import numpy as np
    from mpl_toolkits.basemap import Basemap
    from matplotlib import pyplot as plt

    fig1=plt.figure(figsize=(10,7))
    
    mie=np.amin(data);mae=np.amax(data)
    scale=np.linspace(mie,mae,51)

    map = Basemap(projection='mill', llcrnrlon=lon.min(), urcrnrlon=lon.max(), llcrnrlat=lat.min(), urcrnrlat=lat.max(), resolution='c')

    # convert the lat/lon values to x/y projections.
    x, y = map(*np.meshgrid(lon,lat))

    # plot the field using the fast pcolormesh routine 
    # set the colormap to jet.
    map.contourf(x,y,np.transpose(data),scale,cmap=plt.cm.jet)
    #map.pcolormesh(x,y,np.transpose(data),shading='flat',cmap=plt.cm.jet)
    map.colorbar(location='right')

    # Add a coastline and axis values.
    map.drawcoastlines(linewidth=0.5)
    map.fillcontinents(color='None', lake_color='White')
    map.drawmapboundary(fill_color='None')
    map.drawmeridians(np.arange(0,360,60),labels=[0,0,0,1])
    map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])

    # Add a title, and then show the plot.
    plt.title(tcar)
    plt.show(block=False)
    
#=============================================================

def erbe_season(var):

    import numpy as np

    nt,nlat,nlon=np.shape(var)

    months=list(np.linspace(2,12,11)) #months of the first year
    months+=list(np.linspace(1,12,12)) #months of the second year
    months+=list(np.linspace(1,12,12)) #months of the third year
    months+=list(np.linspace(1,12,12)) #months of the fourth year
    months+=[1]

    var_season=np.zeros((nlon,nlat,12))
    for it in range(12):
        ind = [i for i, j in enumerate(months) if j == it+1]
        var_season[:,:,it]=np.transpose(np.mean(var[ind,:,:],0))

    return var_season

#=============================================================

def plot_season_ave(var,lon,lat,tcar):

    import numpy as np
    from mod1 import erbe_season, planet_average
    from matplotlib import pyplot as plt

    j0=np.amin(np.where(lat>0))

    var_season=erbe_season(var)

    varglo=planet_average(var_season,lat,lon,lat)
    varnh=planet_average(var_season,lat[j0:],lon,lat)
    varsh=planet_average(var_season,lat[0:j0-1],lon,lat)

    month=np.linspace(1,12,12)
    
    fig1=plt.figure(figsize=(10,5))
    plt.plot(month,varglo,'k',label='Global')
    plt.plot(month,varnh,'r',label='NH')
    plt.plot(month,varsh,'b',label='SH')
    plt.title(tcar)
    plt.xticks(month,('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'))
    ll=plt.legend(loc='upper right')
    plt.show(block=False)

#=============================================================

def poleward_energy_transport(netflxdn,lon,lat):

    import numpy as np
    from mod1 import area_planet, planet_average
    from matplotlib import pyplot as plt

    varm=planet_average(netflxdn,lat,lon,lat)

    # remove global mean to get zero average --> needed to compute energy transport
    if (varm!=0):
        print("global mean ", varm ," removed")
        netflxdn+=-varm

    nlat=np.size(lat)

    area=area_planet(lon,lat)
    
    # Northward Energy Transport
    pht=np.zeros(nlat+1)
    for j in range(nlat):
        pht[j+1]=np.sum(np.sum(netflxdn[:,0:j]*area[:,0:j]));

    pht=1.e-15*pht # units PW
        
    lat_g=np.zeros(nlat+1)
    lat_g[1:nlat]=(lat[0:nlat-1]+lat[1::])/2
    lat_g[0]=-90
    lat_g[nlat]=90

    fig1=plt.figure(figsize=(10,5))
    plt.plot(lat_g,pht,'k')
    plt.plot(lat_g,np.zeros(nlat+1),'k--')
    plt.xlabel('Latitude',fontsize=14)
    plt.xlim(-90,90)
    plt.ylabel('PW',fontsize=14)
    plt.title('Energy transport by the entire climate system',fontsize=14)
    plt.show(block=False)
    
#=============================================================

def response_initial_perturbation(param,delta_T):

    import numpy as np
    from mod1 import ebm_annual
    from matplotlib import pyplot as plt
    
    # first run control experiment
    param.update({'restart':0,'ifig':0})
    resu0=ebm_annual(param)
    Ts_eq=resu0['sat'][:,-1]
    ASR_eq=resu0['ASR'][:,-1]
    OLR_eq=resu0['OLR'][:,-1]
    lat=resu0['lat']

    # Then run the perturbed experiment
    sati=resu0['sat'][:,-1]+delta_T
    ssti=resu0['sst'][:,-1]+delta_T
    param.update({'restart':1,'ssti':ssti,'sati':sati})
    resu1=ebm_annual(param)
    Ts_pert=resu1['sat'][:,0]
    ASR_pert=resu1['ASR'][:,0]
    OLR_pert=resu1['OLR'][:,0]

    plt.figure(figsize=(8,8))
    plt.subplots_adjust(wspace = 0.3)
    n1=int(365/param['dt'])
    plt.subplot(2,1,1)
    plt.plot(lat,Ts_eq,'k',linewidth=2,label='Teq (CTRL)')
    plt.plot(lat,resu1['sat'][:,0],'b--',label='Tpert (t=0)')
    plt.plot(lat,resu1['sat'][:,n1],'g--',label='Tpert (t=1y)')
    plt.plot(lat,resu1['sat'][:,3*n1],'r--',label='Tpert (t=3y)')
    plt.plot(lat,resu1['sat'][:,5*n1],'y--',label='Tpert (t=5y)')
    plt.plot([-90,90],[0,0],'k--')
    plt.plot([-90,90],[-10,-10],'b--')
    plt.ylabel('deg.C',fontsize=14)
    plt.title('Surface air temperature',fontsize=14)
    plt.legend(loc='best',fontsize=12)
    plt.subplot(2,1,2)
    plt.plot(lat,resu0['sst'][:,-1],'k',linewidth=2,label='Teq (CTRL)')
    plt.plot(lat,resu1['sst'][:,0],'b--',label='Tpert (t=0)')
    plt.plot(lat,resu1['sst'][:,n1],'g--',label='Tpert (t=1y)')
    plt.plot(lat,resu1['sst'][:,3*n1],'r--',label='Tpert (t=3y)')
    plt.plot(lat,resu1['sst'][:,5*n1],'y--',label='Tpert (t=5y)')
    plt.plot([-90,90],[0,0],'k--')
    plt.plot([-90,90],[-10,-10],'b--')
    plt.xlabel('Latitude',fontsize=14)
    plt.ylabel('deg.C',fontsize=14)
    plt.title('Sea surface temperature',fontsize=14)
    plt.legend(loc='best',fontsize=12)

    plt.figure(figsize=(8,8))
    plt.subplots_adjust(wspace = 0.3)
    plt.subplot(2,1,1)
    plt.plot(lat,ASR_eq,'r',label='ASR equilibrium')
    plt.plot(lat,ASR_pert,'r--',label='ASR perturbed (t=0)')
    plt.plot(lat,OLR_eq,'b',label='OLR equilibrium')
    plt.plot(lat,OLR_pert,'b--',label='OLR perturbed (t=0)')
    plt.legend(loc='best',fontsize=12)
    plt.ylabel(r'W m$^{-2}$',fontsize=14)
    plt.title('ASR and OLR',fontsize=14)
    plt.subplot(2,1,2)
    plt.plot(lat,OLR_pert-OLR_eq,'b',label=r'$\Delta$OLR')
    plt.plot(lat,ASR_pert-ASR_eq,'r',label=r'$\Delta$ASR')
    plt.legend(loc='best',fontsize=12)
    plt.ylabel(r'W m$^{-2}$',fontsize=14)
    plt.xlabel('Latitude',fontsize=14)
    plt.title('changes in ASR and OLR',fontsize=14)

    plt.figure(figsize=(6,8))
    plt.subplots_adjust(hspace = 0.3)
    nt=len(resu1['time'])-1
    plt.subplot(3,1,1)
    plt.plot(resu1['time'][:-1],resu0['satmean'][-1]*np.ones(nt),'r--',label='equilibrium')
    plt.plot(resu1['time'][:-1],resu1['satmean'],'r',label='perturbed')
    plt.title('Average surface temperature',fontsize=14)
    plt.legend(loc='best')
    plt.ylabel(r'$^\circ$C',fontsize=14)
    plt.subplot(3,1,2)
    plt.plot(resu1['time'][:-1],resu0['iceline'][1,-1]*np.ones(nt),'b--',label='equilibrium')
    plt.plot(resu1['time'][:-1],resu1['iceline'][1,:],'b',label='perturbed')
    plt.legend(loc='best')
    plt.title('Iceline position (NH)',fontsize=14)
    plt.ylabel('Latitude',fontsize=14)
    plt.subplot(3,1,3)
    plt.plot(resu1['time'][:-1],resu1['OLRm'],'b',label='OLR')
    plt.plot(resu1['time'][:-1],resu1['ASRm'],'r',label='ASR')
    plt.legend(loc='best')
    plt.title('Average OLR and ASR',fontsize=14)
    plt.ylabel(r'W m$^{-2}$',fontsize=14)
    plt.xlabel('Time (years)',fontsize=14)
    plt.show(block=False)

    d_olr=resu1['OLRm'][0]-resu0['OLRm'][-1]
    d_asr=resu1['ASRm'][0]-resu0['ASRm'][-1]

    return d_olr, d_asr

#=============================================================

def response_CO2_levels(param,co2r):

    import numpy as np
    from mod1 import ebm_annual
    from mod1 import feedback_factors_EBM_1D
    from matplotlib import pyplot as plt

    co2for=5.35 # W/m2
    #co2_baseline=280.0 #ppm
    #radf=co2for*np.log(co2_levels/co2_baseline)
    radf=co2for*np.log(co2r)

    n=len(co2r)
    lat=param['resu_solar']['lat']
    sat=np.zeros((len(lat),n))
    sst=np.zeros((len(lat),n))
    sstmean=np.zeros(n)
    satmean=np.zeros(n)
    bb_tot=np.zeros(n)
    bb_olr=np.zeros(n)
    bb_asr=np.zeros(n)
    for i in range(n):
        print('CO2 x '+str(co2r[i]))
        param.update({'radp':radf[i],'ifig':0})
        resu=ebm_annual(param)
        sst[:,i]=resu['sst'][:,-1];
        sat[:,i]=resu['sat'][:,-1];
        sstmean[i]=resu['sstmean'][-1];
        satmean[i]=resu['satmean'][-1];
        b_asr, b_olr, b_tot = feedback_factors_EBM_1D(resu,0)
        bb_tot[i]=b_tot
        bb_olr[i]=b_olr
        bb_asr[i]=b_asr
        
    # estimate temperature change from climate feedbacks
    delta_T_linear = - radf/bb_tot

    plt.figure(figsize=(6,12))
    plt.subplots_adjust(hspace=0.5)
    plt.subplot(3,1,1)
    for i in range(n):
        tcar=str('CO2 x '+str(co2r[i]))
        plt.plot(lat,sat[:,i],label=tcar)
    plt.ylabel('deg.C',fontsize=14)
    plt.legend(loc='best',fontsize=12)
    plt.title('Equilibrium Surface Air Temperature',fontsize=14)
    plt.subplot(3,1,2)
    for i in range(1,n,1):
        tcar=str('CO2 x '+str(co2r[i])+' minus CO2 x '+str(co2r[i-1]))
        plt.plot(lat,sat[:,i]-sat[:,i-1],label=tcar)
    plt.ylabel('deg.C',fontsize=14)
    plt.legend(loc='best',fontsize=12)
    plt.xlabel('Latitude',fontsize=14)
    plt.title(r'$\Delta$ SAT',fontsize=14)
    plt.subplot(3,1,3)
    plt.plot(co2r,sstmean-sstmean[0],'rx-',label=r'$\Delta$ SST')
    plt.plot(co2r,satmean-satmean[0],'bx-',label=r'$\Delta$ SAT')
    #plt.plot(co2r,delta_T_linear,color='orange',label=r'$\Delta$ SAT from feedbacks')
    plt.legend(loc='best',fontsize=14)
    plt.xlabel('$CO2/CO2_{ref}$',fontsize=14)
    plt.ylabel('deg.C',fontsize=14)
    plt.title('Global temperature changes',fontsize=14)
    plt.show(block=False)

#=============================================================
  
def ebm_solar_sensitivity(param,S0array):

    import numpy as np
    from mod1 import ebm_annual
    from matplotlib import pyplot as plt

    iceline=np.zeros(S0array.size)
    iceline_t=np.zeros((2,int(param['nyears']*365/param['dt']),S0array.size))
    satmean=np.zeros(S0array.size)
    ASRm=np.zeros(S0array.size)
    OLRm=np.zeros(S0array.size)
    pht=np.zeros(S0array.size)
    lat=param['resu_solar']['lat']
    sat_eq=np.zeros((len(lat),S0array.size))
    sst_eq=np.zeros((len(lat),S0array.size))
    restart=param['restart']
    ssti=param['ssti']
    sati=param['sati']
    
    for n in range(S0array.size):
        S0=S0array[n]
        param.update({'S0':S0,'restart':restart,'ssti':ssti,'sati':sati})
        resu0=ebm_annual(param)
        iceline[n]=resu0['iceline'][1,-1] # NH
        iceline_t[:,:,n]=resu0['iceline']
        satmean[n]=resu0['satmean'][-1]
        ASRm[n]=resu0['ASRm'][-1]
        OLRm[n]=resu0['OLRm'][-1]
        pht[n]=np.max(np.abs(resu0['PHT']))
        restart=1
        sati=resu0['sat'][:,-1]
        ssti=resu0['sst'][:,-1]
        sat_eq[:,n]=sati
        sst_eq[:,n]=ssti

    tebm=resu0['time']
    resu={'iceline':iceline,'iceline_t':iceline_t,'satmean':satmean,'ASRm':ASRm,'OLRm':OLRm,'pht_max':pht,'sat_eq':sat_eq,'sst_eq':sst_eq,'time':tebm,'lat':lat}
    return resu

#=============================================================

def make_fig_cool_warm(S0array,S1array,resu_cool,resu_warm):

    import numpy as np
    from matplotlib import pyplot as plt

    plt.figure(figsize=(8,8))
    plt.subplots_adjust(hspace = 0.3)
    plt.subplots_adjust(wspace = 0.3)
    plt.subplot(2,2,1)
    ind=np.max(np.where(resu_cool['iceline']>0)) 
    lat_min=resu_cool['iceline'][ind] # critical latitude
    plt.plot(S0array,resu_cool['iceline'],'r')
    plt.plot(S1array,resu_warm['iceline'],'b')
    plt.plot([np.min(S0array),np.max(S0array)],[lat_min,lat_min],'k--')
    plt.title('a) iceline',fontsize=14)
    plt.ylabel('Latitude',fontsize=14)
    plt.subplot(2,2,2)
    plt.plot(S0array,resu_cool['satmean'],'r')
    plt.plot(S1array,resu_warm['satmean'],'b')
    plt.title('b) Ts',fontsize=14)
    plt.ylabel(r'$^\circ$C',fontsize=14)
    plt.subplot(2,2,3)
    plt.plot(S0array,resu_cool['ASRm'],'r')
    plt.plot(S1array,resu_warm['ASRm'],'b')
    plt.title('c) ASR',fontsize=14)
    plt.ylabel(r'W m$^{-2}$',fontsize=14)
    plt.xlabel(r'$S_0$ (W m$^{-2}$)',fontsize=14)
    plt.subplot(2,2,4)
    plt.plot(S0array,resu_cool['OLRm'],'r')
    plt.plot(S1array,resu_warm['OLRm'],'b')
    plt.title('d) OLR',fontsize=14)
    plt.ylabel(r'W m$^{-2}$',fontsize=14)
    plt.xlabel(r'$S_0$ (W m$^{-2}$)',fontsize=14)

    plt.figure(figsize=(6,6))
    plt.plot(resu_cool['time'][:-1],resu_cool['iceline_t'][0,:,ind+1],'k')
    plt.plot(resu_cool['time'][:-1],resu_cool['iceline_t'][1,:,ind+1],'k')
    plt.title(r'iceline for $S_0$ = '+str(np.int(100*S0array[ind+1])/100)+'W/m2',fontsize=14)
    plt.xlabel('Time (years)',fontsize=14)
    plt.ylabel('Latitude',fontsize=14)

    plt.figure(figsize=(4,4)) # Ts of snowball state
    plt.plot(resu_cool['lat'],resu_cool['sat_eq'][:,-1],'b',label='S0=1200')
    plt.plot(resu_cool['lat'],resu_cool['sat_eq'][:,0],'r',label='S0=1400')
    plt.legend(loc='best')
    plt.xlabel('Latitude')
    plt.ylabel('deg.C')
    plt.title('Ts snowball state')
    plt.show(block=False)
