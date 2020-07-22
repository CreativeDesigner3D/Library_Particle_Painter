import bpy,os,inspect

from bpy.types import (Header, 
                       Menu, 
                       Panel, 
                       Operator,
                       PropertyGroup)

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       PointerProperty,
                       EnumProperty,
                       CollectionProperty)
from . import particle_painter_utils
from .pc_lib import pc_utils

def event_is_place_asset(event):
    if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
        return True
    elif event.type == 'NUMPAD_ENTER' and event.value == 'PRESS':
        return True
    elif event.type == 'RET' and event.value == 'PRESS':
        return True
    else:
        return False

def event_is_cancel_command(event):
    if event.type in {'RIGHTMOUSE', 'ESC'}:
        return True
    else:
        return False

def event_is_pass_through(event):
    if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
        return True
    else:
        return False

class particle_painter_OT_activate(Operator):
    bl_idname = "particle_painter.activate"
    bl_label = "Activate Library"
    bl_options = {'UNDO'}
    
    library_name: StringProperty(name='Library Name')

    def execute(self, context):
        #Code to initalize library goes here
        #This can be left blank
        print('Activate Particle Painter:',self.library_name)
        path = particle_painter_utils.get_library_path()
        pc_utils.update_file_browser_path(context,path)
        return {'FINISHED'}


class particle_painter_OT_drop(Operator):
    bl_idname = "particle_painter.drop"
    bl_label = "Drop File"
    bl_options = {'UNDO'}
    
    filepath: StringProperty(name='Library Name')

    particle_systems = []
    obj = None

    def get_particles(self,context):
        self.particle_systems = []
        path, ext = os.path.splitext(self.filepath)
        filename = os.path.basename(path)
        object_file_path = os.path.join(path + ".blend")
        with bpy.data.libraries.load(object_file_path, False, False) as (data_from, data_to):
            for part in data_from.particles:
                if part == filename:
                    data_to.particles = [part]
                
        for ps in data_to.particles:
            self.particle_systems.append(ps)

    def execute(self, context):
        self.get_particles(context)
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def assign_particle_system(self, context, obj):
        for part in self.particle_systems:
            vgrp = obj.vertex_groups.new(name=part.name)
            mod = obj.modifiers.new(part.name,'PARTICLE_SYSTEM')
            mod.particle_system.settings = part
            mod.particle_system.vertex_group_density = part.name
        
    def finish(self,context):
        context.window.cursor_set('DEFAULT')
        context.view_layer.objects.active = self.obj 
        context.area.tag_redraw()
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT') 
        return {'FINISHED'}

    def modal(self, context, event):
        context.area.tag_redraw()
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y
        selected_point, selected_obj = pc_utils.get_selection_point(context,event,exclude_objects=[])
        bpy.ops.object.select_all(action='DESELECT')
        if selected_obj:
            self.obj = selected_obj
            selected_obj.select_set(True)
            context.view_layer.objects.active = selected_obj

        if event_is_place_asset(event):
            self.assign_particle_system(context,selected_obj)
            return self.finish(context)

        if event_is_cancel_command(event):
            return self.cancel_drop(context)
        
        if event_is_pass_through(event):
            return {'PASS_THROUGH'}        
        
        return {'RUNNING_MODAL'}

def update_particle_paint_name(self,context):
    for i, particle in enumerate(self.particle_systems):
        if particle:
            self.group_name = bpy.data.particles[i].name


class particle_painter_OT_particle_paint(bpy.types.Operator):
    bl_idname = "bp_object.particle_paint"
    bl_label = "Particle Paint"

    particle_systems: bpy.props.BoolVectorProperty(name="Particle Systems", 
                                                    description="Determines if the particle system is set to draw", 
                                                    size=32,
                                                    update=update_particle_paint_name)

    group_name: bpy.props.StringProperty(name="Group Name")

    def check(self, context):
        return True

    @classmethod
    def poll(cls, context):
        if context.object and len(bpy.data.particles) > 0:
            return True
        else:
            return False

    def execute(self, context):
        particle = None
        for i, particle in enumerate(self.particle_systems):
            if particle:
                particle_settings = bpy.data.particles[i]
                
        obj = context.object
        vgrp = obj.vertex_groups.new(name=self.group_name)
        mod = obj.modifiers.new(self.group_name,'PARTICLE_SYSTEM')
        mod.particle_system.settings = particle_settings
        mod.particle_system.vertex_group_density = self.group_name
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT') 
        #GET SELECTED SETTINGS
        #mod.settings = bpy.data.particles[name]
        return {'FINISHED'}
        
    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)
        
    def draw(self, context):
        layout = self.layout
        layout.label(text="Select the Particles to Draw:")
        for i, particle in enumerate(bpy.data.particles):
            row = layout.row()
            row.prop(self,'particle_systems',index=i,text="")
            row.label(text=particle.name)
        layout.prop(self,'group_name',text="Particle Name")


class particle_painter_OT_settings(Operator):
    bl_idname = "particle_painter.settings"
    bl_label = "Settings"
    bl_options = {'UNDO'}
    
    filepath: StringProperty(name='Library Name')

    particle_systems = []
    obj = None

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

classes = (
    particle_painter_OT_activate,
    particle_painter_OT_drop,
    particle_painter_OT_settings
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
