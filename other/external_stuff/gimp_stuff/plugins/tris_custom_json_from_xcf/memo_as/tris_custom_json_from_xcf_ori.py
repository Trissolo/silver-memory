#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   GIMP - The GNU Image Manipulation Program
#   Copyright (C) 1995 Spencer Kimball and Peter Mattis
#
#   *** Based on: ***
#   https://testing.docs.gimp.org/3.0/en/gimp-using-python-plug-in-tutorial.html
#   gimp-tutorial-plug-in.py
#   sample plug-in to illustrate the Python plug-in writing tutorial
#   Copyright (C) 2023 Jacob Boerema
#
#   (ensure the script is executable)

# just for sys.argv
import sys

import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Glib is used mostly for GLib.Error()
# or utility functions like:
# GLib.build_pathv(GLib.DIR_SEPARATOR_S, [GLib.get_home_dir(), "my_file_name.txt"])
from gi.repository import GLib

# GObject is for GObject.ParamFlags:
# G_PARAM_READABLE: 1
# G_PARAM_WRITABLE: 2
# G_PARAM_READWRITE: 3 # -> Alias for: G_PARAM_READABLE | G_PARAM_WRITABLE
from gi.repository import GObject

# I/O and files, e.g., new_file = Gio.File.new_for_path("/home/USER/Graphics/my_picture.xcf")
#from gi.repository import Gio


# other custom imports
import json
#import os


# constants:
#class CONSTS:
#    FILE_NAME = GLib.path_get_basename(__file__).removesuffix(".py")


