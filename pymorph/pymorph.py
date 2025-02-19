
"""PyMorph [Py MOrphological Parameters' Hunter], is a pipeline to find the Morphological parameters of galaxy. Authors: Vinu Vikram , Yogesh Wadadekar, Ajit K. Kembhavi. 2008 Feb, Alan Meert 2010"""

import os
import sys
import time
import csv
import traceback
import argparse
import fitsio
import numpy as np
import re
import configparser
import subprocess
from multiprocessing import Pool

import pymorphutils as ut
from flagfunc import GetFlag, isset, SetFlag

from ellimaskfunc_easy import ElliMaskFunc

from maskfunc_easy import MaskFunc

from configfunc import GalfitConfigFunc
#from configtwostep import ConfigIter
from yetbackfunc import FindYetSky
#from plotfunc import PlotFunc
from runsexfunc import PySex
#from writehtmlfunc import WriteParams
import psffunc as pf  
import mask_or_fit as mf
from pipeline import Pipeline
       
        


def run_test(option, opt, value, parser):
    print("Using directory {} for output\n".format(value))
    center_deviated = 0
    starthandle = 0
    find_and_fit()
    main()
    if crashhandler:
        starthandle = 1
        os.system('mv restart.cat CRASH.CAT')
        obj_cata = 'CRASH.CAT' 
        main()
    
    sys.exit(0)
    return


