# NASA ACME 3D CAD Repository & Model Archive

This directory provides the consolidated 3D CAD models, subassemblies, and production STEP AP214 files for the **NASA ACME (Advanced Combustion via Microgravity Experiments)** flight insert, engineered for the International Space Station (ISS) Combustion Integrated Rack (CIR).

---

## Subsystem Directory Structure

```
CAD/
├── 01_Chamber_Insert/                    # Consolidated Flight Insert Assembly
│   ├── s1101mfa0003_chamber_insert.step  # Master STEP AP214 insert assembly
│   ├── s1101mfa0003_chamber_insert.iam   # Autodesk Inventor master assembly
│   └── ACME_Insert_Simplificado.stp      # Enclosure reference shell
│
├── 02_Experiment_Mounting_Structure_EMS/ # Structural Framework & Cold Plates
│   ├── s1101mfa1000.step                 # Complete EMS Structural Assembly
│   ├── s1101mfa1001.iam / .stp           # Lower Mounting Plate Assembly
│   ├── s1101mfa1003.iam / .stp           # EMS Structural Cage Frame
│   └── Pecas/                            # Individual brackets, gussets, and plates
│
├── 03_Burner_Assembly/                   # 1/4" & 3/8" Porous Spherical Burners
│   ├── S1101MFA1220_B.step               # 3/8" Spherical Burner Multi-Solid
│   ├── S1101MFA1218_A.step               # 1/4" Flight Burner Tip
│   ├── S1101MFD1201.stp                  # Burner Insulator Mounting Base
│   └── S1101MFD1268_Coflow_Burner_Collar.stp # Coflow Diffusion Aerodynamic Collar
│
├── 04_Igniter_Assembly/                  # Articulated Motorized Igniter Subsystem
│   ├── s1101mfa1300.iam / .stp           # Full Motorized 4-Bar Kinematic Assembly
│   ├── s1101mfa1339_ponteira_ignitor.stp # High-Precision Igniter Tip Assembly
│   ├── S1101MFA1319_C.step               # Filament Retention Loop
│   ├── S1101MFD1320.stp                  # Actuator Mounting Interface
│   └── igniter_braco_all.step            # Articulated Linkage Arm
│
├── 05_Thermal_Rake_Array/                # Far-Field Boundary Thermocouple Arrays
│   ├── S1101MFA1606.stp                  # Thermocouple Rake Subassembly
│   └── s1101mfa1609_1609_OPER.stp        # Operational Far Rake Sensor Array
│
└── 06_Standard_Hardware_Fasteners/       # Aerospace Flight Hardware (NAS / MS Standards)
    ├── nas1102e / nas1149 / nas1351 / nas1352 # High-strength aerospace socket screws & washers
    └── ms51830ca103l                     # Aerospace locking inserts
```

---

## Supported File Formats

* **STEP AP214 (`.stp` / `.step`):** Universal neutral exchange format containing full 3D boundary representation (B-Rep) geometry, multi-solid assembly hierarchy, and millimeter unit definitions. Compatible with Autodesk Inventor, SolidWorks, CATIA, Siemens NX, FreeCAD, Rhino, and ANSYS SpaceClaim.
* **Autodesk Inventor (`.iam` / `.ipt`):** Native parametric CAD models containing feature trees, parametric sketches, work planes, and physical aerospace materials (Inconel 625, 316L SS, Al 6061-T6, Alumina Ceramic).

---

## Technical Leadership & CAD Authorship

* **Lead Mechanical Design & Simulation Engineer:** Emerson B. J. ([@EmersonBJ](https://github.com/EmersonBJ))
