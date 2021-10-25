#=============================================================
# Introduction to Ocean and Climate
# Master 1 Marine Physics

# This file contains modules needed for the second computer class:
#
#   * distribution of insolation, eccentricity, obliquity, seasons, ...
#   * one dimensional energy balance model
#   * atmospherc observations
#
# last modif: 26 Oct 2020 / author: oarzel@univ-brest.fr
#
#=============================================================

def read_data(years,var,data_dir):

    import numpy as np
    from netCDF4 import Dataset

    # number of days over the period
    # needed to allocate memory for outpout files
    lpyr = (np.mod(years,4)==0) # leap year
    dpy = np.ones(np.size(years))*365+lpyr # days per year
    nt=int(np.sum(dpy)) # number of days for the whole time period

    if var=='U':
        scale_factor=0.01;add_offset=202.66;
        netcdf_prefix='uwnd';netcdf_var='uwnd';npres=17
    elif var=='V':
        scale_factor=0.01;add_offset=202.66;
        netcdf_prefix='vwnd';netcdf_var='vwnd';npres=17
    elif var=='T':
        scale_factor=0.01;add_offset=477.65;
        netcdf_prefix='air';netcdf_var='air';npres=12
    elif var=='Q':
        scale_factor=1.e-06;add_offset=0.032666;
        netcdf_prefix='shum';netcdf_var='shum';npres=8
    elif var=='Z':
        scale_factor=1.0;add_offset=32066.0;
        netcdf_prefix='hgt';netcdf_var='hgt';npres=12
    elif var=='S':
        scale_factor=0.01;add_offset=1202.65;
        netcdf_prefix='slp';netcdf_var='slp';npres=0

    nlon=144
    nlat=73
    if var=='S':
        varclim=np.zeros((nt,nlat,nlon))
    else:
        varclim=np.zeros((nt,npres,nlat,nlon))

    itmin=0;
    # read data
    ipinf=False
    for i in range(len(years)):
        print('read ', var ,' year ', years[i])
        filename=str(data_dir+"/"+netcdf_prefix+"."+str(years[i])+".nc")
        nc_fid = Dataset(filename,'r')
        ipinf=False
        if (ipinf):
            print (nc_fid.dimensions.keys())
            print (nc_fid.file_format)
            print (nc_fid.variables.keys())
            print (nc_fid.variables[netcdf_var])
        if var!='S':
            pres=nc_fid['level'][:];npres=len(pres)
        lon=nc_fid['lon'][:];nlon=len(lon)
        lat=nc_fid['lat'][:];nlat=len(lat)
        varc=nc_fid[netcdf_var][:] #*scale_factor+add_offset
        itmax=int(dpy[i]+itmin) #exclusive
        if var=='S':
            varclim[itmin:itmax,:,:]=varc
        else:
            varclim[itmin:itmax,:,:,:]=varc
        itmin=itmax
        nc_fid.close()

    if var=='S':
        resu={var:varclim,'lon':lon,'lat':lat}
    else:
        resu={var:varclim,'pres':pres,'lon':lon,'lat':lat}

    return resu

#============================================================

