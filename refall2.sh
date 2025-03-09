#!/bin/bash 


cd $1
echo "moving into directory corrsponding to adaptation $1"
cd ./paraview_files
ln -s /../../writesol.py 			# Please change this line as per the location of writesol.py
python3 writesol.py 
echo "solution file has been written. starting refine..."
cd ../
mpirun -np $4 refmpifull multiscale inputmesh.meshb ./paraview_files/mach.sol $3 mach-output-metric.solb
echo "multiscale metric created for target complexity of $3"
# ref adapt inputmesh.meshb --egads ../../HEG-Cylinder.egads -m mach-output-metric.solb -x mach-adapted-mesh.meshb	# off: for hybrid; 		on: otherwise  # Change based on the location of the .egads file
mpirun -np $4 refmpifull adapt inputmesh.meshb -m mach-output-metric.solb -x mach-adapted-mesh.meshb						# off: for all except hybrid; 	on: for hybrid
echo "adapted mesh has been created"
ref translate mach-adapted-mesh.meshb mach-adapted-mesh.su2
mkdir ../$2
cp mach-adapted-mesh.meshb ../$2/inputmesh.meshb
cp mach-adapted-mesh.su2 ../$2/inputmesh.su2
cp *.inp ../$2/
echo "refinement completed and files moved to the next folder"
echo ""
cd ../$2
mcfdaui.211
echo "Complete the set-up and run the simulation."

