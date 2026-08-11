"""BlackMamba Circuit Simulator — Blender workbench bootstrap.

Non-destructive bootstrap for Blender 4.x.

Goals:
- Keep the user's existing scene untouched.
- Introduce canonical, reusable electronic parts as data-backed assemblies.
- Give every part stable metadata + electrical terminals for future snapping/routing.
- Treat Arduino Leonardo as an assembly container, not a monolithic mesh.
- Export a small JSON component catalog next to the .blend file.

Run from Blender's Scripting workspace with the target .blend open.
"""

from __future__ import annotations

import bpy
import json
from pathlib import Path

BM_VERSION = "0.1.0"
GENERATOR_ID = "blackmamba.workbench.bootstrap"


def mm(value: float) -> float:
    """Convert millimetres to Blender units without changing scene units."""
    unit = bpy.context.scene.unit_settings
    scale_length = unit.scale_length if unit.system != 'NONE' and unit.scale_length > 0 else 1.0
    return (value / 1000.0) / scale_length


def mm_vec(values):
    return tuple(mm(float(v)) for v in values)


def ensure_collection(name: str, parent=None):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        if parent is None:
            bpy.context.scene.collection.children.link(col)
        else:
            parent.children.link(col)
    return col


def unlink_from_all(obj):
    for col in list(obj.users_collection):
        col.objects.unlink(obj)


def link_only(obj, collection):
    unlink_from_all(obj)
    collection.objects.link(obj)


def delete_generated_root(name: str):
    root = bpy.data.objects.get(name)
    if not root or root.get("bm.generated_by") != GENERATOR_ID:
        return
    children = list(root.children_recursive)
    for obj in children:
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.objects.remove(root, do_unlink=True)


