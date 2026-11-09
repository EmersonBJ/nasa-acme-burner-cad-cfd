import os
import shutil

repo_root = r"D:\NASA_CAD_Reverse_Engineering"
cad_root = os.path.join(repo_root, "CAD")

source_cads_nosso = os.path.join(repo_root, "PSI-Documents", "Engineering Documents", "CADs_Nosso")
source_reports_cad = os.path.join(repo_root, "PSI-Documents", "Reports", "CAD")

dirs = {
    "01_Chamber_Insert": os.path.join(cad_root, "01_Chamber_Insert"),
    "02_Experiment_Mounting_Structure_EMS": os.path.join(cad_root, "02_Experiment_Mounting_Structure_EMS"),
    "03_Burner_Assembly": os.path.join(cad_root, "03_Burner_Assembly"),
    "04_Igniter_Assembly": os.path.join(cad_root, "04_Igniter_Assembly"),
    "05_Thermal_Rake_Array": os.path.join(cad_root, "05_Thermal_Rake_Array"),
    "06_Standard_Hardware_Fasteners": os.path.join(cad_root, "06_Standard_Hardware_Fasteners"),
}

for d in dirs.values():
    os.makedirs(d, exist_ok=True)

def copy_file(src, dst_dir):
    if os.path.exists(src):
        dst = os.path.join(dst_dir, os.path.basename(src))
        if not os.path.exists(dst) or os.path.getsize(src) != os.path.getsize(dst):
            shutil.copy2(src, dst)
            print(f"Copied {os.path.basename(src)} -> {os.path.basename(dst_dir)}")

# 1. Chamber Insert
mont_final = os.path.join(source_cads_nosso, "Montagem_Final")
for f in ["s1101mfa0003_chamber_insert.iam", "s1101mfa0003_chamber_insert.step", "s1101mfa0003_chamber_insert.stp"]:
    copy_file(os.path.join(mont_final, f), dirs["01_Chamber_Insert"])
for f in ["ACME_Insert_Simplificado.ipt", "ACME_Insert_Simplificado.stp"]:
    copy_file(os.path.join(source_reports_cad, f), dirs["01_Chamber_Insert"])

# 2. EMS Structure
ems_dir = os.path.join(source_cads_nosso, "Expt_Mounting_Structure")
ems_mont = os.path.join(ems_dir, "Montagens")
ems_pecas = os.path.join(ems_dir, "Pecas")

for root, _, files in os.walk(ems_dir):
    if "OldVersions" in root or "_Backup" in root:
        continue
    for f in files:
        if not (f.endswith(".stp") or f.endswith(".step") or f.endswith(".ipt") or f.endswith(".iam")):
            continue
        fl = f.lower()
        src_path = os.path.join(root, f)
        if any(h in fl for h in ["nas", "ms518", "washer"]):
            copy_file(src_path, dirs["06_Standard_Hardware_Fasteners"])
        else:
            copy_file(src_path, dirs["02_Experiment_Mounting_Structure_EMS"])

# 3. Burner Assembly
burner_dir = os.path.join(source_cads_nosso, "Burner")
for root, _, files in os.walk(burner_dir):
    if "OldVersions" in root:
        continue
    for f in files:
        if f.endswith(".stp") or f.endswith(".step") or f.endswith(".ipt") or f.endswith(".iam"):
            copy_file(os.path.join(root, f), dirs["03_Burner_Assembly"])

serie_dir = os.path.join(source_cads_nosso, "Serie_1100_a_1109")
if os.path.exists(serie_dir):
    for f in os.listdir(serie_dir):
        if f.endswith(".stp") or f.endswith(".step") or f.endswith(".ipt") or f.endswith(".iam"):
            copy_file(os.path.join(serie_dir, f), dirs["03_Burner_Assembly"])

# 4. Igniter Assembly
igniter_dir = os.path.join(source_cads_nosso, "Igniter")
for root, _, files in os.walk(igniter_dir):
    if "OldVersions" in root:
        continue
    for f in files:
        if f.endswith(".stp") or f.endswith(".step") or f.endswith(".ipt") or f.endswith(".iam"):
            copy_file(os.path.join(root, f), dirs["04_Igniter_Assembly"])

# 5. Thermal Rake
rake_dir = os.path.join(source_cads_nosso, "Thermal_Rake")
if os.path.exists(rake_dir):
    for root, _, files in os.walk(rake_dir):
        for f in files:
            if f.endswith(".stp") or f.endswith(".step") or f.endswith(".ipt") or f.endswith(".iam"):
                copy_file(os.path.join(root, f), dirs["05_Thermal_Rake_Array"])

print("CAD mirror completed successfully!")