def SExtractorConfEdit():
    SEx_DETECT_MINAREA = input("DETECT_MINAREA (6) >>> ")
    try:
        SEx_DETECT_MINAREA = float(SEx_DETECT_MINAREA)
        SEx_DETECT_MINAREA = int(SEx_DETECT_MINAREA)
    except:
        SEx_DETECT_MINAREA = 6
    SEx_DETECT_THRESH = input('DETECT_THRESH (1.5) >>> ')
    try:
        SEx_DETECT_THRESH = float(SEx_DETECT_THRESH)
    except:
        SEx_DETECT_THRESH = 1.5
    SEx_ANALYSIS_THRESH = input('ANALYSIS_THRESH (1.5) >>> ')
    try:
        SEx_ANALYSIS_THRESH = float(SEx_ANALYSIS_THRESH)
    except:
        SEx_ANALYSIS_THRESH = 1.5
    SEx_FILTER = input('FILTER (Y/N) >>> ')
    while SEx_FILTER != 'Y' and SEx_FILTER != 'N' and SEx_FILTER != '':
        SEx_FILTER = input('FILTER (Y/N) >>> ')
    if len(SEx_FILTER) == 0:
        SEx_FILTER = 'Y'
    else:
        SEx_FILTER = SEx_FILTER
    print('Available options for convolve filter are gauss_1.5_3x3.conv(1) '\
          'gauss_2.0_3x3.conv(2) gauss_2.0_5x5.conv(3) gauss_2.5_5x5.conv(4) '\
          'gauss_3.0_5x5.conv(5) gauss_3.0_7x7.conv(6) gauss_4.0_7x7.conv(7) '\
          'gauss_5.0_9x9.conv(8) default(0)')
    SEx_FILTER_NAME  = input('FILTER_NAME (default.conv) >>> ')
    if len(SEx_FILTER_NAME) == 0 or SEx_FILTER_NAME == '0':
        SEx_FILTER_NAME = 'default.conv'
    elif SEx_FILTER_NAME == '1':
        SEx_FILTER_NAME = 'gauss_1.5_3x3.conv'
    elif SEx_FILTER_NAME == '2':
        SEx_FILTER_NAME = 'gauss_2.0_3x3.conv'
    elif SEx_FILTER_NAME == '3':
        SEx_FILTER_NAME = 'gauss_2.0_5x5.conv'
    elif SEx_FILTER_NAME == '4':
        SEx_FILTER_NAME = 'gauss_2.5_5x5.conv'
    elif SEx_FILTER_NAME == '5':
        SEx_FILTER_NAME = 'gauss_3.0_5x5.conv'
    elif SEx_FILTER_NAME == '6':
        SEx_FILTER_NAME = 'gauss_3.0_7x7.conv'
    elif SEx_FILTER_NAME == '7':
        SEx_FILTER_NAME = 'gauss_4.0_7x7.conv'
    elif SEx_FILTER_NAME == '8':
        SEx_FILTER_NAME = 'gauss_5.0_9x9.conv'
    SEx_DEBLEND_NTHRESH = input('DEBLEND_NTHRESH (32) >>> ')
    try:
        SEx_DEBLEND_NTHRESH = float(SEx_DEBLEND_NTHRESH)
        SEx_DEBLEND_NTHRESH = int(SEx_DEBLEND_NTHRESH)
    except:
        SEx_DEBLEND_NTHRESH = 32
    SEx_DEBLEND_MINCONT = input('DEBLEND_MINCONT (0.005) >>> ')
    try:
        SEx_DEBLEND_MINCONT = float(SEx_DEBLEND_MINCONT)
    except:
        SEx_DEBLEND_MINCONT = 0.005
    SEx_PHOT_FLUXFRAC = input('PHOT_FLUXFRAC (0.5) >>> ')
    try:
        SEx_PHOT_FLUXFRAC = float(SEx_PHOT_FLUXFRAC)
    except:
        SEx_PHOT_FLUXFRAC = 0.5
    SEx_pix_scale_disp = 'PIXEL_SCALE (' + str(SEx_PIXEL_SCALE) + ') >>> '
    SEx_PIXEL_SCALE = input(SEx_pix_scale_disp)
    try:
        SEx_PIXEL_SCALE = float(SEx_PIXEL_SCALE)
    except:
        SEx_PIXEL_SCALE = pixelscale
    SEx_SEEING_FWHM = input('SEEING_FWHM (0.11) >>> ')
    try:
        SEx_SEEING_FWHM = float(SEx_SEEING_FWHM )
    except:
        SEx_SEEING_FWHM = pixelscale * 3.37
    SEx_BACK_SIZE = input('BACK_SIZE (64) >>> ')
    try:
        SEx_BACK_SIZE = float(SEx_BACK_SIZE)
        SEx_BACK_SIZE = int(SEx_BACK_SIZE)
    except:
        SEx_BACK_SIZE = 64
    SEx_BACK_FILTERSIZE = input('BACK_FILTERSIZE (3) >>> ')
    try:
        SEx_BACK_FILTERSIZE = float(SEx_BACK_FILTERSIZE)
        SEx_BACK_FILTERSIZE = int(SEx_BACK_FILTERSIZE)
    except:
        SEx_BACK_FILTERSIZE = 3
    SEx_BACKPHOTO_TYPE = input('BACKPHOTO_TYPE (G)LOBAL/(L)OCAL) >>> ')
    while SEx_BACKPHOTO_TYPE != 'G' and SEx_BACKPHOTO_TYPE != 'L' \
          and SEx_BACKPHOTO_TYPE != '':
        SEx_BACKPHOTO_TYPE = input('BACKPHOTO_TYPE (G)LOBAL/(L)OCAL) >>> ')
    if len(SEx_BACKPHOTO_TYPE) == 0:
        SEx_BACKPHOTO_TYPE = 'GLOBAL'
    elif SEx_BACKPHOTO_TYPE == 'G':
        SEx_BACKPHOTO_TYPE = 'GLOBAL'
    elif SEx_BACKPHOTO_TYPE == 'L':
        SEx_BACKPHOTO_TYPE = 'LOCAL'
    if SEx_BACKPHOTO_TYPE == 'LOCAL':
        SEx_BACKPHOTO_THICK = input('BACKPHOTO_THICK (24) >>> ')
    try:
        SEx_BACKPHOTO_THICK = float(SEx_BACKPHOTO_THICK)
        SEx_BACKPHOTO_THICK = int(SEx_BACKPHOTO_THICK)
    except:
        SEx_BACKPHOTO_THICK = 24
    SEx_WEIGHT_TYPE = input('WEIGHT_TYPE (MAP_RMS) >>> ')
    SEx_WEIGHT_TYPE = SEx_WEIGHT_TYPE

    return [SEx_DETECT_MINAREA, SEx_DETECT_THRESH, SEx_ANALYSIS_THRESH, SEx_FILTER, SEx_FILTER_NAME, SEx_DEBLEND_NTHRESH, SEx_DEBLEND_MINCONT, SEx_PHOT_FLUXFRAC, SEx_BACK_SIZE, SEx_BACK_FILTERSIZE, SEx_BACKPHOTO_TYPE, SEx_BACKPHOTO_THICK, SEx_WEIGHT_TYPE, SEx_PIXEL_SCALE, SEx_SEEING_FWHM]



def SExtractorConfDefault():
    SEx_DETECT_MINAREA = 6
    SEx_DETECT_THRESH = 1.5
    SEx_ANALYSIS_THRESH = 1.5
    SEx_FILTER = 'Y'
    SEx_FILTER_NAME = 'default.conv'
    SEx_DEBLEND_NTHRESH = 32
    SEx_DEBLEND_MINCONT = 0.005
    SEx_PHOT_FLUXFRAC = 0.5
    SEx_BACK_SIZE = 64
    SEx_BACK_FILTERSIZE = 3
    SEx_BACKPHOTO_TYPE = 'GLOBAL'
    SEx_BACKPHOTO_THICK = 24
    SEx_WEIGHT_TYPE = 'MAP_RMS'

    return [SEx_DETECT_MINAREA, SEx_DETECT_THRESH, SEx_ANALYSIS_THRESH, SEx_FILTER, SEx_FILTER_NAME, SEx_DEBLEND_NTHRESH, SEx_DEBLEND_MINCONT, SEx_PHOT_FLUXFRAC, SEx_BACK_SIZE, SEx_BACK_FILTERSIZE, SEx_BACKPHOTO_TYPE, SEx_BACKPHOTO_THICK, SEx_WEIGHT_TYPE]



