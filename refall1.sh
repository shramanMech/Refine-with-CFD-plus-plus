#!/bin/bash 


cd $1
mkdir paraview_files
mv *.vtk paraview_files
echo "Copy the following to open paraview. Once saved, close it and run refall2.sh"
echo "paraview $1/paraview_files/mcfdsol.vtk"
