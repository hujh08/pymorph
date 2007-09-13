"""Configure file for automation"""
imagefile = 'j8f647-1-1_drz_sci.fits'
whtfile = 'j8f647-1-1_drz_rms.fits'   #The weight image. 
sex_cata = 'goods_sex.cat'           #The sextractor catalogue which has 
                                      #the format given in the file
clus_cata = 'abhi_goods_first.cat'         #catalogue of galaxies from
                                      #online catalogu service
                                      #(name ra1 ra2 ra2 dec1 dec2 dec3)
out_cata = 'cl1216-1201_out.cat'      #catalogue of galaxies in the field
rootname = ''
psflist = ('psf_1216424-1202057.fits', 'psf_1216434-1200395.fits', 'psf_1216434-1200395.fits')        #List of psf containg their 
                                      #position information in the 
                                      #header (RA_TARG, DEC_TARG). 
                                      #Make psf with the names as here 
                                      #and use psf_header_update.py. 
                                      #It will update the header information.
mag_zero = 25.256                     #magnitude zero point
mask_reg = 2.5
thresh_area = 400.0
threshold = 2.0                       #Masking will start for neighbours 
                                      #whose distace from the object greater 
                                      #than threshold * semi-major axis of 
                                      #the object and area of the neighbour 
                                      #less than thresh_area sq.pixel. 
                                      #The masking will be for a circular 
                                      #region of radius mask_reg*semi-major 
                                      #axis of the nighbour with respect to 
                                      #the center of the neightbour.
size = 120                            #size of the stamp image
shiftra = 0.0 
shiftdec =  0.0                       #If the image WCS is not same as the 
                                      #coordinate given in the clus_cata, 
                                      #the appropriateshiftra and shiftdec  
                                      #should be used. It will be better to 
                                      #correct WCS using iraf command ccmap 
                                      #so that the programcan identify the 
                                      #correct objects. Remember: Shift 
                                      #in the frame in not LINEAR! and it 
                                      #can leads to detect wrong objects
pixelscale = 0.045                    #Pixel scale (arcsec/pixel)
galcut = True                        #True if we provide cutouts
H0 = 71                               #Hubble parameter
WM = 0.27                             #Omega matter
WV = 0.73                             #Omega Lambda
repeat = False                        #Repeat the pipeline manually
back_extraction_radius = 15.0
#back_ini_xcntr = 32.0 
#back_ini_ycntr = 22.0
angle = 180.0
decompose = False
galfit = False
cas = True
