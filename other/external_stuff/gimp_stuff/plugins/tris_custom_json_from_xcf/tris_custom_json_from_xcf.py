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
#
#   (ensure the script is executable)

# sys: just for sys.argv and sys.path[0]
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

# Gio: I/O and files, e.g., new_file = Gio.File.new_for_path("/home/USER/Graphics/my_picture.xcf")
#from gi.repository import Gio


# other custom imports
import json
#import os


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

        procedure.set_menu_label("[Tris] ✍️💠 New Room Editor and JSON generator")

        procedure.add_menu_path("<Image>/Filters/[[Tris]]/")

        procedure.set_documentation(
            "[Tris] Basically, a JSON-Room editor for adventure games.",
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
    
    # Two test methods
    def set_working_directory(self):
        GLib.chdir(GLib.path_get_dirname(__file__))
        GLib.chdir("../..")
        return GLib.get_current_dir()
    
    def load_and_parse_gamedata_json(self):
        terminal_col_start = '\033[45m'
        terminal_col_end = '\033[0m'
        terminal_col_end = f"{terminal_col_end}\n"

        print(GLib.path_get_basename(__file__), f"{terminal_col_start}This script name (including '.py' extension){terminal_col_end}")
        print(__file__, f"{terminal_col_start}full script path (including file extension){terminal_col_end}")
        print(sys.path[0], f"{terminal_col_start}The folder of this script (without separator in the end){terminal_col_end}")
        print(GLib.DIR_SEPARATOR_S, f"{terminal_col_start}OS Separator{terminal_col_end}")

        # The JSON:
        print("Load JSON:")
        wanted_file = "gamedata.json"
        complete_path= f"{sys.path[0]}{GLib.DIR_SEPARATOR_S}{wanted_file}"
        grabbeddata = None
        with open(complete_path) as json_file:
            grabbeddata = json.load(json_file)
        
        #for key, value in grabbeddata.items():
        #    print(f"{key}: {value}", end="\n")
        #print("\ngrabbeddata KEYS:", *grabbeddata.keys(), sep="\n")

        # self.gamedata:
        # self.gamedata["BOOL"]
        # self.gamedata["CRUMBLE"]
        # self.gamedata["NIBBLE"]
        # self.gamedata["BYTE"]
        # self.gamedata["onHoverNames"]
        # self.gamedata["thingKind"]
        # self.gamedata["thingProps"]
        #self.gamedata = grabbeddata
        return grabbeddata
    
    def load_splitted_jsons(self):
        from os import listdir
        print("Splitted JSON grabbing")

        # wanted dir path, as string
        folder_path = f"{sys.path[0]}{GLib.DIR_SEPARATOR_S}splitted_gamedata{GLib.DIR_SEPARATOR_S}"
        
        # list of filenames, as string
        dir_content = listdir(folder_path)
        print(*dir_content, sep="\n")

        
        # bools = None
        # wanted_file = "bool_names.json"
        # with open(f"{folder_path}{wanted_file}") as json_file:
        #     bools = json.load(json_file)

        # print(f"{bools =}")
        return self
    
    def run(self, procedure, run_mode, image, drawables, config, run_data):
        print("** Starting -from scratch!- Json procedure **")
        # just for debug: not required for the plugin purpose
        # MessageHandlerType.MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE)

        # quick bail
        if len(image.get_layers()) == 0 or image.get_xcf_file() is None:
            print("Quitting because there are no layers, or the image is not saved to disk...")
            return self.procedure_is_complete(procedure)
        
        # initialize Gtk!
        GimpUi.init(GLib.path_get_basename(__file__).removesuffix(".py"))

        
        print("*** Generate Game Json Plugin ***")
        
        #from trispackage.logic.Stocker import var_ary, hover_names_ary

        from trispackage import TrisDialog
        from trispackage.gamedata import GamedataGatherer

        print("Plugin is creating the TrisDialog()")
        dialog_holder = TrisDialog(image)
        #dialog_holder.dialog.show_all()
        dialog_holder.dialog.run()

        
        '''
        {
            "kind": "ab",
            "x": 90,
            "y": 68,
            "frame": "r2cabinetDoors",
            "suffix": [0, 7],
            "skipCond": "b_4_1",
            "hoverName": 8
        }
        '''
        #imports
        #from trismodule import WidgetTree, TrisLabel, TrisDialog, TrisEnum, Necessary
        #print("TrisDialog MRO:", TrisDialog.__mro__)

        # get the gamedata.JSON
        #gamedata = self.load_and_parse_gamedata_json()

        # Initialize the shared stuff, managed by 'Necessary' class
        #Necessary.setup(image=image, gamedata=gamedata)
        
        #test Plugin Dialog
        #dialog = TrisDialog().run()
        #dialog.run()

        
        # We have reached the end of the procedure: let's return "Success"
        return self.procedure_is_complete(procedure)  #procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(AdventureGameNook.__gtype__, sys.argv)

