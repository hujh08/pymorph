import os, sys, pyfits
import numpy as n
import config as c

class OutMaskFunc:
    """The class for making mask for output image from GALFIT to run ellipse.
       The file name of the mask is OEM_string(galid).fits"""
    def __init__(self, OUTDIR, xcntr, ycntr, NXPTS, NYPTS, line_s):
        self.OUTDIR = OUTDIR
        self.xcntr = xcntr
        self.ycntr = ycntr
        self.NXPTS = NXPTS
        self.NYPTS = NYPTS
        self.line_s  = line_s

    def mask(self, xcntr, ycntr, NXPTS, NYPTS, line_s):
        imagefile = c.imagefile
        sex_cata = c.sex_cata
        threshold = c.threshold
        thresh_area = c.thresh_area
        mask_reg = c.mask_reg
        values = line_s.split()
        mask_file = 'OEM_' + c.fstring + '.fits'
        emask_file = 'EM_' + str(outimage)[2:-5] + '.fits'
        os.system('cp ' + emask_file + ' '+ mask_file)