def vertical_profile(data_dir,months,lat_range,var,z_coord,tcar,ifig):

    # compute and display vertical profiles of temperature, specific humidify,
    # or any other quantities
    # data are long term (1981-2010) monthly mean quantities
    #
    # use : varm, zcoord = vertical_profile(data_dir,months,lat_range,var,z_coord,tcar,ifig)
    #
    # input :
    #   data_dir : name of the directory where data are to be read
    #   months : months over which the time average is perfomed
    #   lat_range : latitude ranges to be considered
    #   var : 'T', 'Q' , 'U' , 'V', 'Z'
    #   z_coord : 'p' for pressure coordinates,'z' for altiude (meters) coordinates
    #   tcar : title of the figure
    #   ifig : 0/1 flag to display figure
    #
    # output : - variable 'varm' as a function of vertical coordinates for all
    #            latitude ranges : dimensions varm[nz,nr]
    #            where nz=number of pressure/z levels
    #            and nr the number of latitude intervals
    #          - vertical coordinate 'zcoord' (dimension nz)
    #
    # examples :
    # 1/ Annual mean vertical profile of global mean temperature (deg.C) as a function of altitude
    # varm,zccord=vertical_profile(data_dir,np.linspace(1,12,12),[-90,90],'T','z','Vertical profile of global mean temperature (deg.C)')
    # 2/ DJF mean vertical profile of temperature (deg.C) in the 10S-10N latitude range as a function of pressure
    # varm,zccord=vertical_profile(data_dir,[12,1,2],[-10,10],'T','p','Vertical profile of global mean temperature (deg.C)')
    # 3/ Annual mean vertical profile of temperature (deg.C) in the 10S-10N, 40N-50N and 70N-80N latitude
    #    ranges as a function of altitude
    # varm,zccord=vertical_profile(data_dir,np.linspace(1,12,12),[-10,10,40,50,70,80],'T','z','Annual mean vertical profiles of temperature (deg.C)')

    import numpy as np
    from matplotlib import pyplot as plt
    from mod2 import read_data_ltm,area_planet

    resu=read_data_ltm(months,var,data_dir)

    nr=int(len(lat_range)/2)
    nz=len(resu['pres'])
    nlat=len(resu['lat'])
    nlon=len(resu['lon'])

    area=area_planet(resu['lon'],resu['lat'])
    varm=np.zeros((nz,nr))
    varc=resu[var]
    
    for i in range(nr):
        lat0=lat_range[2*i]
        lat1=lat_range[2*i+1]
        j1=np.amax(np.where(resu['lat']>=lat0))
        j0=np.amin(np.where(resu['lat']<=lat1))
        varm[:,i]=np.sum(np.sum(varc[:,j0:j1,:]*np.tile(np.transpose(area[:,j0:j1]), \
            (nz,1,1)),axis=2),axis=1)/np.tile(np.sum(np.sum(area[:,j0:j1])),nz)

    if z_coord=='z':
        #(International Reference Atmosphere)
        hatm=6.8 # atmospheric scale height according to CIRA
        # The COSPAR International Reference Atmosphere (CIRA) is an empirical
        # model of the atmosphere of Earth. It consists of a set of tables of
        # average air pressures, altitudes and temperatures. The CIRA models
        # are developed by the Committee on Space Research (COSPAR) and have
        # been important for the planning of spaceflight.
        # see also http://ccmc.gsfc.nasa.gov/modelweb/atmos/cospar1.html
        ps0=1013
        zcoord=-hatm*np.log(resu['pres']/ps0)
        ycar="Altitude (km)"
    elif z_coord=='p':
        zcoord=resu['pres']
        ycar="Pressure (mb)"

    if (ifig):
        
        if var=='T':
            xcar="Temperature (deg.C)"
        elif var=='Tp':
            xcar="Potential Temperature (K)"
        elif var=='Q':
            xcar="Specific Humididy (g/kg)"
        elif var=='U':
            xcar="Zonal velocity U (m/s)"
        elif var=='V':
            xcar="Meridional velocity V (m/s)"
        elif var=='Z':
            xcar="Geopotential Height (m)"

        # legend
        sl=np.sign(lat_range)
        cs=[]
        for i in range(2*nr):
            if (sl[i] > 0):
                cs.append('N')
            else:
                cs.append('S')

        tcarleg=[]
        for i in range(nr):
            lat0=lat_range[2*i]
            lat1=lat_range[2*i+1]
            tcarleg.append(str(str(abs(lat0))+cs[2*i]+"-"+str(abs(lat1))+cs[2*i+1]))
    
        fig1=plt.figure(figsize=(5,5))
        plt.plot(varm,zcoord)
        plt.xlabel(xcar,fontsize=14)
        plt.ylabel(ycar,fontsize=14)
        plt.title(tcar,fontsize=14)
        plt.xlim(np.amin(np.amin(varm)),np.amax(np.amax(varm)))
        ll=plt.legend(tcarleg,loc='upper right',fontsize=14)
        if z_coord=='p':
            plt.gca().invert_yaxis()
        plt.show(block=False)

        # LAPSE RATE
        if var=='T':
            ps0=1013
            zcoord=-hatm*np.log(resu['pres']/ps0)
            kmax=np.amax(np.where(zcoord<= 10)) # to compute lapse rate in the first 10 km
            dTdz=-(varm[kmax,:]-varm[0,:])/(zcoord[kmax]-zcoord[0])
            for i in range(nr):
                print("Averaged lapse rate in the first 10 km is ", '%.4f' %dTdz[i] ," deg.C/km at latitudes", tcarleg[i])

    return varm, zcoord

#============================================================

def vertical_profile_season(data_dir,var):

    import numpy as np
    from matplotlib import pyplot as plt
    from mod2 import vertical_profile

    if var=='T':
        xcar="Temperature (deg. C)";mie=-90;mae=30;zmax=30;
    if var=='Tp':
        xcar="Potential Temperature (K)";mie=250;mae=800;zmax=30;
    elif var=='Q':
        xcar="Specific Humidity (g/kg)";mie=0;mae=10;zmax=10;

    fig1=plt.figure(figsize=(4.5,9))
    plt.subplots_adjust(hspace = 0.5)
    p1=plt.subplot(3,1,1)
    varm1,z1=vertical_profile(data_dir,np.linspace(1,12,12),[-10,10],var,'z','Annual mean T',False)
    varm2,z2=vertical_profile(data_dir,np.array([6,7,8]),[-10,10],var,'z','JJA mean T',False)
    varm3,z3=vertical_profile(data_dir,np.array([12,1,2]),[-10,10],var,'z','DJF mean T',False)
    plt.plot(varm1,z1,'k',label='Annual Mean')
    plt.plot(varm2,z2,'r',label='JJA')
    plt.plot(varm3,z2,'b',label='DJF')
    plt.ylabel('Altitude (km)',fontsize=14)
    tcar=str("a) "+var+" profile 10S-10N");plt.title(tcar,fontsize=14)
    plt.xlim(mie,mae);plt.ylim(0,zmax)
    plt.legend(loc="upper right",fontsize=14)

    p2=plt.subplot(3,1,2)
    varm1,z1=vertical_profile(data_dir,np.linspace(1,12,12),[40,50],var,'z','Annual mean T',False)
    varm2,z2=vertical_profile(data_dir,np.array([6,7,8]),[40,50],var,'z','JJA mean T',False)
    varm3,z3=vertical_profile(data_dir,np.array([12,1,2]),[40,50],var,'z','DJF mean T',False)
    plt.plot(varm1,z1,'k',label='Annual Mean')
    plt.plot(varm2,z2,'r',label='JJA')
    plt.plot(varm3,z2,'b',label='DJF')
    plt.ylabel('Altitude (km)',fontsize=14)
    tcar=str("b) "+var+" profile 40N-50N");plt.title(tcar,fontsize=14)
    plt.xlim(mie,mae);plt.ylim(0,zmax)

    p3=plt.subplot(3,1,3)
    varm1,z1=vertical_profile(data_dir,np.linspace(1,12,12),[70,80],var,'z','Annual mean T',False)
    varm2,z2=vertical_profile(data_dir,np.array([6,7,8]),[70,80],var,'z','JJA mean T',False)
    varm3,z3=vertical_profile(data_dir,np.array([12,1,2]),[70,80],var,'z','DJF mean T',False)
    plt.plot(varm1,z1,'k',label='Annual Mean')
    plt.plot(varm2,z2,'r',label='JJA')
    plt.plot(varm3,z2,'b',label='DJF')
    plt.ylabel('Altitude (km)',fontsize=14)
    tcar=str("c) "+var+" profile 70N-80N");plt.title(tcar,fontsize=14)
    plt.xlim(mie,mae);plt.ylim(0,zmax)
    plt.xlabel(xcar,fontsize=14)

    plt.show(block=False)

