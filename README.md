Upload Metadata to ESRI Arcgis Portal 
===================

One the problems with the portal for arcgis is that the metadata of a dataset in the geodatabase, isn't uploaded to the  server. So the user needs to manualy copy paste the description of the layer, author, ... from metadata to the portal every time he edits the metadata.

This script will upload created a item in the portal with the correct metadata for every item in a Arcgis mapdocument. The user needs to provide the link to the service. If a item already exists with the same name it will be overwriten. 

It is very important that the layername order in the mxd corresponds with name in the service. Also if you change a name of a item or move it. Then the layer will be added again as new item the next time you run the script, instead of updating it. 

So you can run this script daily to update changes in the metadata. 

    usage: uploadMetadata2portal.py [-h] [--portal PORTAL] [--user USER]
                                    [--password PASSWORD] [--mxd MXD]
                                    [--service SERVICE] [--group GROUP] [--ws WS]
                                    [--del_if_in_group_not_in_mxd DEL_IF_IN_GROUP_NOT_IN_MXD]

    optional arguments:
      -h, --help            show this help message and exit
      --portal PORTAL       the link to the ESRI argis Portal, default is Arcgis
                            online
      --user USER           the username of the ESRI argis Portal
      --password PASSWORD   the password of the ESRI argis Portal
      --mxd MXD             the mxd to with sync with the ESRI argis Portal
      --csv                 the csv to with featurs sync with the ESRI argis Portal, 
                            The csv has the follwing sturcture: firstline=headers, following lines:  name;path;url
                            if this argument is added --mxd and --service wil be ignored.
      --service SERVICE     the link to !CORRESPONDING! mapservice of the mxd
      --group GROUP         add all layers to this group
      --ws WS               worskpace a location of a geodatabase that overwrites
                            the location in the mxd, for example a .sde file
      --del_if_in_group_not_in_mxd DEL_IF_IN_GROUP_NOT_IN_MXD
                            Will delete al layers not in mxd but in group, skip if
                            no group

      
<img  width="450" src="https://docs.google.com/drawings/d/1sMhr11r6yopZ8S7nIzhhvZ8qKXnxMBoFWQJmwiquWqw/pub?w=926&amp;h=926">
