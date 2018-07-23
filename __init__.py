'''
Copyright (C) 2017 MACHIN3, machin3.io, support@machin3.io

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''


bl_info = {
    "name": "MACHIN3tools",
    "author": "MACHIN3",
    "version": (0, 3),
    "blender": (2, 80, 0),
    "location": "",
    "description": "A collection of blender python scripts.",
    "warning": "",
    "wiki_url": "https://github.com/machin3io/MACHIN3tools",
    "category": "Mesh"}


import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty, CollectionProperty
from bpy.utils import register_class, unregister_class
from . properties import AppendMatsCollection, AppendMatsUIList
from . utils import MACHIN3 as m3



# TODO: add automatic custom blender keymaps option
# TODO: OSD feedback, so you dont have to check into the op props to verify a tool did what you want it to do


class MACHIN3Settings(bpy.types.PropertyGroup):
    debugmode = BoolProperty(name="Debug Mode", default=False)

    pieobjecteditmodehide = BoolProperty(name="Auto Hide", default=False)
    pieobjecteditmodeshow = BoolProperty(name="Auto Reveal", default=False)
    pieobjecteditmodeshowunselect = BoolProperty(name="Unselect", default=False)
    pieobjecteditmodetoggleao = BoolProperty(name="Toggle AO", default=False)

    pieviewsalignactive = bpy.props.BoolProperty(name="Align Active", default=False)

    preview_percentage = IntProperty(name="Preview Percentage", default=100, min=10, max=100, subtype="PERCENTAGE")
    final_percentage = IntProperty(name="Final Percentage", default=250, min=100, max=1000, subtype="PERCENTAGE")

    preview_samples = IntProperty(name="Preview Percentage", default=32, min=12, max=64)
    final_samples = IntProperty(name="Final Percentage", default=256, min=64, max=2048)



preferences_tabs = [("MODULES", "Modules", ""),
                    ("SPECIALMENUS", "Special Menus", ""),
                    ("PIEMENUS", "Pie Menus", ""),
                    ("CUSTOMKEYS", "Custom Keys", "")]




class MACHIN3toolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    M3path = __path__[0]

    appendworldpath: StringProperty(name="Append World from", subtype='FILE_PATH')
    appendworldname: StringProperty()

    appendmatspath: StringProperty(name="Append Materials from", subtype='FILE_PATH')
    appendmats: CollectionProperty(type=AppendMatsCollection)
    appendmatsIDX: IntProperty()
    appendmatsname: StringProperty()

    # TABS

    # tabs = EnumProperty(name="Tabs", items=preferences_tabs, default="MODULES")

    def draw(self, context):
        layout=self.layout

        # wm = bpy.context.window_manager
        # kc = wm.keyconfigs.user


        # column = layout.column(align=True)
        # row = column.row()
        # row.prop(self, "tabs", expand=True)

        # box = column.box()


        # if self.tabs == "MODULES":
            # self.draw_modules(box, kc)
        # elif self.tabs == "SPECIALMENUS":
            # self.draw_special(box, kc)
        # elif self.tabs == "PIEMENUS":
            # self.draw_pies(box, kc)


        box = layout.box()

        column = box.column()

        column.prop(self, "appendworldpath")
        column.prop(self, "appendworldname")
        column.separator()

        column.prop(self, "appendmatspath")

        row = column.row()
        rows = len(self.appendmats) if len(self.appendmats) > 6 else 6
        row.template_list("AppendMatsUIList", "", self, "appendmats", self, "appendmatsIDX", rows=rows)

        c = row.column(align=True)
        c.operator("machin3.move_appendmat", text="", icon="TRIA_UP").direction = "UP"
        c.operator("machin3.move_appendmat", text="", icon="TRIA_DOWN").direction = "DOWN"

        c.separator()
        c.separator()
        c.operator("machin3.rename_appendmat", text="", icon="OUTLINER_DATA_FONT")
        c.separator()
        c.separator()
        c.operator("machin3.clear_appendmats", text="", icon="LOOP_BACK")
        c.operator("machin3.remove_appendmat", text="", icon="CANCEL")

        row = column.row()
        row.prop(self, "appendmatsname")
        row.operator("machin3.add_appendmat", text="", icon="ZOOMIN")


def register_pie_keys(wm, keymaps):
    # SELECT MODE

    km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_MACHIN3_select_modes"
    kmi.active = True
    keymaps.append((km, kmi))

    # CHANGE SHADING

    km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'PAGE_UP', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_MACHIN3_change_shading"
    kmi.active = True
    keymaps.append((km, kmi))

    # VIEWS and CAMS

    km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'PAGE_DOWN', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_MACHIN3_views_and_cams"
    kmi.active = True
    keymaps.append((km, kmi))

    # SAVE, OPEN, APPEND

    km = wm.keyconfigs.addon.keymaps.new(name='Window')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'PRESS', ctrl=True)
    kmi.properties.name = "VIEW3D_MT_MACHIN3_save_open_append"
    kmi.active = True
    keymaps.append((km, kmi))


    # Switch Workspace

    km = wm.keyconfigs.addon.keymaps.new(name='Window')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'PAUSE', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_MACHIN3_switch_workspace"
    kmi.active = True
    keymaps.append((km, kmi))





def get_classes():
    from . ui.pie import PieSelectMode, PieChangeShading, PieViewsAndCams, PieSaveOpenAppend, PieSwitchWorkspace
    from . ui.menu import MenuAppendMaterials
    from . ui.operators.select_mode import ToggleEditMode, SelectVertexMode, SelectEdgeMode, SelectFaceMode
    from . ui.operators.change_shading import ShadeSolid, ShadeMaterial, ShadeRendered
    from . ui.operators.toggle_grid_wire_outline import ToggleGrid, ToggleWireframe, ToggleOutline
    from . ui.operators.shade_smooth_flat import ShadeSmooth, ShadeFlat
    from . ui.operators.colorize_materials import ColorizeMaterials
    from . ui.operators.views_and_cams import ViewAxis, MakeCamActive, SmartViewCam
    from . ui.operators.save_load_append import Save, SaveIncremental, LoadMostRecent
    from . ui.operators.save_load_append import AppendWorld, AppendMaterial, LoadWorldSource, LoadMaterialsSource
    from . ui.operators.appendmats import Add, Move, Rename, Clear, Remove
    from . ui.operators.switch_workspace import SwitchWorkspace

    classes = []

    # ui lists
    classes.append(AppendMatsUIList)

    # collections and property groups
    classes.append(AppendMatsCollection)

    # addon preferences
    classes.append(MACHIN3toolsPreferences)


    # menus and their operators

    # SELECT MODE
    classes.append(PieSelectMode)
    classes.append(SelectVertexMode)
    classes.append(SelectEdgeMode)
    classes.append(SelectFaceMode)
    classes.append(ToggleEditMode)

    # CHANGE SHADING
    classes.append(PieChangeShading)
    classes.extend([ShadeSolid, ShadeMaterial, ShadeRendered])
    classes.extend([ToggleGrid, ToggleWireframe, ToggleOutline])
    classes.extend([ShadeSmooth, ShadeFlat])
    classes.append(ColorizeMaterials)

    # VIEWS and CAMS
    classes.append(PieViewsAndCams)
    classes.extend([ViewAxis, MakeCamActive, SmartViewCam])

    # SAVE, OPEN, Append
    classes.append(PieSaveOpenAppend)
    classes.append(MenuAppendMaterials)
    classes.extend([Save, SaveIncremental, LoadMostRecent])
    classes.extend([AppendWorld, AppendMaterial, LoadWorldSource, LoadMaterialsSource])
    classes.extend([Add, Move, Rename, Clear, Remove])

    # SWITCH WORKSPACE
    classes.append(PieSwitchWorkspace)
    classes.append(SwitchWorkspace)

    return classes


keymaps = []
classes = get_classes()


def register():
    # CLASSES
    for c in classes:
        register_class(c)

    wm = bpy.context.window_manager

    # PIE MENUS  KEYS

    register_pie_keys(wm, keymaps)


def unregister():
    # CLASSES
    for c in classes:
        unregister_class(c)


    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)

    keymaps.clear()
