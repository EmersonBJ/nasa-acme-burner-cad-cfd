import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import os
import matplotlib.patheffects as pe

def render_cad_model(
    glb_path,
    output_png,
    title,
    part_number,
    material_spec,
    base_color=(0.28, 0.65, 0.95), # Aerospace blue/cyan
    edge_color="#0d1829",
    elev=26,
    azim=-55,
    figsize=(14, 9),
    dpi=220,
    subtitle="NASA ACME FLIGHT HARDWARE REVERSE ENGINEERING"
):
    print(f"Loading {glb_path}...")
    scene = trimesh.load(glb_path)
    if isinstance(scene, trimesh.Scene):
        meshes = [g for g in scene.geometry.values() if isinstance(g, trimesh.Trimesh)]
        if not meshes:
            raise ValueError(f"No meshes found in {glb_path}")
        mesh = trimesh.util.concatenate(meshes)
    else:
        mesh = scene

    verts = mesh.vertices
    faces = mesh.faces
    normals = mesh.face_normals

    print(f"Mesh: {len(verts)} vertices, {len(faces)} faces")

    # If faces > 45000, uniform subsample for smooth & fast vector rendering
    if len(faces) > 45000:
        step = int(np.ceil(len(faces) / 40000))
        faces = faces[::step]
        normals = normals[::step]

    # Two-point aerospace lighting (Key light + Fill light)
    key_light = np.array([0.55, 0.65, 0.75])
    key_light /= np.linalg.norm(key_light)

    fill_light = np.array([-0.6, -0.3, 0.4])
    fill_light /= np.linalg.norm(fill_light)

    intensity_key = np.clip(np.dot(normals, key_light), 0.0, 1.0)
    intensity_fill = np.clip(np.dot(normals, fill_light), 0.0, 1.0) * 0.35
    ambient = 0.18

    total_intensity = np.clip(intensity_key * 0.75 + intensity_fill + ambient, 0.15, 1.0)

    # Compute face colors
    colors = np.outer(total_intensity, np.array(base_color))
    # Specular shine
    half_vec = key_light + np.array([0, 0, 1])
    half_vec /= np.linalg.norm(half_vec)
    specular = np.power(np.clip(np.dot(normals, half_vec), 0.0, 1.0), 16) * 0.25
    colors = np.clip(colors + np.outer(specular, np.array([1.0, 1.0, 1.0])), 0.0, 1.0)

    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor='#090d16')
    ax = fig.add_subplot(111, projection='3d', facecolor='#090d16')

    poly = Poly3DCollection(
        verts[faces],
        facecolors=colors,
        edgecolors=edge_color,
        linewidths=0.18,
        alpha=1.0
    )
    ax.add_collection3d(poly)

    # Centering & Aspect ratio bounding box
    min_b = verts.min(axis=0)
    max_b = verts.max(axis=0)
    max_range = (max_b - min_b).max() / 2.0
    mid = (max_b + min_b) * 0.5

    ax.set_xlim(mid[0] - max_range, mid[0] + max_range)
    ax.set_ylim(mid[1] - max_range, mid[1] + max_range)
    ax.set_zlim(mid[2] - max_range, mid[2] + max_range)

    ax.axis('off')
    ax.view_init(elev=elev, azim=azim)

    # Technical Aerospace HUD annotations
    plt.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)

    # Top-left HUD badge
    fig.text(0.04, 0.94, subtitle, fontsize=9, color='#38bdf8', weight='semibold',
             fontfamily='sans-serif')
    fig.text(0.04, 0.89, title, fontsize=20, color='#f8fafc', weight='bold', fontfamily='sans-serif')
    fig.text(0.04, 0.85, f"PART NO: {part_number}  |  SPEC: {material_spec}",
             fontsize=9.5, color='#94a3b8', fontfamily='monospace')

    # Bottom-right CAD stamp
    fig.text(0.96, 0.06, "REVERSE ENGINEERING & 3D MODELING",
             fontsize=8.5, color='#64748b', weight='semibold', ha='right', fontfamily='sans-serif')
    fig.text(0.96, 0.035, "Emerson B. J.  |  Autodesk Inventor & Python AP214 Pipeline",
             fontsize=9, color='#38bdf8', weight='bold', ha='right', fontfamily='sans-serif')

    # Bottom-left GD&T badge
    fig.text(0.04, 0.045, f"BBOX: {max_b[0]-min_b[0]:.1f} × {max_b[1]-min_b[1]:.1f} × {max_b[2]-min_b[2]:.1f} mm  •  SOLID ISOMETRIC",
             fontsize=8, color='#64748b', fontfamily='monospace')

    plt.savefig(output_png, facecolor=fig.get_facecolor(), bbox_inches='tight', pad_inches=0.1, dpi=dpi)
    plt.close()
    print(f"Render saved: {output_png} ({os.path.getsize(output_png)} bytes)")

if __name__ == "__main__":
    assets_dir = r"D:\NASA_CAD_Reverse_Engineering\assets"
    
    # 1. Chamber Insert
    render_cad_model(
        os.path.join(assets_dir, "chamber_insert.glb"),
        os.path.join(assets_dir, "render_chamber_insert_iso.png"),
        title="Chamber Insert Assembly (CIR Insert)",
        part_number="S1101MFA0003 REV C",
        material_spec="6061-T6 Al / 316L SS / Inconel 625",
        base_color=(0.30, 0.68, 0.98), # Titanium blue
        elev=24,
        azim=-50
    )

    # 2. Experiment Mounting Structure (EMS)
    render_cad_model(
        os.path.join(assets_dir, "ems_structure.glb"),
        os.path.join(assets_dir, "render_ems_structure_iso.png"),
        title="Experiment Mounting Structure (EMS Cage)",
        part_number="S1101MFA1000 REV B",
        material_spec="Aluminium 6061-T6 / Anodized Hardcoat",
        base_color=(0.35, 0.75, 0.88), # Aero cyan
        elev=22,
        azim=-45
    )

    # 3. Motorized Igniter Subsystem
    render_cad_model(
        os.path.join(assets_dir, "igniter.glb"),
        os.path.join(assets_dir, "render_igniter_assembly_iso.png"),
        title="Articulated Igniter Actuator & Arm Assembly",
        part_number="S1101MFA1300 REV D",
        material_spec="Inconel 625 / Kanthal A-1 / 303 SS",
        base_color=(0.95, 0.60, 0.25), # Aerospace Amber/Gold
        elev=28,
        azim=-65
    )

    # 4. Coflow Burner Collar & Base
    render_cad_model(
        os.path.join(assets_dir, "burner_collar.glb"),
        os.path.join(assets_dir, "render_burner_collar_iso.png"),
        title="Coflow Diffusion Burner Collar",
        part_number="S1101MFD1268 REV C",
        material_spec="316L Stainless Steel / Sintered Bronze",
        base_color=(0.85, 0.45, 0.40), # Copper / Bronze
        elev=30,
        azim=40
    )

    # 5. Thermocouple Rake Array
    render_cad_model(
        os.path.join(assets_dir, "thermal_rake_1606.glb"),
        os.path.join(assets_dir, "render_thermal_rake_iso.png"),
        title="Thermocouple Far Rake Sensor Array",
        part_number="S1101MFA1606 REV A",
        material_spec="Alumina Ceramic / Type-K Thermocouple",
        base_color=(0.40, 0.85, 0.55), # Emerald Green / Sensor
        elev=25,
        azim=-40
    )