#============================================================

def temperature_structure(data_dir):

    import os
    import numpy as np
    from mod2 import zonal_average,vertical_profile,vertical_profile_season
    from matplotlib import pyplot as plt

    colc=False
    add_contour=True
    
    # Zonal averages
    tr=[0,0]
    zonal_average(data_dir,np.linspace(1,12,12),'T','T (deg.C) annual mean',colc,add_contour,tr,cmapname=plt.cm.jet)
    #plt.savefig('T_zonal_annual.png',dpi=100)
    zonal_average(data_dir,np.array([12,1,2]),'T','T (deg.C) DJF',colc,add_contour,tr,cmapname=plt.cm.jet)
    #plt.savefig('T_zonal_DJF.png',dpi=100)
    zonal_average(data_dir,np.array([6,7,8]),'T','T (deg.C) JJA',colc,add_contour,tr,cmapname=plt.cm.jet)
    #plt.savefig('T_zonal_JJA.png',dpi=100)

    # Vertical profiles
    vertical_profile(data_dir,np.linspace(1,12,12),[-90,90],'T','z','Annual mean T',True)
    #plt.savefig('T_z_global_average_annual_mean.png',dpi=100)
    vertical_profile(data_dir,np.linspace(1,12,12),[-10,10,40,50,70,80],'T','z','Annual mean T',True)
    #plt.savefig('T_z_regions_annual_mean.png',dpi=100)
    vertical_profile_season(data_dir,'T')
    #plt.savefig('T_z_regions_seasons.png',dpi=100)

    #os.system("mv *.png figures/.")

#=============================================================

def plot_xy_map(data,lon,lat,tcar,icenter,colc,tr,cmapname):

    import numpy as np
    from mpl_toolkits.basemap import Basemap

    # actually done using basemap
    # should be updated to cartopy
    # import cartopy.crs as ccrs
    # import cartopy.feature as cfeature
    # my_proj=ccrs.PlateCarree()

    from matplotlib import pyplot as plt

    if (icenter): # map centered on Greenwich meridian
        datac=np.zeros((len(lat),len(lon)))
        nlon_greenwich=np.int(len(lon)/2.0)
        datac[:,:nlon_greenwich]=data[:,nlon_greenwich:]
        datac[:,nlon_greenwich:]=data[:,:nlon_greenwich]
        lon=lon-180.0
    else:
        datac=data
        
    fig1=plt.figure(figsize=(10,8))
    
    mie=np.nanmin(data);mae=np.nanmax(data)
    mabs=max(abs(mie),mae)

    if (colc):
        scale=np.linspace(-mabs,mabs,51)
    else:
        scale=np.linspace(mie,mae,51)
        if np.amax(np.abs(tr)) > 0:
            scale=np.linspace(tr[0],tr[1],51)

    map = Basemap(projection='mill', llcrnrlon=lon.min(), urcrnrlon=lon.max(), llcrnrlat=lat.min(), urcrnrlat=lat.max(), resolution='c')

    # convert the lat/lon values to x/y projections.
    x, y = map(*np.meshgrid(lon,lat))

    # plot the field using the fast pcolormesh routine 
    # set the colormap to jet.
    map.contourf(x,y,datac,scale,cmap=cmapname)
    #map.pcolormesh(x,y,np.transpose(data),shading='flat',cmap=plt.cm.jet)
    cbar=map.colorbar(location='right')
    
    # Add a coastline and axis values.
    map.drawcoastlines(linewidth=0.5)
    map.fillcontinents(color='None', lake_color='White')
    map.drawmapboundary(fill_color='None')
    map.drawmeridians(np.arange(0,370,60),labels=[0,0,0,1],fontsize=12)
    map.drawparallels(np.arange(-90,100,30),labels=[1,0,0,0],fontsize=12)
    plt.clim(-mabs,mabs)

    # Add a title, and then show the plot.
    plt.title(tcar,fontsize=14)
    plt.show(block=False)

#=============================================================

def zonal_average(data_dir,months,var,tcar,colc,add_contour,tr,cmapname):

    import numpy as np
    from mod2 import read_data_ltm,plot_yp_zonal_mean
    
    resu=read_data_ltm(months,var,data_dir)

    varm=np.mean(resu[var],axis=2)
    
    output={'varm':varm,'pres':resu['pres'],'lon':resu['lon'],'lat':resu['lat']}

    plot_yp_zonal_mean(varm,resu['lat'],resu['pres'],tcar,colc,add_contour,tr,cmapname)

#=============================================================

