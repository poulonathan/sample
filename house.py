import bpy
from math import radians

# Configurable parameters
roof_slope = 0.5
house_width = 10
house_depth = 8
house_height = 6
roof_overhang = 0.5

# Remove default objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create walls
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(0,0,0))
bpy.ops.transform.resize(value=(house_width, house_depth, house_height))
bpy.ops.transform.translate(value=(0,0,house_height/2))

# Create roof
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(0,0,house_height+roof_overhang))
bpy.ops.transform.resize(value=(house_width, house_depth, 0.1))
bpy.ops.transform.translate(value=(0,0,-roof_overhang/2))
bpy.ops.transform.rotate(value=radians(45), orient_axis='X')

# Create roof slope
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(0,0,house_height+roof_overhang))
bpy.ops.transform.resize(value=(house_width, house_depth, 0.1))
bpy.ops.transform.translate(value=(0,0,-roof_overhang/2))
bpy.ops.transform.rotate(value=radians(-45*roof_slope), orient_axis='X')
bpy.ops.transform.translate(value=(0,0,roof_slope*house_height))

# Set materials
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['Cube'].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects['Cube']
bpy.ops.material.new()
bpy.context.object.active_material.diffuse_color = (0.8, 0.8, 0.8)
bpy.ops.object.material_slot_add()
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=radians(66), island_margin=0.02)
bpy.ops.object.editmode_toggle()

# Set camera and lighting
bpy.ops.object.camera_add(location=(0-house_width,0-house_depth,3*house_height))
bpy.ops.object.light_add(type='SUN', location=(0,0,3*house_height))
bpy.data.worlds['World'].node_tree.nodes['Background'].inputs[0].default_value = (0.1, 0.1, 0.1, 1)

# Render image
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.filepath = "//house.png"
bpy.ops.render.render(write_still=True)