def material(name, rgba, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF") if mat.use_nodes else None
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat


def cube(name, dims_mm, loc_mm=(0, 0, 0), mat=None, collection=None, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=mm_vec(loc_mm))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = mm_vec(dims_mm)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    if collection:
        link_only(obj, collection)
    if parent:
        obj.parent = parent
    return obj


def component_root(name, collection, kind, package, terminal_count, location_mm=(0, 0, 0)):
    delete_generated_root(name)
    root = bpy.data.objects.new(name, None)
    root.empty_display_type = 'PLAIN_AXES'
    root.empty_display_size = mm(0.5)
    root.location = mm_vec(location_mm)
    collection.objects.link(root)
    root["bm.generated_by"] = GENERATOR_ID
    root["bm.schema_version"] = BM_VERSION
    root["bm.entity"] = "component_definition"
    root["bm.kind"] = kind
    root["bm.package"] = package
    root["bm.units"] = "mm"
    root["bm.terminal_count"] = terminal_count
    root["bm.canonical"] = True
    return root


def terminal(root, number, local_mm, role="passive", polarity="none"):
    obj = bpy.data.objects.new(f"{root.name}__PIN_{number}", None)
    obj.empty_display_type = 'SPHERE'
    obj.empty_display_size = mm(0.18)
    root.users_collection[0].objects.link(obj)
    obj.parent = root
    obj.location = mm_vec(local_mm)
    obj["bm.entity"] = "terminal"
    obj["bm.pin"] = str(number)
    obj["bm.role"] = role
    obj["bm.polarity"] = polarity
    obj["bm.snap_class"] = "electrical_terminal"
    return obj


def set_local(obj, x_mm, y_mm, z_mm):
    obj.location = mm_vec((x_mm, y_mm, z_mm))


MAT_TERM = material("BM_Metal_Terminal", (0.62, 0.64, 0.66, 1.0), metallic=0.88, roughness=0.28)
MAT_RES_BODY = material("BM_Resistor_Body", (0.055, 0.055, 0.055, 1.0), metallic=0.05, roughness=0.82)
MAT_CAP_BODY = material("BM_Ceramic_Tan", (0.56, 0.37, 0.18, 1.0), metallic=0.0, roughness=0.88)
MAT_LED_BODY = material("BM_LED_Lens", (0.22, 0.55, 0.23, 1.0), metallic=0.0, roughness=0.28)
MAT_HEADER = material("BM_Header_Black", (0.02, 0.02, 0.02, 1.0), metallic=0.0, roughness=0.76)
MAT_PIN_GOLD = material("BM_Pin_Gold", (0.65, 0.42, 0.12, 1.0), metallic=0.82, roughness=0.26)


def make_resistor_0805(collection, location_mm=(0, 0, 0)):
    root = component_root("BM_R_0805", collection, "resistor", "0805", 2, location_mm)
    cube("BM_R_0805__BODY", (1.40, 1.25, 0.60), mat=MAT_RES_BODY, collection=collection, parent=root)
    left = cube("BM_R_0805__TERM_1", (0.30, 1.25, 0.60), mat=MAT_TERM, collection=collection, parent=root)
    right = cube("BM_R_0805__TERM_2", (0.30, 1.25, 0.60), mat=MAT_TERM, collection=collection, parent=root)
    set_local(left, -0.85, 0, 0)
    set_local(right, 0.85, 0, 0)
    terminal(root, 1, (-1.00, 0, 0), role="passive")
    terminal(root, 2, (1.00, 0, 0), role="passive")
    root["bm.dimensions_mm"] = "2.00,1.25,0.60"
    root["bm.rotation_step_deg"] = 90
    root["bm.polarized"] = False
    return root


def make_capacitor_0805(collection, location_mm=(4, 0, 0)):
    root = component_root("BM_C_0805", collection, "capacitor", "0805", 2, location_mm)
    cube("BM_C_0805__BODY", (1.40, 1.25, 0.80), mat=MAT_CAP_BODY, collection=collection, parent=root)
    left = cube("BM_C_0805__TERM_1", (0.30, 1.25, 0.80), mat=MAT_TERM, collection=collection, parent=root)
    right = cube("BM_C_0805__TERM_2", (0.30, 1.25, 0.80), mat=MAT_TERM, collection=collection, parent=root)
    set_local(left, -0.85, 0, 0)
    set_local(right, 0.85, 0, 0)
    terminal(root, 1, (-1.00, 0, 0), role="passive")
    terminal(root, 2, (1.00, 0, 0), role="passive")
    root["bm.dimensions_mm"] = "2.00,1.25,0.80"
    root["bm.rotation_step_deg"] = 90
    root["bm.polarized"] = False
    root["bm.dielectric_class"] = "generic_mlcc"
    return root


def make_led_0805(collection, location_mm=(8, 0, 0)):
    root = component_root("BM_LED_0805", collection, "led", "0805", 2, location_mm)
    cube("BM_LED_0805__BODY", (1.40, 1.25, 0.75), mat=MAT_LED_BODY, collection=collection, parent=root)
    cube("BM_LED_0805__ANODE", (0.30, 1.25, 0.35), loc_mm=(-0.85, 0, -0.20), mat=MAT_TERM, collection=collection, parent=root)
    cube("BM_LED_0805__CATHODE", (0.30, 1.25, 0.35), loc_mm=(0.85, 0, -0.20), mat=MAT_TERM, collection=collection, parent=root)
    terminal(root, "A", (-1.00, 0, 0), role="anode", polarity="positive")
    terminal(root, "K", (1.00, 0, 0), role="cathode", polarity="negative")
    root["bm.dimensions_mm"] = "2.00,1.25,0.75"
    root["bm.rotation_step_deg"] = 90
    root["bm.polarized"] = True
    return root


def make_header_1x8(collection, location_mm=(14, 0, 0), pins=8):
    pitch = 2.54
    length = pitch * pins
    root = component_root("BM_HEADER_1x8_2P54", collection, "header", "1x8_2.54mm", pins, location_mm)
    cube("BM_HEADER_1x8_2P54__HOUSING", (length, 2.54, 2.50), mat=MAT_HEADER, collection=collection, parent=root)
    start_x = -((pins - 1) * pitch) / 2.0
    for i in range(pins):
        x = start_x + i * pitch
        cube(f"BM_HEADER_1x8_2P54__PINMESH_{i+1}", (0.64, 0.64, 11.5), loc_mm=(x, 0, 0), mat=MAT_PIN_GOLD, collection=collection, parent=root)
        terminal(root, i + 1, (x, 0, -5.75), role="header_pin")
    root["bm.pitch_mm"] = pitch
    root["bm.rotation_step_deg"] = 90
    root["bm.keyed"] = False
    return root


def ensure_leonardo_assembly(collection):
    name = "ARDUINO_LEONARDO__ASSEMBLY"
    obj = bpy.data.objects.get(name)
    if obj is None:
        obj = bpy.data.objects.new(name, None)
        obj.empty_display_type = 'CUBE'
        obj.empty_display_size = mm(4.0)
        collection.objects.link(obj)
    obj["bm.entity"] = "assembly"
    obj["bm.assembly_type"] = "arduino_leonardo"
    obj["bm.status"] = "capture_in_progress"
    obj["bm.truth_model"] = "composition_plus_rules"
    obj["bm.rule_set"] = "arduino_leonardo_v0.1"
    obj["bm.routing_model"] = "net_classes"
    obj["bm.flow_visualization"] = "enabled_future"
    return obj


def catalog_payload():
    return {
        "catalog_version": BM_VERSION,
        "units": "mm",
        "architecture": "component_definitions + assembly_instances + rules + nets",
        "packages": {
            "R_0805": {"kind": "resistor", "package": "0805", "dimensions_mm": [2.00, 1.25, 0.60], "terminals": ["1", "2"], "polarized": False},
            "C_0805": {"kind": "capacitor", "package": "0805", "dimensions_mm": [2.00, 1.25, 0.80], "terminals": ["1", "2"], "polarized": False, "family": "generic_mlcc"},
            "LED_0805": {"kind": "led", "package": "0805", "dimensions_mm": [2.00, 1.25, 0.75], "terminals": ["A", "K"], "polarized": True},
            "HEADER_1x8_2P54": {"kind": "header", "package": "1x8_2.54mm", "pitch_mm": 2.54, "pins": 8},
        },
        "rules": {
            "placement": {"canonical_rotation_step_deg": 90, "component_origins": "package_center", "terminal_empties": "authoritative_snap_points"},
            "routing": {"principle": "nets carry rules; geometry must satisfy the net class", "future_classes": ["POWER", "GND", "ANALOG", "GPIO", "PWM", "I2C", "SPI", "UART", "USB_DIFF"]},
            "assembly": {"principle": "Leonardo is composed from reusable components; never store it as one closed mesh"}
        }
    }


def write_catalog():
    blend_path = Path(bpy.data.filepath) if bpy.data.filepath else None
    out_dir = blend_path.parent if blend_path else Path.home()
    out = out_dir / "blackmamba_component_catalog.json"
    out.write_text(json.dumps(catalog_payload(), indent=2), encoding="utf-8")
    print(f"[BlackMamba] catalog exported: {out}")
    return out


def ensure_readme_text():
    text = bpy.data.texts.get("BLACKMAMBA_WORKBENCH_README") or bpy.data.texts.new("BLACKMAMBA_WORKBENCH_README")
    text.clear()
    text.write(
        "BlackMamba Circuit Simulator Workbench v0.1\n"
        "=============================================\n"
        "The Leonardo is an assembly, not a monolithic object.\n"
        "Canonical parts live under BM_LIBRARY. Electrical terminals are child empties.\n"
        "Future routing/simulation will consume terminal IDs + net rules, while Blender remains the visual/mechanical view.\n"
        "Existing user geometry is intentionally untouched by this bootstrap.\n"
    )


def main():
    root = ensure_collection("BLACKMAMBA")
    library = ensure_collection("BM_LIBRARY", parent=root)
    assemblies = ensure_collection("BM_ASSEMBLIES", parent=root)
    ensure_collection("BM_RULE_DEBUG", parent=root)

    make_resistor_0805(library, (0, 0, 0))
    make_capacitor_0805(library, (4, 0, 0))
    make_led_0805(library, (8, 0, 0))
    make_header_1x8(library, (20, 0, 0), pins=8)
    ensure_leonardo_assembly(assemblies)
    ensure_readme_text()
    write_catalog()

    bpy.context.scene["bm.workbench_version"] = BM_VERSION
    bpy.context.scene["bm.architecture"] = "parts+rules+nets+assemblies"
    print("[BlackMamba] workbench bootstrap complete. Existing scene preserved.")


if __name__ == "__main__":
    main()
