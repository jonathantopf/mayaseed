import pymel.core as pm
import maya.cmds as cmds
from functools import partial
import ms_export


ENTITY_TYPES = ['object_instance', 'light', 'edf']


class AEms_renderSettingsTemplate(pm.uitypes.AETemplate):
        def __init__(self, node):

                self.beginScrollLayout()

                self.callCustom(self.toolbar_create, self.toolbar_edit, 'render_toolbar')


                self.beginLayout('Export Settings', collapse=False)

                self.callCustom(self.output_directory_create, self.populate_render_layer_layout, 'output_directory')
                self.addControl('output_file')

                self.addControl('convert_shading_nodes_to_textures')
                self.addSeparator()
                self.addControl('convert_textures_to_exr')
                self.addSeparator()
                self.addControl('overwrite_existing_textures')
                self.addSeparator()
                self.addControl('overwrite_existing_geometry')

                self.endLayout()

                self.beginLayout('Render Layers')
                self.callCustom(self.render_layer_create_layout, self.populate_render_layer_layout, 'render_layers')
                self.endLayout()

                self.addExtraControls()

                self.endScrollLayout()


        def get_file_dir(self, *attr):
            file_name = cmds.fileDialog2(fm=3, cap='Select directory', okc='Select')
            if file_name is not None:
                cmds.setAttr(attr[0], file_name[0], type='string')

        def output_directory_create(self, attr):
            cmds.rowLayout(nc=3)
            cmds.text(label='Output Directory')
            self.output_dir_text_field = cmds.textField(fileName=cmds.getAttr(attr))
            self.output_dir_button = cmds.button(' Select directory ', c=partial(self.get_file_dir, attr))

        def output_directory_update(self, attr):
            cmds.textField(self.output_dir_text_field, edit=True, fileName=cmds.getAttr(attr))
            cmds.button(self.output_dir_button, edit=True, c=partial(self.get_file_dir, attr))


        def render_layer_create_layout(self, args):
            self.render_layer_layout_widths = [130, 120, 130, 50, 30]
            render_layer_label_layout = cmds.rowLayout('render_layer_label_layout', nc=5, cal=[1, 'left'])
            for i, width in enumerate(self.render_layer_layout_widths):
                cmds.rowLayout(render_layer_label_layout, e=True, cw=[i + 1, width])
            cmds.text('name')
            cmds.text('entity type')
            cmds.text('rule')
            cmds.text('order')
            cmds.text(' - ')
            cmds.setParent('..')
            self.render_layer_layout = cmds.columnLayout('render_layer_layout')
            cmds.setParent('..')
            cmds.rowLayout(nc=3)
            cmds.button(' + ', command=partial(self.add_render_layer, args))

            self.populate_render_layer_layout(args)


        def add_render_layer(self, attr, name=None, model=None, rule=None, entity_type=None, refresh=False):
            node = attr.split('.')[0]

            i = 0

            while True:
                i += 1
                if i > 50:
                    break
                layer_name = 'render_layer_{0}_name'.format(i)  
            
                if not cmds.attributeQuery(layer_name, exists=True, node=node):

                    cmds.addAttr(node, longName='render_layer_{0}_name'.format(i), dt="string")
                    if name is not None:
                        cmds.setAttr(node + '.render_layer_{0}_name'.format(i), name, type='string')
                    cmds.addAttr(node, longName='render_layer_{0}_model'.format(i), dt="string")
                    if model is not None:
                        cmds.setAttr(node + '.render_layer_{0}_model'.format(i), model, type='string')
                    cmds.addAttr(node, longName='render_layer_{0}_rule'.format(i), dt="string")
                    if rule is not None:
                        cmds.setAttr(node + '.render_layer_{0}_rule'.format(i), rule, type='string')
                    if entity_type is not None:
                        cmds.setAttr(node + '.render_layer_{0}_type'.format(i), entity_type, type='string')
                    cmds.addAttr(node, longName='render_layer_{0}_type'.format(i), dt="string")

                    cmds.addAttr(node, longName='render_layer_{0}_order'.format(i), at="short")

                    if refresh:
                        self.populate_render_layer_layout(attr)

                    break


        def populate_render_layer_layout(self, attr): # here we pass the attribute rather than the node name so we can re use this finction id the call custom menu

            node = attr.split('.')[0]  

            # delete old ui
            children = cmds.columnLayout(self.render_layer_layout, q=True, childArray=True)
            if children is not None:
                for name in children:
                    cmds.deleteUI(name)

            i = 0

            while True:
                i += 1


                if i > 50:
                    break
                layer_name = 'render_layer_{0}_name'.format(i)

                if cmds.attributeQuery(layer_name, exists=True, node=node):

                    cmds.setParent(self.render_layer_layout)

                    current_render_layer_layout = cmds.rowLayout(nc=5)
            
                    for n, width in enumerate(self.render_layer_layout_widths):
                        cmds.rowLayout(current_render_layer_layout, e=True, cw=[n + 1, width])

                    cmds.textField()
                    entity_type_menu = cmds.optionMenu()
                    for entity_type in ENTITY_TYPES:
                        cmds.menuItem(label=entity_type)
                    rule_text_field = cmds.textField()
                    cmds.intField(v=1)
                    cmds.button(' - ', height=20)


        def toolbar_create(self, args):
            cmds.button('Export', bgc=[0, 0.7, 1], command=self.render)         
            cmds.button('Refresh attribute editor', command=self.refresh_editor)
            

        def toolbar_edit(self, args):
            pass


        def refresh_editor(self, args):
            cmds.refreshEditorTemplates()


        def render(self, args):
            node = cmds.ls(sl=True)
            ms_export.export(node[0])



            