def run_SExtractorConf():
    try:
        SExtractorConf()
    except:
        raise OptionValueError("failure in SextractorConf()")
    return


def rm_sex_cata(sex_cata):
    if os.path.exists(sex_cata):
        os.remove(sex_cata)
    else:
        pass
    return





class InitializeParams(object):

    def _initilize_params(self, config_file='config.ini'):

        c = configparser.ConfigParser()
        c.read(config_file)
        

        self.DATADIR = c.get('imagecata', 'datadir')
        self.OUTDIR = c.get('imagecata', 'outdir')

        self.imagefile = c.get('imagecata', 'imagefile')
        self.imagefile = os.path.join(self.DATADIR, self.imagefile)

        self.whtfile = c.get('imagecata', 'whtfile')
        self.whtfile = os.path.join(self.DATADIR, self.whtfile)

        self.sex_cata = c.get('imagecata', 'sex_cata')
        self.sex_cata = os.path.join(self.DATADIR, self.sex_cata)

        self.obj_cata = c.get('imagecata', 'obj_cata')
        self.obj_cata = os.path.join(self.DATADIR, self.obj_cata)

        self.out_cata = c.get('imagecata', 'out_cata')
        self.out_cata = os.path.join(self.OUTDIR, self.out_cata)


        self.rootname = c.get('imagecata', 'rootname')

        self.GALFIT_PATH = c.get('external', 'GALFIT_PATH')
        self.SEX_PATH = c.get('external', 'SEX_PATH')

        self.findandfit = c.getboolean('modes', 'findandfit')
        self.repeat = c.getboolean('modes', 'repeat')
        self.galcut = c.getboolean('modes', 'galcut')
        self.decompose = c.getboolean('modes', 'decompose')
        self.detail = c.getboolean('modes', 'detail')
        self.galfit = c.getboolean('modes', 'galfit')
        self.cas = c.getboolean('modes', 'cas')
        self.crashhandler = c.getboolean('modes', 'crashhandler')


        try:
            components = c.get('galfit', 'components').split(',')
            self.components = [cm.strip() for cm in components]
        except:
            print("components undefined. Asuming bulge+disk model")
            self.components = ['bulge', 'disk']

        self.devauc = c.get('galfit', 'devauc')
        self.fitting = c.get('galfit', 'fitting')
        self.fitting = [int(tf) for tf in self.fitting.split(',')]

        self.chi2sq = c.getfloat('diagnosis', 'chi2sq')
        self.goodness = c.getfloat('diagnosis', 'goodness')
        self.center_deviation = c.getfloat('diagnosis', 'center_deviation')
        self.center_constrain = c.getfloat('diagnosis', 'center_constrain')


        try:
            size = c.get('size', 'size_list')
            size = [int(s) for s in size.split(',')]
            self.ReSize = size[0]
            self.VarSize = size[1]
            self.FracRad = size[2]
            self.Square = size[3]
            self.FixSize = size[4]
        except:
            self.ReSize = c.getint('size', 'size_list')

            if self.ReSize:
                self.VarSize = 1
            else:
                self.VarSize = 0
            self.Square = 1
            self.FracRad = 20
            self.FixSize = 120
        try:
            self.searchrad = c.get('size', 'searchrad')
        except:
            self.searchrad = None


        self.pixelscale = c.getfloat('cosmology', 'pixelscale')
        self.H0 = c.getfloat('cosmology', 'H0')
        self.WM = c.getfloat('cosmology', 'WM')
        self.WV = c.getfloat('cosmology', 'WV')
        self.redshift = c.getfloat('cosmology', 'redshift')

        self.psfselect = c.getint('psf', 'psfselect')
        self.stargal_prob = c.getfloat('psf', 'stargal_prob')
        self.star_size = c.getint('psf', 'star_size')
        self.psflist = c.get('psf', 'psflist')
        self.which_psf = c.getint('psf', 'which_psf')
        self.area_obj = c.getint('psf', 'which_psf')

        self.manual_mask = c.getint('mask', 'manual_mask')
        self.mask_reg = c.getfloat('mask', 'mask_reg')
        self.thresh_area = c.getfloat('mask', 'thresh_area')
        self.threshold = c.getfloat('mask', 'threshold')
        self.avoidme = c.getfloat('mask', 'avoidme')
        self.mag_zero = c.getfloat('mag', 'mag_zero')
        self.maglim = c.get('mag', 'maglim').split(',')
        self.maglim = [float(mlim) for mlim in self.maglim]


        self.host = c.get('db', 'host')
        self.database = c.get('db', 'database')
        self.table = c.get('db', 'table')
        self.user = c.get('db', 'user')
        self.password = c.get('db', 'password')
        self.dbparams = c.get('db', 'dbparams')

        self.galfitv = c.get('version', 'galfitv')
        self.FirstCreateDB = 1 #Won't create table when FirstCreateDB=0
        self.FILTER = 'UNKNOWN'


        self.bdbox = c.get('params_limit', 'bdbox')
        self.bbox = c.get('params_limit', 'bbox')
        self.dbox = c.get('params_limit', 'dbox')
        self.no_mask = c.get('mask', 'no_mask')
        self.norm_mask = c.get('mask', 'norm_mask')

        #Sextractor configuration
        self.SEx_PIXEL_SCALE = self.pixelscale
        self.SEx_SEEING_FWHM = self.pixelscale * 3.37
        self.SEx_MAG_ZEROPOINT = self.mag_zero
        self.SEx_DETECT_MINAREA = 6
        self.SEx_DETECT_THRESH = 1.5
        self.SEx_ANALYSIS_THRESH =1.5
        self.SEx_FILTER = 'Y'
        self.SEx_FILTER_NAME = 'default.conv'
        self.SEx_DEBLEND_NTHRESH = 32
        self.SEx_DEBLEND_MINCONT = 0.005
        self.SEx_PHOT_FLUXFRAC = 0.5
        self.SEx_BACK_SIZE = 64
        self.SEx_BACK_FILTERSIZE = 3
        self.SEx_BACKPHOTO_TYPE = 'GLOBAL'
        self.SEx_BACKPHOTO_THICK = 24
        self.SEx_WEIGHT_TYPE = 'MAP_RMS'


        #Limit of parameters
        self.LMag  = 50.
        self.UMag  = -50.
        self.LN    = 0.1
        self.UN    = 15.
        self.LRe   = 0.
        self.URe   = 200.
        self.LRd   = 0.
        self.URd   = 200.


        self.pymorph_config = self.get_pymorph_config_dict()
        self.sex_config = self.get_sex_config_dict()
        self.limit_config = self.get_limit_config_dict()



    def get_pymorph_config_dict(self):

        pymorph_config = dict()

        pymorph_config['DATADIR'] = self.DATADIR
        pymorph_config['OUTDIR'] = self.OUTDIR
        pymorph_config['imagefile'] = self.imagefile
        pymorph_config['whtfile'] = self.whtfile
        pymorph_config['sex_cata'] = self.sex_cata
        pymorph_config['obj_cata'] = self.obj_cata
        pymorph_config['out_cata'] = self.out_cata
        pymorph_config['rootname'] = self.rootname
        pymorph_config['GALFIT_PATH'] = self.GALFIT_PATH
        pymorph_config['SEX_PATH'] = self.SEX_PATH
        pymorph_config['findandfit'] = self.findandfit
        pymorph_config['repeat'] = self.repeat
        pymorph_config['galcut'] = self.galcut
        pymorph_config['decompose'] = self.decompose
        pymorph_config['detail'] = self.detail
        pymorph_config['galfit'] = self.galfit
        pymorph_config['cas'] = self.cas
        pymorph_config['crashhandler'] = self.crashhandler
        pymorph_config['devauc'] = self.devauc
        pymorph_config['fitting'] = self.fitting
        pymorph_config['fitting'] = self.fitting
        pymorph_config['chi2sq'] = self.chi2sq
        pymorph_config['goodness'] = self.goodness
        pymorph_config['center_deviation'] = self.center_deviation
        pymorph_config['center_constrain'] = self.center_constrain
        pymorph_config['pixelscale'] = self.pixelscale
        pymorph_config['H0'] = self.H0
        pymorph_config['WM'] = self.WM
        pymorph_config['WV'] = self.WV
        pymorph_config['redshift'] = self.redshift
        pymorph_config['psfselect'] = self.psfselect
        pymorph_config['stargal_prob'] = self.stargal_prob
        pymorph_config['star_size'] = self.star_size
        pymorph_config['psflist'] = self.psflist
        pymorph_config['which_psf'] = self.which_psf
        pymorph_config['area_obj'] = self.area_obj
        pymorph_config['manual_mask'] = self.manual_mask
        pymorph_config['mask_reg'] = self.mask_reg
        pymorph_config['thresh_area'] = self.thresh_area
        pymorph_config['threshold'] = self.threshold
        pymorph_config['mag_zero'] = self.mag_zero
        pymorph_config['maglim'] = self.maglim
        pymorph_config['maglim'] = self.maglim
        pymorph_config['host'] = self.host
        pymorph_config['database'] = self.database
        pymorph_config['table'] = self.table
        pymorph_config['user'] = self.user
        pymorph_config['password'] = self.password
        pymorph_config['dbparams'] = self.dbparams
        pymorph_config['galfitv'] = self.galfitv
        pymorph_config['FirstCreateDB'] = self.FirstCreateDB
        pymorph_config['bdbox'] = self.bdbox
        pymorph_config['bbox'] = self.bbox
        pymorph_config['dbox'] = self.dbox
        pymorph_config['FILTER'] = self.FILTER
        pymorph_config['no_mask'] = self.no_mask
        pymorph_config['norm_mask'] = self.norm_mask
        pymorph_config['components'] = self.components
        pymorph_config['ReSize'] = self.ReSize
        pymorph_config['VarSize'] = self.VarSize
        pymorph_config['FracRad'] = self.FracRad
        pymorph_config['Square'] = self.Square
        pymorph_config['FixSize'] = self.FixSize
        pymorph_config['searchrad'] = self.searchrad

        return pymorph_config


    def get_sex_config_dict(self):

        sex_config = dict()

        sex_config['SEx_PIXEL_SCALE'] = self.pixelscale
        sex_config['SEx_SEEING_FWHM'] = self.pixelscale * 3.37
        sex_config['SEx_MAG_ZEROPOINT'] = self.mag_zero
        sex_config['SEx_DETECT_MINAREA'] = self.SEx_DETECT_MINAREA
        sex_config['SEx_DETECT_THRESH'] = self.SEx_DETECT_THRESH
        sex_config['SEx_ANALYSIS_THRESH'] = self.SEx_ANALYSIS_THRESH
        sex_config['SEx_FILTER'] = self.SEx_FILTER
        sex_config['SEx_FILTER_NAME'] = self.SEx_FILTER_NAME
        sex_config['SEx_DEBLEND_NTHRESH'] = self.SEx_DEBLEND_NTHRESH
        sex_config['SEx_DEBLEND_MINCONT'] = self.SEx_DEBLEND_MINCONT
        sex_config['SEx_PHOT_FLUXFRAC'] = self.SEx_PHOT_FLUXFRAC
        sex_config['SEx_BACK_SIZE'] = self.SEx_BACK_SIZE
        sex_config['SEx_BACK_FILTERSIZE'] = self.SEx_BACK_FILTERSIZE
        sex_config['SEx_BACKPHOTO_TYPE'] = self.SEx_BACKPHOTO_TYPE
        sex_config['SEx_BACKPHOTO_THICK'] = self.SEx_BACKPHOTO_THICK
        sex_config['SEx_WEIGHT_TYPE'] = self.SEx_WEIGHT_TYPE

        return sex_config


    def get_limit_config_dict(self):

        limit_config = dict()

        limit_config['LMag'] = self.LMag 
        limit_config['UMag'] = self.UMag
        limit_config['LN'] = self.LN
        limit_config['UN'] = self.UN
        limit_config['LRe'] = self.LRe
        limit_config['URe'] = self.URe 
        limit_config['LRd'] = self.LRd
        limit_config['URd'] = self.URd

        return limit_config


    def set_sexparams(self,
                      SEx_DETECT_MINAREA = 6,
                      SEx_DETECT_THRESH = 1.5,
                      SEx_ANALYSIS_THRESH =1.5,
                      SEx_FILTER = 'Y',
                      SEx_FILTER_NAME = 'default.conv',
                      SEx_DEBLEND_NTHRESH = 32,
                      SEx_DEBLEND_MINCONT = 0.005,
                      SEx_PHOT_FLUXFRAC = 0.5,
                      SEx_BACK_SIZE = 64,
                      SEx_BACK_FILTERSIZE = 3,
                      SEx_BACKPHOTO_TYPE = 'GLOBAL',
                      SEx_BACKPHOTO_THICK = 24,
                      SEx_WEIGHT_TYPE = 'MAP_RMS',
                      ):
        '''

        Setting SExtractor default.sex

        FHWH is 3.37 * SEx_PIXEL_SCALE

        '''


        self.SEx_DETECT_MINAREA =  SEx_DETECT_MINAREA
        self.SEx_DETECT_THRESH =   SEx_DETECT_THRESH
        self.SEx_ANALYSIS_THRESH = SEx_ANALYSIS_THRESH
        self.SEx_FILTER =          SEx_FILTER
        self.SEx_FILTER_NAME =     SEx_FILTER_NAME
        self.SEx_DEBLEND_NTHRESH = SEx_DEBLEND_NTHRESH
        self.SEx_DEBLEND_MINCONT = SEx_DEBLEND_MINCONT
        self.SEx_PHOT_FLUXFRAC =   SEx_PHOT_FLUXFRAC
        self.SEx_BACK_SIZE =       SEx_BACK_SIZE
        self.SEx_BACK_FILTERSIZE = SEx_BACK_FILTERSIZE
        self.SEx_BACKPHOTO_TYPE =  SEx_BACKPHOTO_TYPE
        self.SEx_BACKPHOTO_THICK = SEx_BACKPHOTO_THICK
        self.SEx_WEIGHT_TYPE =     SEx_WEIGHT_TYPE

        self.sex_params = [SEx_DETECT_MINAREA, SEx_DETECT_THRESH,
                           SEx_ANALYSIS_THRESH, SEx_FILTER,
                           SEx_FILTER_NAME, SEx_DEBLEND_NTHRESH,
                           SEx_DEBLEND_MINCONT, SEx_PHOT_FLUXFRAC,
                           SEx_BACK_SIZE, SEx_BACK_FILTERSIZE,
                           SEx_BACKPHOTO_TYPE, SEx_BACKPHOTO_THICK,
                           SEx_WEIGHT_TYPE, self.SEx_PIXEL_SCALE,
                           self.SEx_SEEING_FWHM, self.SEx_MAG_ZEROPOINT]

        self.sex_config = self.get_sex_config_dict()


    def set_limits(self,
                   LMag=500, UMag=-500, LN=0.1, UN=20.,
                   LRe=0., URe=500., LRd=0., URd=500.):
        '''

        Setting pymorph parameters limits

        '''

        self.LMag  = LMag
        self.UMag  = UMag
        self.LN    = LN
        self.UN    = UN
        self.LRe   = LRe
        self.URe   = URe
        self.LRd   = LRd
        self.URd   = URd

        self.limit_config = self.get_limit_config_dict()




