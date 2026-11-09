"""
NASA ACME Flight Hardware — Automated Parametric CAD Modeling & STEP AP214 Export
---------------------------------------------------------------------------------
Automated procedural generation of axisymmetric and rotational flight hardware
components using the Autodesk Inventor COM API (Python win32com).

Author: Emerson B. J. (Lead CAD & Aerospace Mechanical Engineer)
Framework: NASA ACME s-Flame Research / Hybrid CAD Synthesis
"""

import sys
import os
import math

try:
    import win32com.client
    from win32com.client import constants
except ImportError:
    print("[WARNING] pywin32 not installed. Run: pip install pywin32")

class InventorCADAutomation:
    """Automates Autodesk Inventor session, parametric modeling, and multi-format export."""
    
    def __init__(self, visible=True):
        self.app = None
        self.visible = visible
        self.connect()

    def connect(self):
        """Connects to active Autodesk Inventor instance or starts a new session."""
        try:
            self.app = win32com.client.GetActiveObject("Inventor.Application")
            print("[INFO] Successfully connected to active Autodesk Inventor session.")
        except Exception:
            try:
                self.app = win32com.client.Dispatch("Inventor.Application")
                self.app.Visible = self.visible
                print("[INFO] Started new Autodesk Inventor session.")
            except Exception as e:
                print(f"[ERROR] Could not start Autodesk Inventor: {e}")
                self.app = None

    def create_support_tube(self, part_number, outer_diameter_mm, wall_thickness_mm, length_mm, export_dir):
        """
        Generates precision burner support tube according to NASA MFD specification.
        Example: S1101MFD1270 (OD=1.80mm, deviation ACME-DEV-031).
        """
        if not self.app:
            print("[ERROR] Inventor application not available.")
            return None

        # Inventor native units are centimeters
        od_cm = outer_diameter_mm / 10.0
        wall_cm = wall_thickness_mm / 10.0
        id_cm = od_cm - 2.0 * wall_cm
        len_cm = length_mm / 10.0

        # Create Part Document
        part_doc = self.app.Documents.Add(12290)  # kPartDocumentObject = 12290
        comp_def = part_doc.ComponentDefinition
        trans_geom = self.app.TransientGeometry

        # Select XY Work Plane (WorkPlanes Item 3)
        xy_plane = comp_def.WorkPlanes.Item(3)
        sketch = comp_def.Sketches.Add(xy_plane)

        # Draw concentric circles
        origin = trans_geom.CreatePoint2d(0, 0)
        c_outer = sketch.SketchCircles.AddByCenterRadius(origin, od_cm / 2.0)
        c_inner = sketch.SketchCircles.AddByCenterRadius(origin, id_cm / 2.0)

        # Create Profile
        profile = sketch.Profiles.AddForSolid()

        # Extrude tube
        extrude_def = comp_def.Features.ExtrudeFeatures.CreateExtrudeDefinition(
            profile, 20481  # kJoinOperation = 20481
        )
        extrude_def.SetDistanceExtent(len_cm, 20993)  # kPositiveExtentDirection = 20993
        extrude_feat = comp_def.Features.ExtrudeFeatures.Add(extrude_def)

        # Set aerospace material (Stainless Steel 316L)
        try:
            part_doc.ActiveMaterial = "Stainless Steel"
        except Exception:
            pass

        # Save IPT and export STEP AP214
        os.makedirs(export_dir, exist_ok=True)
        ipt_path = os.path.join(export_dir, f"{part_number}.ipt")
        stp_path = os.path.join(export_dir, f"{part_number}.step")

        part_doc.SaveAs(ipt_path, False)
        part_doc.SaveAs(stp_path, True)  # True = SaveCopyAs
        print(f"[SUCCESS] Generated: {ipt_path} and {stp_path}")

        part_doc.Close(True)
        return stp_path

if __name__ == "__main__":
    print("Inventor CAD Automation Module loaded.")