def zonal_mean_winds(data_dir):

    import os
    import numpy as np
    from mod2 import zonal_average,read_data_ltm
    from matplotlib import pyplot as plt

    colc=True
    add_contour=True
    # zonal averages
    tr=[0,0]
    #zonal_average(data_dir,np.linspace(1,12,12),'U','U (m/s) annual mean',colc,add_contour,tr,cmapname=plt.cm.jet)
    #plt.savefig('U_zonal_annual.png',dpi=100)
    #zonal_average(data_dir,np.array([12,1,2]),'U','U (m/s) DJF',colc,add_contour,tr,cmapname=plt.cm.jet)
    #plt.savefig('U_zonal_DJF.png',dpi=100)
    #zonal_average(data_dir,np.array([6,7,8]),'U','U (m/s) JJA',colc,add_contour,tr,cmapname=plt.cm.jet)
    #plt.savefig('U_zonal_JJA.png',dpi=100)
    zonal_average(data_dir,np.linspace(1,12,12),'V','V (m/s) annual mean',colc,add_contour,tr,cmapname=plt.cm.seismic)
    #plt.savefig('V_zonal_annual.png',dpi=100)

    # zonally-averaged surface winds
    resu_am=read_data_ltm(np.linspace(1,12,12),'U',data_dir)
    resu_djf=read_data_ltm(np.array([12,1,2]),'U',data_dir)
    resu_jja=read_data_ltm(np.array([6,7,8]),'U',data_dir)
    
    fig1=plt.figure(figsize=(8,5))
    plt.plot(resu_am['lat'],np.mean(resu_am['U'][0,:,:],axis=1),'k',label='Annual Mean')
    plt.plot(resu_am['lat'],np.mean(resu_jja['U'][0,:,:],axis=1),'r',label='JJA')
    plt.plot(resu_am['lat'],np.mean(resu_djf['U'][0,:,:],axis=1),'b',label='DJF')
    plt.plot([-90,90],[0,0],'k',linestyle='dashed')
    plt.title('Zonally-averaged surface winds',fontsize=14)
    plt.xlabel('Latitude',fontsize=14)
    plt.ylabel('m s$^{-1}$',fontsize=14)
    plt.legend(loc='upper right')
    plt.show(block=False)
    #plt.savefig('zonal_average_surface_winds.png',dpi=100)


    fig=plt.figure(figsize=(10,12))
    lat=resu_am['lat']
    pres=resu_am['pres']
    plt.subplots_adjust(hspace=0.2)
    cmapname=plt.cm.jet
    ax1=plt.subplot(3,1,1)
    varn=np.mean(resu_am['U'],axis=2)
    mie=np.amin(varn);mae=np.amax(varn)
    mabs=np.amax([np.abs(mie),mae])
    scale=np.linspace(mie,mae,51)
    c1=plt.contourf(lat,pres,varn,scale,cmap=cmapname)
    plt.ylabel('pressure (mb)',fontsize=14)
    plt.gca().invert_yaxis()
    ax1.set_xticks([-90,-60,-30,0,30,60,90])
    ax1.set_xticklabels(['90S','60S','30S','EQ','30N','60N','90N'])
    plt.text(-85, 900, 'Annual Mean', {'color': 'k', 'fontsize': 14, 'ha': 'left', 'va': 'center','bbox':dict(boxstyle="round", fc="w", ec="k", pad=0.2)})

    ax2=plt.subplot(3,1,2)
    varn=np.mean(resu_djf['U'],axis=2)
    mie=np.amin(varn);mae=np.amax(varn)
    mabs=np.amax([np.abs(mie),mae])
    scale=np.linspace(mie,mae,51)
    c2=plt.contourf(lat,pres,varn,scale,cmap=cmapname)
    plt.ylabel('pressure (mb)',fontsize=14)
    plt.gca().invert_yaxis()
    ax2.set_xticks([-90,-60,-30,0,30,60,90])
    ax2.set_xticklabels(['90S','60S','30S','EQ','30N','60N','90N'])
    plt.text(-85, 900, 'DJF', {'color': 'k', 'fontsize': 14, 'ha': 'left', 'va': 'center','bbox':dict(boxstyle="round", fc="w", ec="k", pad=0.2)})

    ax3=plt.subplot(3,1,3)
    varn=np.mean(resu_jja['U'],axis=2)
    mie=np.amin(varn);mae=np.amax(varn)
    mabs=np.amax([np.abs(mie),mae])
    scale=np.linspace(mie,mae,51)
    c3=plt.contourf(lat,pres,varn,scale,cmap=cmapname)
    plt.xlabel('Latitude',fontsize=14)
    plt.ylabel('pressure (mb)',fontsize=14)
    plt.gca().invert_yaxis()
    ax3.set_xticks([-90,-60,-30,0,30,60,90])
    ax3.set_xticklabels(['90S','60S','30S','EQ','30N','60N','90N'])
    plt.text(-85, 900, 'JJA', {'color': 'k', 'fontsize': 14, 'ha': 'left', 'va': 'center','bbox':dict(boxstyle="round", fc="w", ec="k", pad=0.2)})

    box1 = ax1.get_position()
    box2 = ax2.get_position()
    box3 = ax3.get_position()
    cbaxes = fig.add_axes([0.01+box1.x1,box1.y0, 0.02, box1.y1-box1.y0]) 
    cb1=plt.colorbar(c1,orientation='vertical',cax=cbaxes)
    cbaxes = fig.add_axes([0.01+box2.x1,box2.y0, 0.02, box2.y1-box2.y0]) 
    cb2=plt.colorbar(c2,orientation='vertical',cax=cbaxes)
    cbaxes = fig.add_axes([0.01+box3.x1,box3.y0, 0.02, box3.y1-box3.y0]) 
    cb3=plt.colorbar(c3,orientation='vertical',cax=cbaxes)
    plt.show(block=False)
    #plt.savefig('zonal_average_zonal_winds.png',dpi=200,bbox_inches='tight')

    
    #os.system("mv *.png figures/.")

