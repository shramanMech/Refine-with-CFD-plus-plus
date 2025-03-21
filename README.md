# Refine-with-CFD++
A workflow for using NASA's Refine with CFD++. General instructions for mesh adaptation using [NASA's Refine](https://github.com/nasa/refine?tab=readme-ov-file) can be found [here*](https://github.com/aravind-balan/Mesh-Adaptation/tree/main).

## Instructions: 

**1. Creation of the initial mesh**

Any good meshing tool can be used for the creation of the initial mesh. Just keep in mind it is able to export the mesh in the binary formats needed by CFD++ or any of the other formats that CFD++ can convert from.

**1.1. Case I: If mesh is exported in CFD++ readable format**

Store the exported files in the folder which will contain all the set-up and output files for that particular case and run the solver.

**1.2. Case II: If mesh is exported in .su2 format**

Once, the mesh has been exported as a .su2 file, the built-in mesh converter of CFD++ can be used. The corresponding executable for the converter is convert25.c which is invoked in the background. To invoke this converter follow the following sequence:

*Tools >> Import >> Convert from SU2 >> Select the file >> Run*

**1.3. Case III: Using Refine’s bootstrap command**

For using this, the geometry file must exist in the .stp or .step formats and should be converted to a .egads format. This geometry can be used to create the initial mesh. The instructions for these can be found in the link * (in section 1). For reference, the command for bootstrap is as follows:
```
ref bootstrap geometry title.egads
```
By default, the mesh that comes out of bootstrap is a very coarse mesh in .meshb format. The mesh can be made uniformly finer using the *implied-complexity* option of the adapt command.
It can be done as follows:
```
ref adapt bootstrapped-mesh.meshb --implied-complexity $COMPLEXITY -x output-mesh.meshb
```
This mesh can now be converted to .su2 format and can be used in CFD++ (as shown in section 2.1.1 ). The command for converting .meshb to .su2 is as follows:
```
ref translate output-mesh.meshb output-mesh.su2
```
**2. Solving with CFD++ and exporting the solutions**

Once the set-up is done and the case has been run to achieve a satisfactory level of convergence, the solution files can be exported to a Paraview-readable .vtk format using another built-in converter of CFD++. To invoke the converter, follow the following sequence: 

*Tools >> Export >> VTK >> ASCII >> Run*

This will create mcfdsol.vtk for the entire volume and mcfdsol_bc*.vtk for the corresponding boundaries. The converter can also be invoked as an API command as follows:
```
genplif pltosout.bin vtk
```
Copy the Python file **writesol_volnsurf.py** in the folder (or link it using ln -s to the folder) and run it. It will create two solution files named *mach.sol* and *yplus.sol*. The script has been written to write out a volume variable and a surface variable. Make relevant changes in the Python file to read other variables by changing the variables *reqvar_vol*  and *reqvar_surf* in the Python script.

**P.S.:** If the inital mesh was in a CFD++ readable format, along with the solution files, a *.su2* format of the mesh should also be exported using the following sequence:

*Tools >> Export >> Other >> SU2 Format >> Name the file >> Run*

Once the *.su2* file is present, it can be converted to .meshb for adaptation using:
```
ref translate inputmesh.su2 inputmesh.meshb
```
**3. Mesh adaptation**

Once the relevant solution file is available, the adaptation can be done. Here we will use the solution of the Mach number for demonstration. To create the multiscale metric, the following command is used:
```
mpirun -np $NUMPROCS refmpifull multiscale inputmesh.meshb ./mach.sol $COMPLEXITY mach-output-metric.solb
```
This will create the multiscale metric file named mach-output-metric.solb. This can be used for adapting. The command for adapting the mesh is as follows:
```
mpirun -np $NUMPROCS refmpifull adapt inputmesh.meshb --egads geometry title.egads -m mach-output-metric.solb -x mach-adapted-mesh.meshb
```

**P.S.:** The .egads geometry file can be passed in the command **ONLY** when the initial geometry is bootstrapped. Otherwise, the part **--egads geometry title.egads** can be removed from the command. More detailed instructions can be found [here*](https://github.com/aravind-balan/Mesh-Adaptation/tree/main).

Once we have the adapted mesh, it can be converted to .su2 using the following command:
```
ref translate mach-adapted-mesh.meshb mach-adapted-mesh.su2
```
**4. Repeating the process**

Once the .su2 file is available, it can be copied to the folder for the next adaptation cycle, and the
process can be repeated. From now on, the instructions shown in section 1.2 can be used
for all the subsequent adaptation cycles.

**5. Shell scripts for automation**

A shell script named **refall.sh** was written to streamline the workflow. Although the scripts do not ensure complete automation, most of the steps have been added to these files to speed up the process.

Place the file in the parent folder that contains the sub-directories for all the adaptation cycles.
The script is self-explanatory, and comments have been added wherever changes are required. It should be called in the following way:
```
./refall.sh $CURRENT_RUN_NUMBER $NEXT_RUN_NUMBER $COMPLEXITY $NUMPROCS
```
This will invoke the CFD++ GUI and stop executing.

Once the solver has run and the solution files have been exported (in .vtk format) through the GUI, *refall.sh* can be run again for the next cycle.
