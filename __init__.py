import bpy
from .pc_lib import pc_utils
from . import particle_painter_ops
from . import particle_painter_props
from . import particle_painter_ui
from bpy.app.handlers import persistent

#Standard bl_info for Blender Add-ons
bl_info = {
    "name": "Particle Painter",
    "author": "Andrew Peel",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Asset Library",
    "description": "This is an asset library that allows users to maintain their own particles and paint them onto objects",
    "warning": "",
    "wiki_url": "",
    "category": "Asset Library",
}

@persistent
def load_library_on_file_load(scene=None):
    pc_utils.register_library(name="Particle Painter",
                              activate_id='particle_painter.activate',
                              drop_id='particle_painter.drop',
                              icon='SHADERFX')

#Standard register/unregister Function for Blender Add-ons
def register():
    particle_painter_ops.register()
    particle_painter_props.register()
    particle_painter_ui.register()

    bpy.app.handlers.load_post.append(load_library_on_file_load)
    load_library_on_file_load()

def unregister():
    particle_painter_ops.unregister()
    particle_painter_props.unregister()
    particle_painter_ui.unregister()

    bpy.app.handlers.load_post.remove(load_library_on_file_load)  

    pc_utils.unregister_library("Particle Painter")