#=============================================================

def read_data_ltm(months,var,data_dir):

    import numpy as np
    from netCDF4 import Dataset

    if var=='U':
        scale_factor=1.0;add_offset=0.0;
        netcdf_prefix='uwnd';netcdf_var='uwnd';
    elif var=='V':
        scale_factor=1.0;add_offset=0.0;
        netcdf_prefix='vwnd';netcdf_var='vwnd';
    elif var=='T':
        scale_factor=1.0;add_offset=0.0;
        netcdf_prefix='air';netcdf_var='air';
    elif var=='Tp':
        scale_factor=1.0;add_offset=0.0;
        netcdf_prefix='pottmp';netcdf_var='pottmp';
    elif var=='Q':
        scale_factor=1.0;add_offset=0.0;
        netcdf_prefix='shum';netcdf_var='shum';
    elif var=='Z':
        scale_factor=1.0;add_offset=0.0;
        netcdf_prefix='hgt';netcdf_var='hgt';

    # read data
    # this directory must be modified by the student:
    filename=str(data_dir+"/"+netcdf_prefix+".mon.1981-2010.ltm.nc")
    nc_fid = Dataset(filename,'r')

    # information about the dataset:
    ipinf=False
    if (ipinf):
        print (nc_fid.dimensions.keys())
        print (nc_fid.file_format)
        print (nc_fid.variables.keys())
        print (nc_fid.variables[netcdf_var])

    lon=nc_fid['lon'][:];nlon=len(lon)
    lat=nc_fid['lat'][:];nlat=len(lat)
    pres=nc_fid['level'][:];npres=len(pres)
    varclim=np.zeros((nlon,nlat,len(pres)))
    varc=nc_fid[netcdf_var][:] #*scale_factor+add_offset
    varclim=np.mean(varc[months.astype(int)-1,:,:,:],axis=0)
    nc_fid.close()

    resu={var:varclim,'pres':pres,'lon':lon,'lat':lat}

    return resu

#=============================================================

def plot_yp_zonal_mean(var,lat,pres,tcar,colc,add_contour,tr,cmapname):

    import numpy as np
    from matplotlib import pyplot as plt

    fig1=plt.figure(figsize=(10,6))
    maxtr=np.amax(np.abs(tr))
    if maxtr==0:
        varn=var
        presn=pres
    else:
        varn=var[tr[0]:tr[1],:]
        presn=pres[tr[0]:tr[1]]

    mie=np.amin(varn);mae=np.amax(varn)
    mabs=np.amax([np.abs(mie),mae])
    if (colc):
        scale=np.linspace(-mabs,mabs,51)
    else:
        scale=np.linspace(mie,mae,51)
    c=plt.contourf(lat,presn,varn,scale,cmap=cmapname)
    if (add_contour):
        plt.rcParams['contour.negative_linestyle'] = 'dashed'
        plt.contour(lat,presn,varn,21,colors='k')

    plt.xlabel('Latitude',fontsize=14)
    plt.ylabel('pressure (mb)',fontsize=14)
    plt.gca().invert_yaxis()
    plt.title(tcar,fontsize=14)
    plt.colorbar(c,orientation='vertical')
    plt.show(block=False)

#=============================================================

def geopotential_height(data_dir):

    import os
    import numpy as np
    from matplotlib import pyplot as plt
    from mod2 import read_data_ltm,area_planet

    colc=True
    add_contour=True
    
    resu_am=read_data_ltm(np.linspace(1,12,12),'Z',data_dir)
    resu_djf=read_data_ltm(np.array([12,1,2]),'Z',data_dir)
    resu_jja=read_data_ltm(np.array([6,7,8]),'Z',data_dir)

    zx_am=np.mean(resu_am['Z'],axis=2)
    zx_jja=np.mean(resu_jja['Z'],axis=2)
    zx_djf=np.mean(resu_djf['Z'],axis=2)

    nz,nlat=np.shape(zx_am)

    # Annual and global mean geopotential height as a function of pressure
    # Here this is what we define as the "standard atmosphere"
    zm=np.zeros(nz);area=area_planet(resu_am['lon'],resu_am['lat'])
    zm=(np.sum(np.sum(resu_am['Z']*np.tile(np.transpose(area),(nz,1,1)),axis=2),axis=1))/np.sum(np.sum(area))

    hgeo_am=zx_am-np.transpose(np.tile(zm,(nlat,1)))
    hgeo_jja=zx_jja-np.transpose(np.tile(zm,(nlat,1)))
    hgeo_djf=zx_djf-np.transpose(np.tile(zm,(nlat,1)))

    tcar="Annual Mean Z (gpm) departure from global mean"
    plot_yp_zonal_mean(hgeo_am,resu_am['lat'],resu_am['pres'],tcar,colc,add_contour,[0,0],cmapname=plt.cm.jet)
    #plt.savefig('geopotential_height_zonal_mean_am.png',dpi=100)

    fig1=plt.figure(figsize=(4.5,9))
    plt.subplots_adjust(hspace = 0.5)
    p1=plt.subplot(3,1,1)
    k0=np.where(resu_am['pres']==100);kk0=int(k0[0])
    plt.plot(resu_am['lat'],hgeo_am[kk0,:],'k',label='Annual Mean')
    plt.plot(resu_am['lat'],hgeo_jja[kk0,:],'r',label='JJA')
    plt.plot(resu_am['lat'],hgeo_djf[kk0,:],'b',label='DJF')
    plt.plot([-90,90],[0,0],'k',linestyle='--')
    plt.ylabel('gpm',fontsize=14)
    plt.title('a) Z-Z_m at 100 mb',fontsize=14)
    plt.legend(loc="upper right")
    plt.xlim(-90,90)
    p2=plt.subplot(3,1,2)
    k0=np.where(resu_am['pres']==500);kk0=int(k0[0])
    plt.plot(resu_am['lat'],hgeo_am[kk0,:],'k',label='Annual Mean')
    plt.plot(resu_am['lat'],hgeo_jja[kk0,:],'r',label='JJA')
    plt.plot(resu_am['lat'],hgeo_djf[kk0,:],'b',label='DJF')
    plt.plot([-90,90],[0,0],'k',linestyle='--')
    plt.ylabel('gpm',fontsize=14)
    plt.title('b) Z-Z_m at 500 mb',fontsize=14)
    plt.xlim(-90,90)
    p3=plt.subplot(3,1,3)
    k0=np.where(resu_am['pres']==1000);kk0=int(k0[0])
    plt.plot(resu_am['lat'],hgeo_am[kk0,:],'k',label='Annual Mean')
    plt.plot(resu_am['lat'],hgeo_jja[kk0,:],'r',label='JJA')
    plt.plot(resu_am['lat'],hgeo_djf[kk0,:],'b',label='DJF')
    plt.plot([-90,90],[0,0],'k',linestyle='--')
    plt.ylabel('gpm',fontsize=14)
    plt.title('c) Z-Z_m at 1000 mb',fontsize=14)
    plt.xlim(-90,90)
    plt.show(block=False)
    #plt.savefig('geopotential_height_zonal_mean_100_500_1000mb_season.png',dpi=100)

    #os.system("mv *.png figures/.")