# our plugin class
class AdventureGameNook(Gimp.PlugIn):
    # procedure(s) name in Procedure Browser. Note that this string value CANNOT have underscores, only hyphens/dashes
    def do_query_procedures(self):
        return ["tris-custom-json-from-xcf"]


    def do_set_i18n(self, name):
        return False


    # The ImageProcedure (mostly hardcoded strings)
    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None
        )

        procedure.set_image_types("*")

        procedure.set_menu_label("[Tris] 🔩🌺 Room Editor and JSON generator")

        procedure.add_menu_path("<Image>/Filters/[[Tris]]/")

        procedure.set_documentation(
            "[Tris] Basically, a Room editor for adventure games.",
            "A complex plugin (GIMP 3.0). WIP",
            name,
        )

        procedure.set_attribution("Tris", "---", "2025")

        return procedure


    def procedure_is_complete(self, prcdr):
        #Gimp.PDBStatusType
        #       .EXECUTION_ERROR # == 0
        #       .CALLING_ERROR # == 1
        #       .PASS_THROUGH # Pass through == 2
        #       .SUCCESS # Success == 3
        #       .CANCEL # User cancel == 4
        print("** Json procedure complete! :D **")
        return prcdr.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
    
    
    # load json
    def get_gamedata_from_json_file(self):
        my_path = GLib.build_pathv(GLib.DIR_SEPARATOR_S, [GLib.path_get_dirname(__file__), "gamedata.json"])   
        data = None
        with open(my_path) as json_file:
            data = json.load(json_file)

            # Test: Print the data of dictionary
            #print("\nTop level content:", data.keys())
            #print("\nGame Vars:", data['vars'].keys())
        return data
    
    def set_working_directory(self):
        GLib.chdir(GLib.path_get_dirname(__file__))
        GLib.chdir("../..")
        return GLib.get_current_dir()
    
    # Pseudo-TrisManager methods! Here!

    def update_layer(self):
        self.current_layer = self.image.get_selected_layers()[0]
        return self.current_layer
    
    @property
    def layer_parasite(self):
        return self.current_layer.get_parasite_list()
    

    # All static methods are signal handlers
    @staticmethod
    def btn_update_layer_onclick(button, self):
        self.update_layer()
        if True:
            print('Received a click!')
        else:
            #print(self.layer_dict["stoca"])
            temp_layer = self.update_layer()
            print("CAPTURED:", temp_layer.get_name())
            some_bool, ox, oy = temp_layer.get_offsets()
            ret_str = f"name: {temp_layer.get_name()}\nx: {ox}\ny: {oy}\nwidth: {temp_layer.get_width()}\nheight: {temp_layer.get_height()}"
            self.info_label.set_text(ret_str)
    
    # CRUCIAL SETUP
    def basic_setup(self, image, TrisEnum):
        self.image = image
        self.current_layer = None
        self.update_layer()
        self.shared_game_data = self.get_gamedata_from_json_file()
        print("🔻 Summary:")
        print('', "self.image", "self.current_layer", "self.update_layer()", sep='\n 🔸')
        print(" 🔸self.shared_game_data [Parsed 'gamedata.json' file]")
        print("", "self.bool_enum", "self.crumble_enum", "self.nibble_enum", "self.byte_enum", "self.onHoverNames_enum", sep='\n 🔸')
        # set properties for:
        #["BOOL", "CRUMBLE", "NIBBLE", "BYTE", "onHoverNames", "thingKind"]
        self.bool_enum = TrisEnum(self.BOOL, "The names of the gameBools")
        self.crumble_enum = TrisEnum(self.CRUMBLE, "The names of the gameCrumbles")
        self.nibble_enum = TrisEnum(self.NIBBLE, "The names of the gameNibbles")
        self.byte_enum = TrisEnum(self.BYTE, "The names of the gameBytes")
        self.onHoverNames_enum = TrisEnum(self.onHoverNames, "Things descriptions")

        future_thingKind = {}
        for elem in self.shared_game_data["thingKind"]: future_thingKind[elem["key"]] = elem["val"]
        self.thingKind = future_thingKind
        print("\n 🔸self.thingKind:")
        #for elem in self.thingKind: print(f"'{elem}'")
        for elem in self.shared_game_data["thingKind"]: print(f"{elem["key"]} ({elem["comment"]})" )

        # widget holder!
        self.tris_widget = {}
        print("\n 🔸self.tris_widget")
        print(" 🔸PROPS:\"self.shared_game_data['thingProps']", *self.shared_game_data['thingProps'], sep='"\n"', end='"' )
        print("\n\n🔺EOSummary\n")

    
    @property
    def BOOL(self):
        return self.shared_game_data["BOOL"]
    
    @property
    def CRUMBLE(self):
        return self.shared_game_data["CRUMBLE"]
    
    @property
    def NIBBLE(self):
        return self.shared_game_data["NIBBLE"]
    
    @property
    def BYTE(self):
        return self.shared_game_data["BYTE"]
    
    @property
    def onHoverNames(self):
        return self.shared_game_data["onHoverNames"]
        

    def build_main_dialog(self):
        dialog = GimpUi.Dialog.new()
        #dialog.set_default_size(320, 200)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("OK", Gtk.ResponseType.OK)

        new_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        new_box.set_name("menu container")

        dialog.get_content_area().pack_start(new_box, False, False, 1)
        return dialog, new_box
    
    def build_test_widget_hoverna(self, dialogazzo, new_box, TrisLabel, TrisChooserGrid):
        # Gtk.PositionType.LEFT
        # Gtk.PositionType.RIGHT
        # Gtk.PositionType.TOP
        # Gtk.PositionType.BOTTOM

        # https://ozh.github.io/ascii-tables/
        #  +---+----------+----------+------------+------------+---------------------------+---------------------------+--------------------------+
        #  | . | 0        | 1        | 2          | 3          | 4                         | 5                         | 6                        |
        #  +---+----------+----------+------------+------------+---------------------------+---------------------------+--------------------------+
        #  | 0 | Prop_Key | Prop_Key | Prop_value | Prop_value | Prop_human_readable_value | Prop_human_readable_value | Search_FieldSearch_Field |
        #  +---+----------+----------+------------+------------+---------------------------+---------------------------+--------------------------+
        #  | 1 | ()       | ()       | BTN_del    | BTN_Select | ()                        | Scrollable with options   | Scrollable with options  |
        #  +---+----------+----------+------------+------------+---------------------------+---------------------------+--------------------------+
        #  | 2 | ()       | ()       | ()         | ()         | ()                        | Scrollable with options   | Scrollable with options  |
        #  +---+----------+----------+------------+------------+---------------------------+---------------------------+--------------------------+
        #  | 3 |          |          |            |            |                           |                           |                          |
        #  +---+----------+----------+------------+------------+---------------------------+---------------------------+--------------------------+
        '''
        Prop_Key = TrisLabel("Prop-key")
        Prop_value = TrisLabel("Prop-value")
        Prop_human_readable_value = TrisLabel("Prop-human_readable")
   
        psbtn_del = TrisLabel("Delete")
        psbtn_sel = TrisLabel("New")

        hn_grid = Gtk.Grid.new()
        hn_grid.attach(Prop_Key, 0, 0, 2, 1)
        hn_grid.attach(Prop_human_readable_value, 2, 0, 2, 1)
        hn_grid.attach(Prop_value, 4, 0, 2, 1)
        hn_grid.attach(psbtn_del, 5, 1, 1, 1)
        hn_grid.attach(psbtn_sel, 5, 2, 1, 1)

        name_chooser = TrisChooserGrid(self, "NameGermy", self.onHoverNames)
        #now attach:
        #name_chooser.searcWidget
        #name_chooser.scrolled
        hn_grid.attach(name_chooser.searcWidget, 6, 0, 2, 1)
        hn_grid.attach(name_chooser.scrolled, 6, 1, 2, 3)
        hn_grid.show_all()
        '''
        new_name_chooser = TrisChooserGrid(self, "Thing Description", self.onHoverNames)
        frame_as = Gtk.Frame.new("Pacco!")
        frame_as.add(new_name_chooser.get_grid())
        new_box.pack_start(frame_as, True, True, 4)
        frame_as.show_all()



        

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        print("** Starting Json procedure **")
        # just for debug: not required for the plugin purpose 
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE) # MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2

        # quick bail
        if len(image.get_layers()) == 0 or image.get_xcf_file() is None:
            print("Quitting because there are no layers, or the image is not saved to disk...")
            return self.procedure_is_complete(procedure)
        
        
        # an unnecessary utility
        #from myutils import elenca_figli

        # mandatory things:
        from myutils import TrisEnum

        from myutils import TrisFrame

        from myutils import TrisBase

        from myutils import TrisBuilder

        from myutils import TrisChooser

        from myutils import TrisLabel
        from myutils import TrisChooserGrid


        # a sort of "__init__" method:
        self.basic_setup(image, TrisEnum)

        print("*** Code from here ***")

        # initialize Gtk!
        #GimpUi.init(CONSTS.FILE_NAME)
        GimpUi.init(GLib.path_get_basename(__file__).removesuffix(".py"))

        #draft for dialog!
        dialogazzo, mcontainer = self.build_main_dialog()

        self.build_test_widget_hoverna(dialogazzo, mcontainer, TrisLabel, TrisChooserGrid)

        dialogazzo.show_all()
        dialogazzo.run()

        # he he!
        return self.procedure_is_complete(procedure)





        btn_update_layer = TrisBuilder.make_gimp_button("_Update current Layer!", self.btn_update_layer_onclick, self)
        

        info_frame = GimpUi.Frame.new("Questa è la label del Frame")
        info_frame.set_name("Layer-info Frame\n" *5)

        tempval = 6
        info_frame.set_margin_start(tempval)
        info_frame.set_margin_end(tempval)
        info_frame.set_margin_top(tempval)
        info_frame.set_margin_bottom(tempval)

        #sub label
        info_frame.get_label_widget().set_name("Layer-info Frame")

        '''
        #info_label.set_use_markup(True)
        #info_label.set_markup('<span foreground="#5687ff" size="x-large">skipCondition</span>: <i>[0, 4]</i>')
        #info_label.set_markup('<span foreground="#464646"><tt>skipCondition</tt></span>: <span background="#569a58"><i>[0, 4]</i></span>')
        '''

        newTest = TrisBase(self, "hoverName")

        chooser = TrisChooser(self, "NAme", self.onHoverNames)

        for plc_widget in [newTest, chooser, Gtk.Separator.new(0), info_frame, btn_update_layer, Gtk.Separator.new(0)]:
            mcontainer.pack_start(plc_widget, False, False, 1)

        #mcontainer.pack_end(btn_update_layer, False, False, 1)
        #mcontainer.pack_start(newTest, False, False, 1)
        
        #
        dialogazzo.show_all()
        dialogazzo.run()


        # We have reached the end of the procedure: let's return "Success"
        return self.procedure_is_complete(procedure)  #procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(AdventureGameNook.__gtype__, sys.argv)

