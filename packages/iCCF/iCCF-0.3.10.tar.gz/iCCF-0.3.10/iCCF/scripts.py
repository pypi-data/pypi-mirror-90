""" Command-line scripts for iCCF """

import numpy as np
import matplotlib.pyplot as plt

import os
import sys
import argparse

from . import iCCF
from . import meta_ESPRESSO
from .utils import get_ncores
# from .meta_ESPRESSO import calculate_ccf as calculate_ccf_ESPRESSO
from astropy.io import fits


def _parse_args_fits_to_rdb():
    desc = """
    This script takes a list of CCF fits files and outputs CCF activity 
    indicators to stdout, in rdb format.
    """
    parser = argparse.ArgumentParser(
        description=desc,
        prog='iccf-fits-to-rdb',
    )
    # parser.add_argument('column', nargs=1, type=int,
    #                     help='which column to use for histogram')
    parser.add_argument('--hdu', type=int, help='HDU number')
    parser.add_argument('--sort', action='store_true', default=True,
                        help='sort the output by the MJD-OBS keyword')
    parser.add_argument('--bis-harps', action='store_true', default=True,
                        help='do the bisector calculation as in HARPS')
    # parser.add_argument('--code', nargs=1, type=str,
    #                     help='code to generate "theoretical" samples '\
    #                          'to compare to the prior. \n'\
    #                          'Assign samples to an iterable called `samples`. '\
    #                          'Use numpy and scipy.stats as `np` and `st`, respectively. '\
    #                          'Number of prior samples in sample.txt is in variable `nsamples`. '\
    #                          'For example: samples=np.random.uniform(0,1,nsamples)')

    args = parser.parse_args()
    return args, parser


def fits_to_rdb():
    args, _ = _parse_args_fits_to_rdb()
    # print(args)

    bisHARPS = args.bis_harps
    hdu_number = args.hdu

    if sys.stdin.isatty():
        print('pipe something (a list of CCF fits files) into this script')
        sys.exit(1)
    else:
        files = [line.strip() for line in sys.stdin]
        # print(files)
        iCCF.indicators_from_files(files, hdu_number=hdu_number,
                                   sort_bjd=args.sort, BIS_HARPS=bisHARPS)


def _parse_args_make_CCF():
    desc = """
    This script takes a list of S2D fits files and calculates the CCF for a 
    given RV array and a given mask. If no mask is provided, it uses the same as
    specified in the S2D file.
    """
    parser = argparse.ArgumentParser(description=desc, prog='iccf-make-ccf')

    help_mask = 'Mask (G2, G9, K6, M2, ...). '\
                'A file called `ESPRESSO_mask.fits` should exist.'
    parser.add_argument('-m', '--mask', type=str, help=help_mask)

    parser.add_argument('-rv', type=str,
                        help='RV array, in the form start:end:step [km/s]')

    default_ncores = get_ncores()
    help_ncores = 'Number of cores to distribute calculation; '\
                  f'default is all available ({default_ncores})'
    parser.add_argument('--ncores', type=int, help=help_ncores)

    help_ssh = 'An SSH user and host with which the script will try to find' \
               'required calibration files. It uses the `locate` and `scp`' \
               'commands to find and copy the file from the host'
    parser.add_argument('--ssh', type=str, metavar='user@host', help=help_ssh)

    args = parser.parse_args()
    return args, parser


def make_CCF():
    args, _ = _parse_args_make_CCF()

    if sys.stdin.isatty():
        print('pipe something (a list of S2D fits files) into this script')
        print('example: ls *S2D* | iccf-make-ccf [options]')
        sys.exit(1)
    else:
        files = [line.strip() for line in sys.stdin]

        for file in files:
            print('Calculating CCF for', file)
            header = fits.open(file)[0].header

            if args.rv is None:
                try:
                    OBJ_RV = header['HIERARCH ESO OCS OBJ RV']
                    start = header['HIERARCH ESO RV START']
                    step = header['HIERARCH ESO RV STEP']
                    end = OBJ_RV + (OBJ_RV - start)
                    print('Using RV array from S2D file:',
                          f'{start} : {end} : {step} km/s')
                    rvarray = np.arange(start, end + step, step)
                except KeyError:
                    print('Could not find RV start and step in S2D file.',
                          'Please use the -rv argument.')
                    sys.exit(1)
            else:
                start, end, step = map(float, args.rv.split(':'))
                rvarray = np.arange(start, end + step, step)

            mask = args.mask
            if mask is None:
                try:
                    mask = header['HIERARCH ESO QC CCF MASK']
                except KeyError:
                    try:
                        mask = header['HIERARCH ESO PRO REC1 CAL25 NAME']
                        if 'ESPRESSO_' in mask:
                            mask = mask[9:11]
                    except KeyError:
                        print('Could not find CCF mask in S2D file.',
                              'Please use the -m argument.')
                        sys.exit(1)
                print('Using mask from S2D file:', mask)

            inst = header['INSTRUME']

            if inst == 'ESPRESSO':
                meta_ESPRESSO.calculate_ccf(file, mask=mask, rvarray=rvarray,
                                            ncores=args.ncores, ssh=args.ssh)

            elif inst == 'HARPS':
                print('dont know what to do with HARPS! sorry')