#=============================================================

def poleward_energy_transport(netflxdn,lon,lat):

    import numpy as np
    from mod2 import area_planet, planet_average
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

def compute_eddy_momentum_fluxes(years,data_dir):

    import os
    import numpy as np
    from matplotlib import pyplot as plt
    from mod2 import read_data
    import netCDF4

    resu_u=read_data(years,'U',data_dir);
    resu_v=read_data(years,'V',data_dir);

    pres=resu_u['pres']
    lat=resu_u['lat']
    lon=resu_u['lon']
    
    vn=resu_v['V']
    tn=resu_u['U']
    [ndays,npres,nlat,nlon]=np.shape(tn)
    
    # time mean --> annual mean
    v_ann=np.mean(vn,axis=0)
    t_ann=np.mean(tn,axis=0)

    # total transport
    vt_total_3D=np.mean(vn*tn,axis=0)
    vt_total=np.mean(vt_total_3D,axis=2)

    # transport by the mean meridional circulation
    vx_ann=np.mean(v_ann,axis=2)
    tx_ann=np.mean(t_ann,axis=2)
    vt_mean=vx_ann*tx_ann
    
    # transport by transients
    vt_tra=np.zeros((npres,nlat))
    vdma=np.zeros((ndays,npres,nlat,nlon));tdma=np.zeros((ndays,npres,nlat,nlon))
    vdma=vn-np.tile(v_ann,(ndays,1,1,1))
    tdma=tn-np.tile(t_ann,(ndays,1,1,1))
    vt_tra_3D=np.mean(vdma*tdma,axis=0)
    vt_tra=np.mean(vt_tra_3D,axis=2)
    
    # transport by the stationary circulation
    vt_sta=np.zeros((npres,nlat))
    vx=np.mean(vn,axis=3);tx=np.mean(tn,axis=3);
    vxa=np.zeros((ndays,npres,nlat,nlon));txa=np.zeros((ndays,npres,nlat,nlon));
    vxa=vn-np.transpose(np.tile(vx,(nlon,1,1,1)),(1,2,3,0))
    txa=tn-np.transpose(np.tile(tx,(nlon,1,1,1)),(1,2,3,0))
    vt_sta_3D=np.mean(vxa,axis=0)*np.mean(txa,axis=0)
    vt_sta=np.mean(vt_sta_3D,axis=2)

    ncfile = netCDF4.Dataset('EddyMomentumFluxes.nc',mode='w',format='NETCDF4_CLASSIC') 
    ncfile.createDimension('longitude', nlon) # latitude axis
    ncfile.createDimension('latitude', nlat) # latitude axis
    ncfile.createDimension('pressure', npres) # pressure axis
    ncfile.title='Eddy Momentum Fluxes'
    longitude = ncfile.createVariable('lon', 'f4', 'longitude')
    longitude.units = 'degrees_east'
    longitude.long_name = 'longitude (E)'
    latitude = ncfile.createVariable('lat', 'f4', 'latitude')
    latitude.units = 'degrees_north'
    latitude.long_name = 'latitude (N)'
    levels = ncfile.createVariable('pres', 'f4', 'pressure')
    levels.units = 'hPa'
    levels.long_name = 'pressure (hPa)'
    uv_tot=ncfile.createVariable('UV_TOT', 'f4', ('pressure','latitude','longitude') )
    uv_tot.units = 'm2/s2'
    uv_tot.long_name = 'Total meridional eddy momentum flux'
    uv_mean=ncfile.createVariable('UV_MEAN', 'f4', ('pressure','latitude') )
    uv_mean.units = 'm2/s2'
    uv_mean.long_name = 'Eulerian mean meridional eddy momentum flux'
    uv_tra=ncfile.createVariable('UV_TRA', 'f4', ('pressure','latitude','longitude') )
    uv_tra.units = 'm2/s2'
    uv_tra.long_name = 'Transient eddy meridional eddy momentum flux'
    uv_sta=ncfile.createVariable('UV_STA', 'f4', ('pressure','latitude','longitude') )
    uv_sta.units = 'm2/s2'
    uv_sta.long_name = 'Stationary eddy meridional eddy momentum flux'
    longitude[:]=lon
    latitude[:]=lat
    levels[:]=pres
    uv_tot[:,:,:]=vt_total_3D
    uv_mean[:,:]=vt_mean
    uv_tra[:,:,:]=vt_tra_3D
    uv_sta[:,:,:]=vt_sta_3D
    ncfile.close()