class PyMorph(InitializeParams):
    
    __version__ = 3.0

    def __init__(self, config_file='config.ini'):

        super()._initilize_params(config_file=config_file) 
        galfitv = self.pymorph_config['galfitv'].split('.')
        galfitv = galfitv[0] + '.' + galfitv[1]
        self.galfitv = float(galfitv)
        self.pymorph_config['galfitv'] = float(galfitv)

    def _indexfile(self):
        #Initialize index.html
        if os.path.exists('index.html'):
            pass
        else:
            indexfile = open('index.html', 'w')
            indexfile.writelines(['<HTML>\n<BODY>\n'])
            indexfile.writelines(['</BODY></HTML>'])
            indexfile.close()



    def main_thread(self):

        print(self.pixelscale, self.ReSize, self.FixSize)

        #try:
        os.system('rm -f TmpElliMask.fits TmpElliMask1.fits')
        #except:
        #    pass

        self._indexfile()
        

        print(self.imagefile)
        #print(self.imagedata)
        print('Image done')
        print(self.whtfile)
        print('Weight done')
        #Initializing psf array. ie. creating psflist from file 
        self.psflist = pf.PSFArr(self.DATADIR, self.psflist)
        if self.decompose:
            for p in self.psflist:
                print('psf', self.DATADIR, p)
                pf.UpdatePsfRaDec(self.DATADIR, p)


        #XXX
        #self.P.psflist = self.psflist

        # Writing csv header and finding the output parameters
        params_to_write = ut.output_params(self.dbparams, self.decompose)    

        #XXX
        #self.P.params_to_write = params_to_write

        if os.path.exists('result.csv'):
            pass
        else:
            f_res = open("result.csv", "a")
            csvhead = ['{}_{:d}'.format(params_to_write[par_key][0], par_key)
                       for par_key in params_to_write.keys()]
            writer = csv.writer(f_res)
            writer.writerow(csvhead)
            f_res.close()

        f_cat = open(self.out_cata, 'w')
        f_failed = open('restart.cat', 'w')
        #obj_cata = open(self.obj_cata, 'r')  # The file contains the 
                                                     # objects of interest
        #pnames = obj_cata.readline().split() #The names of the parameters given 
                                             #in the first line in the obj_cata


        #print('Before multi')
        #pool = Pool(processes=1)
        #results = pool.map(self.P.main, obj_cata)
        #pool.close()
        #pool.join()


        #self.obj_cata = obj_cata
        #pnames = obj_file.readline().split() #The names of the parameters given 
                                             #in the first line in the obj_cata
        #self.obj_cata = obj_cata
        obj_values = np.genfromtxt(self.obj_cata, names=True)

        pnames = obj_values.dtype.names
        print('pnames', pnames)
        print(obj_values.shape)

        if len(obj_values) == 0:
            print('No lines in {}'.format(self.obj_cata))
            print('Exiting PyMorph')
            sys.exit()


        # writing a input catalogue (restart.cat) for failed objects
        for pname in pnames:
            f_failed.writelines(['{} '.format(pname)])
        f_failed.writelines(['flag \n'])


        self.psfcounter = 0       #For getting psf in the case of unknown ra

        #print(1, imgsize, whtsize)


        P = Pipeline()
        P.pymorph_config = self.pymorph_config
        P.sex_config = self.sex_config
        P.limit_config = self.limit_config

            
        P.imagedata = self.imagedata
        P.weightdata = self.weightdata
        P.NXPTS = self.imagedata.shape[0]
        P.NYPTS = self.imagedata.shape[1]
        P.weightexists = self.weightexists

        P.EXPTIME = self.EXPTIME
        P.RDNOISE = self.RDNOISE
        P.GAIN = self.GAIN
        P.SEx_GAIN = self.SEx_GAIN
        P.NCOMBINE = self.NCOMBINE
        P.center_deviated = self.center_deviated

        P.DATADIR  = self.DATADIR
        P.OUTDIR = self.OUTDIR
        P.imagefile = self.imagefile
        P.whtfile  = self.whtfile
        P.sex_cata = self.sex_cata
        P.obj_cata  = self.obj_cata
        P.out_cata = self.out_cata
        P.rootname = self.rootname
        P.GALFIT_PATH = self.GALFIT_PATH
        P.SEX_PATH = self.SEX_PATH
        P.repeat = self.repeat
        P.galcut  = self.galcut
        P.decompose  = self.decompose
        P.detail = self.detail
        P.galfit  = self.galfit
        P.cas  = self.cas
        P.crashhandler = self.crashhandler
        P.components  = self.components
        P.devauc = self.devauc
        P.fitting  = self.fitting
        P.chi2sq  = self.chi2sq
        P.goodness = self.goodness
        P.center_deviation = self.center_deviation
        P.center_constrain = self.center_constrain
        P.ReSize  = self.ReSize
        P.VarSize  = self.VarSize
        P.FracRad  = self.FracRad
        P.Square  = self.Square
        P.FixSize = self.FixSize
        P.searchrad  = self.searchrad
        P.pixelscale = self.pixelscale
        P.H0 = self.H0
        P.WM = self.WM
        P.WV = self.WV
        P.redshift = self.redshift
        P.psfselect = self.psfselect
        P.stargal_prob= self.stargal_prob
        P.star_size  = self.star_size
        P.psflist  = self.psflist
        P.which_psf = self.which_psf
        P.area_obj = self.area_obj
        P.manual_mask  = self.manual_mask
        P.mask_reg  = self.mask_reg
        P.thresh_area  = self.thresh_area
        P.threshold  = self.threshold
        P.mag_zero  = self.mag_zero
        P.maglim = self.maglim
        P.host = self.host
        P.database = self.database
        P.table = self.table
        P.user  = self.user
        P.password  = self.password
        P.dbparams = self.dbparams
        P.galfitv = self.galfitv
        P.FirstCreateDB= self.FirstCreateDB
        P.FILTER  = self.FILTER
        P.LMag = self.LMag
        P.UMag  = self.UMag
        P.LN = self.LN
        P.UN = self.UN
        P.LRe  = self.LRe
        P.URe = self.URe
        P.LRd  = self.LRd
        P.URd = self.URd
        P.bdbox  = self.bdbox
        P.bbox = self.bbox
        P.dbox = self.dbox
        P.devauc  = self.devauc
        P.avoidme  = self.avoidme
        P.no_mask  = self.no_mask
        P.norm_mask  = self.norm_mask

        P.sex_params = self.sex_params

        P.pnames = pnames
        P.params_to_write = params_to_write

        pdb = {}                        #The parameter dictionary
        for obj_value in obj_values:
            P.main(obj_value)


        print(results)

    def find_and_fit(self):
        '''
        Find all the sextractor objects and find fits. It rewrites the
        obj_cata in config.ini
        '''

        print('find_and_fit 1')
        #fc = open(self.obj_cata, 'w')
        #if self.redshift == 9999:
        #    fc.writelines(['gal_id ra dec mag\n'])
        #else:
        #    fc.writelines(['gal_id ra dec mag z\n'])

        values = np.genfromtxt(self.sex_cata)
        print(self.sex_cata)

        print(values.shape)
        con = (values[:, 17] > self.UMag) & (values[:, 17] < self.LMag) & (values[:, 16] < self.stargal_prob)
        values = values[con]
        values = values[:, [0, 3, 4, 17]]
        print(values)
        values[:, 3] = values[:, 3] / 15.0

        if self.redshift != 9999:
            values[:, -1] = self.redshift
            np.savetxt(self.obj_cata, values, fmt='%i %.8f %.8f %.2f %.3f',
                    header='gal_id ra dec mag z', comments='')
        else:
            np.savetxt(self.obj_cata, values, fmt='%i %.8f %.8f %.2f',
                    header='gal_id ra dec mag', comments='')


        searchrad = '0.05arc'

        print('find_and_fit 2')

    def pymorph(self):


        # now change dir to the 
        thisdir = os.getcwd()
        print("Current directory is ", thisdir)
        print("Output directory is ", self.OUTDIR)

        os.chdir(self.DATADIR)



        if 1:
            print(1)
            
            if self.repeat == False & self.galcut == False:
                print(2)
                fimg = fitsio.FITS(self.imagefile)
                self.imagedata = fimg[0].read()
                self.header0 = fimg[0].read_header()
                fimg.close()
                self.NXPTS = self.imagedata.shape[0]
                self.NYPTS = self.imagedata.shape[1]
                
                gheader = ut.CheckHeader(self.header0)
                self.EXPTIME = gheader[0]
                self.RDNOISE = gheader[1],
                self.GAIN = gheader[2]
                self.SEx_GAIN = gheader[3]
                self.NCOMBINE = gheader[4]

                print("Using large image. imagefile >>> {}".format(self.imagefile))
            else:
                print(4)
                self.SEx_GAIN = 1.

            if self.repeat == False & self.galcut == False & os.path.exists(self.whtfile):
                self.weightexists = True
                
                wht = fitsio.FITS(self.whtfile)

                if re.search("rms", self.whtfile.lower()):
                    self.weightdata = wht[0].read()
                    print("whtfile >>> {}".format(self.whtfile))
                elif re.search("weight", self.whtfile.lower()):
                    self.weightdata = 1 / np.sqrt(wht[0].read())
                    print("whtfile >>> {}".format(self.whtfile))
                else:
                    print('Weight file is not understood. Please include ' + \
                          'the word weight/rms to the weight file name. ' + \
                          'If it is weight the rms will be found by 1/sqrt(w)')
                wht.close()
                print('No weight image found\n')


            else:
                self.weightexists = False
            
        #except IOError as e:
        #    print(self.imagefile, "I/O error ({}): {}".format(e.args[0], e.args[1]))
        #    os._exit(0)
        
        print(self.sex_cata)
        if os.path.exists(self.sex_cata):
            pass
            print(5)
        elif self.galcut == False:
            print('The SExtractor catalogue for your frame is NOT found. ' \
                  'One is being made using the default values. It is always '\
                  'recommended to make SExtractor catalogue by YOURSELF as '\
                  'the pipeline keeps the sky value at the SExtractor value '\
                  'during the decomposition.')
            print(6)
            PS = PySex(self.SEX_PATH)
            PS.RunSex(self.sex_config,  
                   self.imagefile, self.whtfile,
                   self.sex_cata, self.SEx_GAIN,
                   check_fits=None, sconfig='default')

        #sys.exit()
    #The old function for psfselect = 2
    #    if psfselect == 2:
    #        center_deviated = 0
    #        starthandle = 0
    #        os.system('ds9 &')
    #        time.sleep(2)
    #        run_psfselect(imagefile, DATADIR, obj_cata, self.galcut)
    #        os.system('xpaset -p ds9 quit')
    #        psflist = '@psflist.list'
    #        find_and_fit()
    #        main()
    #        if crashhandler:
    #            starthandle = 1
    #            os.system('mv restart.cat CRASH.CAT')
    #            obj_cata = 'CRASH.CAT' 
    #            main()
    #New function for psfselect=2 non-interactive for webservice
        print(self.psfselect)
        print(self.obj_cata)
        if self.psfselect == 2:
            self.Interactive = 0
            self.center_deviated = 0
            self.starthandle = 0
            run_psfselect(self.imagefile, 
                          self.DATADIR, 
                          self.obj_cata, 
                          self.galcut)
            psflist = os.path.join(self.DATADIR, '@psflist.list')
            self.find_and_fit()
            self.main()
            if self.crashhandler:
                starthandle = 1
                os.system('mv restart.cat CRASH.CAT')
                self.obj_cata = 'CRASH.CAT' 
                self.main()

    #The old function for psfselect=1
        elif self.psfselect == 1:
            self.Interactive = 1
            os.system('ds9 &')
            time.sleep(2)
            run_psfselect(self.imagefile, 
                          self.DATADIR, 
                          self.obj_cata, 
                          self.galcut)
            os.system('xpaset -p ds9 quit')
    #new function for psfselect=1 non-interactive for webservice (abhishek rawat)
    #    elif psfselect == 1:
    #        Interactive = 0
    #        run_psfselect(imagefile, DATADIR, obj_cata, self.galcut)
            



        elif self.psfselect == 0:
            self.center_deviated = 0
            self.starthandle = 0
            if self.findandfit == True:
                self.find_and_fit()
            print(self.sex_cata)
            self.main_thread()
            if self.crashhandler:
                self.starthandle = 1
                os.system('mv restart.cat CRASH.CAT')
                self.obj_cata = 'CRASH.CAT' 
                self.main()

        os.chdir(thisdir)





if __name__ == '__main__':
    p = PyMorph()
    p.set_sexparams()
    p.set_limits()
    p.pymorph()
    #p.main()
