import numpy as np

fp1 = "mcfdsol.vtk"
fp2 = "mcfdsol_bc1.vtk"
dim = 2
reqvar_vol = 'M'
reqvar_surf = 'Y_plus'
volvar_unsort = []
surfvar_unsort = []

with open(fp1, 'r') as volfile:
    lines = volfile.readlines()

    reqsec = False

    for line in lines:

        line = line.split()
        # print(line)

        if len(line) > 1 and line[1] == reqvar_vol:
            reqsec = True
            continue
        elif reqsec and line[0] == "SCALARS":
            break

        if reqsec:
            if line[0] == "LOOKUP_TABLE":
                continue
            else:
                # vardata = line.split()
                volvar_unsort.append(list(map(float, line)))
    
volvar_srtd = []
for volvar_line in volvar_unsort:
    for volvar in volvar_line:
        volvar_srtd.append(volvar)
        
linesModvol = []
linesModvol.append("MeshVersionFormatted 1")
linesModvol.append(["Dimension", str(dim)])
linesModvol.append("SolAtVertices")
linesModvol.append(str(len(volvar_srtd)))
linesModvol.append([1, 1])
linesModvol.append("")
for volvar in volvar_srtd:
    linesModvol.append(str(volvar))
linesModvol.append("END")

with open("mach.sol", 'w') as file:
    for line in linesModvol:
        if isinstance(line, list):  
            file.write(" ".join(map(str, line)) + '\n')
        else:  
            file.write(str(line) + '\n')
            
with open(fp2, 'r') as surffile:
    lines = surffile.readlines()

    reqsec = False

    for line in lines:

        line = line.split()
        # print(line)

        if len(line) > 1 and line[1] == reqvar_surf:
            reqsec = True
            continue
        elif reqsec and line[0] == "SCALARS":
            break

        if reqsec:
            if line[0] == "LOOKUP_TABLE":
                continue
            else:
                # vardata = line.split()
                surfvar_unsort.append(list(map(float, line)))
                
surfvar_srtd = []
for surfvar_line in surfvar_unsort:
    for surfvar in surfvar_line:
        surfvar_srtd.append(surfvar)
        
linesModsurf = []
linesModsurf.append("MeshVersionFormatted 1")
linesModsurf.append(["Dimension", str(dim)])
linesModsurf.append("SolAtVertices")
linesModsurf.append(str(len(surfvar_srtd)))
linesModsurf.append([1, 1])
linesModsurf.append("")
for surfvar in surfvar_srtd:
    linesModsurf.append(str(surfvar))
linesModsurf.append("END")

with open("yplus.sol", 'w') as file:
    for line in linesModsurf:
        if isinstance(line, list):  
            file.write(" ".join(map(str, line)) + '\n')
        else:  
            file.write(str(line) + '\n')