#=============================================================

def momentum_transport(years,data_dir):

    # momentum transport by mean circulation, transient and stationary eddies
    # momentum transport streamfunction
    # eddy momentum fluxes divergence and surface (zonal) wind stress

    import os
    import numpy as np
    from matplotlib import pyplot as plt
    from mod2 import read_data
    import netCDF4

    resu_u=read_data(years,'U',data_dir);
    resu_v=read_data(years,'V',data_dir);

    pres=resu_u['pres']
    lat=resu_u['lat']
    lon=resu_u['lon']
    
    vn=resu_v['V']
    tn=resu_u['U']
    [ndays,npres,nlat,nlon]=np.shape(tn)
    
    # time mean --> annual mean
    v_ann=np.mean(vn,axis=0)
    t_ann=np.mean(tn,axis=0)

    # total transport
    vt_total_3D=np.mean(vn*tn,axis=0)
    vt_total=np.mean(vt_total_3D,axis=2)

    # transport by the mean meridional circulation
    vx_ann=np.mean(v_ann,axis=2)
    tx_ann=np.mean(t_ann,axis=2)
    vt_mean=vx_ann*tx_ann
    
    # transport by transients
    vt_tra=np.zeros((npres,nlat))
    vdma=np.zeros((ndays,npres,nlat,nlon));tdma=np.zeros((ndays,npres,nlat,nlon))
    vdma=vn-np.tile(v_ann,(ndays,1,1,1))
    tdma=tn-np.tile(t_ann,(ndays,1,1,1))
    vt_tra_3D=np.mean(vdma*tdma,axis=0)
    vt_tra=np.mean(vt_tra_3D,axis=2)
    
    # transport by the stationary circulation
    vt_sta=np.zeros((npres,nlat))
    vx=np.mean(vn,axis=3);tx=np.mean(tn,axis=3);
    vxa=np.zeros((ndays,npres,nlat,nlon));txa=np.zeros((ndays,npres,nlat,nlon));
    vxa=-np.transpose(np.tile(vx,(nlon,1,1,1)),(1,2,3,0))
    txa=tn-np.transpose(np.tile(tx,(nlon,1,1,1)),(1,2,3,0))
    vt_sta_3D=np.mean(vxa,axis=0)*np.mean(txa,axis=0)
    vt_sta=np.mean(vt_sta_3D,axis=2)

    npres=np.size(pres)
    # pressure thicknesses
    pres_mid=np.zeros(npres-1)
    ps=1015.0 # psi=0 at the ground
    for k in range(npres-1):
        pres_mid[k]=0.5*(pres[k]+pres[k+1])

    dp=np.zeros(npres)
    dp[0]=pres_mid[0]-ps
    for k in range(1,npres-1,1):
        dp[k]=pres_mid[k]-pres_mid[k-1]

    pepsi=np.zeros(npres+1)
    pepsi[0]=ps
    for k in range(1,npres,1):
        pepsi[k]=pepsi[k-1]+dp[k-1]

    pepsi[-1]=pres[-1]
    dp[-1]=pepsi[-1]-pepsi[-2]
    dp=dp*100.0 # to get unit in Pascal !
    dp=-dp

    psi_total=np.zeros((npres+1,nlat))
    psi_mean=np.zeros((npres+1,nlat))
    psi_tra=np.zeros((npres+1,nlat))
    psi_sta=np.zeros((npres+1,nlat))
    g0=9.80665
    phi=lat*np.pi/180.0
    rt=6.37e+06
    for j in range(nlat):
        r=2*np.pi*rt**2*np.cos(phi[j])**2/g0
        for k in range(npres,0,-1):
            psi_total[k-1,j]=psi_total[k,j]+r*vt_total[k-1,j]*dp[k-1]
            psi_mean[k-1,j]=psi_mean[k,j]+r*vt_mean[k-1,j]*dp[k-1]
            psi_tra[k-1,j]=psi_tra[k,j]+r*vt_tra[k-1,j]*dp[k-1]
            psi_sta[k-1,j]=psi_sta[k,j]+r*vt_sta[k-1,j]*dp[k-1]

    scfac=1.e-18 # scale factor
    mabs1=np.amax(np.max(np.abs(psi_total)))*scfac
    mabs2=np.max(np.max(np.abs(psi_mean)))*scfac
    mabs3=np.max(np.max(np.abs(psi_tra)))*scfac
    mabs4=np.max(np.max(np.abs(psi_sta)))*scfac
    mabs=np.amax([mabs1,mabs2,mabs3,mabs4])

    add_contour=False

    plt.figure(figsize=(8,8))

    p1=plt.subplot(2,2,1)
    scale=np.linspace(-mabs,mabs,51)
    c=plt.contourf(lat,pepsi,scfac*psi_total,scale,cmap=plt.cm.seismic)
    if (add_contour):
        plt.rcParams['contour.negative_linestyle'] = 'dashed'
        plt.contour(lat,pepsi,scfac*psi_total,21,colors='k')
    plt.ylabel('pressure (mb)',fontsize=14)
    plt.gca().invert_yaxis()
    plt.title("a) Total",fontsize=14)
    plt.colorbar(c,orientation='vertical')

    p2=plt.subplot(2,2,2)
    scale=np.linspace(-mabs,mabs,51)
    c=plt.contourf(lat,pepsi,scfac*psi_mean,scale,cmap=plt.cm.seismic)
    if (add_contour):
        plt.rcParams['contour.negative_linestyle'] = 'dashed'
        plt.contour(lat,pepsi,scfac*psi_mean,21,colors='k')
    plt.gca().invert_yaxis()
    plt.title("b) Mean",fontsize=14)
    plt.colorbar(c,orientation='vertical')

    p3=plt.subplot(2,2,3)
    scale=np.linspace(-mabs,mabs,51)
    c=plt.contourf(lat,pepsi,scfac*psi_tra,scale,cmap=plt.cm.seismic)
    if (add_contour):
        plt.rcParams['contour.negative_linestyle'] = 'dashed'
        plt.contour(lat,pepsi,scfac*psi_tra,21,colors='k')
    plt.xlabel('Latitude',fontsize=14)
    plt.ylabel('pressure (mb)',fontsize=14)
    plt.gca().invert_yaxis()
    plt.title("c) Transient",fontsize=14)
    plt.colorbar(c,orientation='vertical')

    p4=plt.subplot(2,2,4)
    scale=np.linspace(-mabs,mabs,51)
    c=plt.contourf(lat,pepsi,scfac*psi_sta,scale,cmap=plt.cm.seismic)
    if (add_contour):
        plt.rcParams['contour.negative_linestyle'] = 'dashed'
        plt.contour(lat,pepsi,scfac*psi_sta,21,colors='k')
    plt.xlabel('Latitude',fontsize=14)
    plt.gca().invert_yaxis()
    plt.title("d) Stationary",fontsize=14)
    plt.colorbar(c,orientation='vertical')
    plt.suptitle('Angular Momentum Streamfunction (10$^{18}$ kg m$^2$ s$^{-2}$)',fontsize=16)
    plt.show(block=False)
    #plt.savefig('angular_momentum_streamfunction.png',dpi=100)
    #os.system("mv *.png figures/.")

    # eddy momentum fluxes [pres,lat]
    # uv cos(phi)**2
    # show the approximate balance between vertical sum of these
    # eddy fluxes and surface zonal wind stress (M2 level)
    # surface westerlies at midlatiudes are maintained by transient
    # eddy momentum flux convergence against surface friction
    # (negative viscosity phenomena...)

    eddy_fluxes=np.zeros((npres,nlat))
    for j in range(nlat):
        eddy_fluxes[:,j]=vt_tra[:,j]*np.cos(phi[j])**2

    # vertical sum
    efz_tra=np.zeros(nlat);
    for j in range(nlat):
        for k in range(npres-1):
            efz_tra[j]=efz_tra[j]+0.5*(eddy_fluxes[k,j]+eddy_fluxes[k+1,j])*(pres[k]-pres[k+1])
        efz_tra[j]=efz_tra[j]*100.0*2*np.pi*rt/g0

    # divergence
    div_eddy_fluxes=np.zeros(nlat-1)
    dlat=rt*2.5*np.pi/180.0
    lat_mid=0.5*(lat[:-1]+lat[1:])
    for j in range(nlat-1):
        d=dlat*2*np.pi*rt*np.cos(lat_mid[j]*np.pi/180.0)**2
        div_eddy_fluxes[j]=(efz_tra[j]-efz_tra[j+1])/d

    # figures : eddy fluxes structure and vertically integrated momentum balnace
    plt.figure(figsize=(8,5))
    add_contour=True
    mabs=np.amax([np.abs(np.amin(eddy_fluxes)),np.amax(eddy_fluxes)])
    scale=np.linspace(-mabs,mabs,51)
    c=plt.contourf(lat,pres,eddy_fluxes,scale,cmap=plt.cm.seismic)
    if (add_contour):
        plt.rcParams['contour.negative_linestyle'] = 'dashed'
        plt.contour(lat,pres,eddy_fluxes,21,colors='k')
    plt.xlabel('Latitude',fontsize=14)
    plt.ylabel('pressure (mb)',fontsize=14)
    plt.gca().invert_yaxis()
    plt.title("Transient Eddy Momentum Fluxes $uv\cos^2\phi$ (m$^2$s$^{-2}$)",fontsize=14)
    plt.colorbar(c,orientation='vertical')
    plt.show(block=False)
    #plt.savefig('eddy_momentum_fluxes.png',dpi=100)
    #os.system("mv *.png figures/.")

    # to do : check units carefully...
    # add obserbed surface zonal wind stress...
    plt.figure(figsize=(8,4))
    plt.plot(lat_mid,-div_eddy_fluxes,'k')
    plt.title("Transient Eddy Momentum Fluxes Convergence",fontsize=14)
    plt.xlabel('Latitude',fontsize=14)
    plt.ylabel('Pa',fontsize=14)
    plt.show(block=False)
    #plt.savefig('eddy_momentum_fluxes_convergence.png',dpi=100)
    #os.system("mv *.png figures/.")

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
