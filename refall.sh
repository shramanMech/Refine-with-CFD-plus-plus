#!/bin/bash 


cd set_$1/$2
echo "moving into directory corrsponding to adaptation $2 of set $1"
cd ./paraview_files
ln -s ../../../writesol_volnsurf.py      # Change path of the Python file
python3 writesol_volnsurf.py 
echo "solution file has been written. starting refine..."
cd ../
ref multiscale inputmesh.meshb ./paraview_files/mach.sol $4 mach-output-metric.solb
echo "multiscale metric created for target complexity of $4"
# ref adapt inputmesh.meshb --egads ../../HEG-Cylinder.egads -m mach-output-metric.solb -x mach-adapted-mesh.meshb	# off: for hybrid; 		on: otherwise  # Change path of the egads geometry
ref adapt inputmesh.meshb -m mach-output-metric.solb -x mach-adapted-mesh.meshb						# off: for all except hybrid; 	on: for hybrid
echo "adapted mesh has been created"
ref translate mach-adapted-mesh.meshb mach-adapted-mesh.su2
mkdir ../$3
cp mach-adapted-mesh.meshb ../$3/inputmesh.meshb
cp mach-adapted-mesh.su2 ../$3/inputmesh.su2
cp *.inp ../$3/
echo "refinement completed and files moved to the next folder"
echo ""
cd ../$3
mcfdaui.211
echo "Complete the set-up and run the simulation."

