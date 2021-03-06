#!/usr/local/bin/python
# -*- coding: utf-8 -*
#---------------------------------------------------------------------------------
# Name:        uploadMetadata2portal.py
# Purpose:     parse a mxd and upload all layers with metadata to a Arcgis portal.
#
# Author:      Kay Warrie
#
# Created:     20/03/2017
# Copyright:   (c) Stad Antwerpen 2017
# Licence:     MIT
#
# usage: uploadMetadata2portal.py [-h] [--portal PORTAL] [--user USER] [--mxd MXD]
#                              [--password PASSWORD] [--service SERVICE] [--ws WS]
#
# optional arguments:
#       -h --help            show this help message and exit
#       --portal PORTAL      the link to the ESRI argis Portal
#       --user USER          the username of the ESRI argis Portal
#       --password PASSWORD  the password of the ESRI argis Portal
#       --mxd MXD            the mxd to with sync with the ESRI argis Portal
#       --service SERVICE    the link to !CORRESPONDING! mapservice of the mxd
#       --group GROUP        add all layers to this group
#       --ws WS              worskpace a location of a geodatabase that overwrites
#                            the location in the mxd, for example a .sde file
#---------------------------------------------------------------------------------
import argparse, getpass
from   portal.metadata2portal import metadata2portal
from   portal.csvportal import csvportal
#add your portal-url, username and pasword, mxd and corresponding mapservice
#if you dont want to use comamndline parameters:
PORTAL  = "https://arcgis.com"
USER    = ""
PASS    = ""
MXD     = r""
CSV     = r""
SERVICE = ""
GROUP   = ""
WS      = r""
DEL_GRP = True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--portal",  help="the link to the ESRI argis Portal, default is Arcgis online", default=PORTAL)
    parser.add_argument("--user",    help="the username of the ESRI argis Portal", default=USER)
    parser.add_argument("--password",help="the password of the ESRI argis Portal", default=PASS)
    parser.add_argument("--mxd",     help="the mxd to with sync with the ESRI argis Portal", default=MXD)
    parser.add_argument("--csv",     help="""the csv to with featurs sync with the ESRI argis Portal, 
        The csv has the follwing sturcture: firstline=headers, following lines:  name;path;url
        if this argument is added --mxd and --service wil be ignored.""", default=CSV)
    parser.add_argument("--service", help="the link to !CORRESPONDING! mapservice of the mxd", default=SERVICE)
    parser.add_argument("--group",   help="add all layers to this group", default=GROUP)
    parser.add_argument("--ws",      help="worskpace a location of a geodatabase that overwrites the location in the mxd, for example a .sde file", default=WS)
    parser.add_argument("--del_if_in_group_not_in_mxd", help="Will delete al layers not in mxd but in group, skip if no group", default=DEL_GRP)

    args = parser.parse_args()

    if not args.user: user = raw_input("Username: ")
    else: user = args.user

    if not args.password: password = getpass.getpass()
    else: password = args.password

    if args.csv == "" or args.csv is None:
       if not args.mxd: mxd = raw_input("ESRI mapdocument (*mxd): ")
       else: mxd = args.mxd

       if not args.service: service = raw_input("ESRI mapservice (url): ")
       else: service = args.service
       #make sure service ends with a slash
       service = service if args.service.endswith("/") else service + "/"

    if not args.group: groups = []
    else: groups = [args.group]

    if not args.ws: ws = None
    else: ws = args.ws
    
    if not args.csv : 
       m2p = metadata2portal(user, password, args.portal, ws, groups)
       m2p.uploadEveryLayerInMxd(mxd, service, args.del_if_in_group_not_in_mxd)
    else:
       c2p = csvportal(user, password, args.portal, ws, groups)
       c2p.uploadCsv(args.csv)


if __name__ == '__main__':
    main()