import bpy
import os
from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        UIList,
        )
from bpy.props import (
        BoolProperty,
        FloatProperty,
        IntProperty,
        PointerProperty,
        StringProperty,
        CollectionProperty,
        EnumProperty,
        )

class Particle_Painter_Scene_Props(PropertyGroup):
    library_enum: EnumProperty(name="Library Tabs",
                               items=[('OPTION1',"Option 1","Example Enum"),
                                      ('OPTION2',"Option 2","Example Enum"),
                                      ('OPTION3',"Option 3","Example Enum")],
                               default='OPTION1')

    active_category: StringProperty(name="Active Category",default="")

    @classmethod
    def register(cls):
        bpy.types.Scene.particle_painter = PointerProperty(
            name="Particle Painter Props",
            description="Particle Painter Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Scene.particle_painter

classes = (
    Particle_Painter_Scene_Props,
)

register, unregister = bpy.utils.register_classes_factory(classes)        