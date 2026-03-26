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
#import json
#import os


# our plugin class
class GameInventory(Gimp.PlugIn):
    # procedure(s) name in Procedure Browser. Note that this string value CANNOT have underscores, only hyphens/dashes
    def do_query_procedures(self):
        return ["tris-game-inventory-editor"]

    def do_set_i18n(self, name):
        return False

    # The ImageProcedure (mostly hardcoded strings)
    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None
        )

        procedure.set_image_types("*")

        procedure.set_menu_label("[Tris] ⛏️ Tris Game Inventory generator")

        procedure.add_menu_path("<Image>/Filters/[[Tris]]/")

        procedure.set_documentation(
            "[Tris] Basically, a barebone Javascript Class for a simple inventory in adventure games.",
            "A complex plugin (GIMP 3.0). WIP",
            name,
        )

        procedure.set_attribution("Tris", "---", "2026")

        procedure.add_boolean_argument(
            "crossroads",
            "Dialog for JSON Game properties (True-Checked) or Inventory properties (False-Unchecked)?",
            "Determine what Dialog will be built.",
            True,
            GObject.ParamFlags.READWRITE,
        )

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
    
    # def set_working_directory(self):
    #     GLib.chdir(GLib.path_get_dirname(__file__))
    #     GLib.chdir("../..")
    #     return GLib.get_current_dir()
       
    def run(self, procedure, run_mode, image, drawables, config, run_data):
        print("** Starting -Inventory procedure **")
        # MessageHandlerType.MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE)

        print("Inv drawables and layers", drawables[0].get_name(), len(drawables), len(image.get_layers()))

        # quick bail
        if len(image.get_layers()) == 0 or image.get_xcf_file() is None:
            print("Quitting because there are no layers, or the image is not saved to disk...", sys.version, sys.version_info)
            return self.procedure_is_complete(procedure)
        
        # initialize Gtk!
        GimpUi.init(GLib.path_get_basename(__file__).removesuffix(".py"))
        
        print("*** Generate Game Inventory Plugin ***")

        from invpackage import InventoryDialog

        options_dialog = GimpUi.ProcedureDialog.new(procedure, config, "title_test")
        options_dialog.fill(["crossroads"])
        options_dialog.run()
        options_dialog.destroy()

        dialog = InventoryDialog(image=image, crossroads=config.get_property("crossroads"))
        dialog.run()
        dialog.destroy()

        print("DESTROYED")
        
        # We have reached the end of the procedure: let's return "Success"
        return self.procedure_is_complete(procedure)  #procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(GameInventory.__gtype__, sys.argv)

