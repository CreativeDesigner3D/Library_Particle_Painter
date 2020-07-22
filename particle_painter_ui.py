import bpy
import os
from .pc_lib import pc_utils

class FILEBROWSER_PT_particle_painter_headers(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'UI'
    bl_label = "Library"
    bl_category = "Attributes"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        #Only display when active and File Browser is not open as separate window
        if len(context.area.spaces) > 1:
            pyclone = pc_utils.get_scene_props(context.scene)
            if pyclone.active_library_name == 'Particle Painter':
                return True   
        return False

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.scale_y = 1.3
        row.label(text="Particle Painter")
        if context.object and context.object.mode != 'OBJECT':
            row = layout.row()
            row.scale_y = 1.3
            row.operator('particle_painter.settings',text="Finish Painting",icon='SETTINGS')     
        else:
            row = layout.row()
            row.scale_y = 1.3
            row.operator('particle_painter.settings',text="Settings",icon='PANEL_CLOSE')                    

classes = (
    FILEBROWSER_PT_particle_painter_headers,
)

register, unregister = bpy.utils.register_classes_factory(classes)                