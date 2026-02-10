#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   GIMP - The GNU Image Manipulation Program
#   Copyright (C) 1995 Spencer Kimball and Peter Mattis
#
#   gimp-tutorial-plug-in.py
#   sample plug-in to illustrate the Python plug-in writing tutorial
#   Copyright (C) 2023 Jacob Boerema
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

# just fou sys.argv
import sys

import gi

#import os

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

# Glib is used mostly for GLib.Error()
# or utility functions like:
# GLib.build_pathv(GLib.DIR_SEPARATOR_S, [GLib.get_home_dir(), "my_file_name.txt"])
from gi.repository import GLib

# GObject is for GObject.ParamFlags:
# G_PARAM_READABLE: 1
# G_PARAM_WRITABLE: 2
# G_PARAM_READWRITE: 3 # -> Alias for: G_PARAM_READABLE | G_PARAM_WRITABLE
from gi.repository import GObject

from gi.repository import Gio

# constants:
ARGU_FOLDER = "tris_user_folder"
ARGU_BOOL_EXPERIMENTAL = "Check_parasite"
'''
class CONSTS:
    FILE_NAME = "tris-save-layers-png" # GLib.path_get_basename(__file__).removesuffix(".py")
    TEXT = "QWE"
    OTHER = "FOO_NEW!"
    ARGU_TEST_BOOL = "tris_test_bool"
    ARGU_TEXT = "tris_user_text"
    ARGU_INTEGER = "tris_user_integer"
    ARGU_FOLDER = "tris_user_folder"

# Helper class
class Tris_Helper:
    message = ""
    prefix = "\n"

    @classmethod
    def reset_message(cls):
        cls.message = ""
        return cls

    @classmethod
    def add_message(cls, chunk="", prepend_prefix=True):
        cls.message += f"{cls.prefix}{chunk}" if prepend_prefix else chunk
        return cls

    @classmethod
    def show_message(cls):
        Gimp.message(cls.message)
        return cls


class FileGenerator:
    def __init__(self, path, content):
        self.path = path
        self.content = content

    def generate_file(self):
        # Create a file output stream at the specified path
        file = Gio.File.new_for_path(self.path)
        output_stream = file.replace(None, False, Gio.FileCreateFlags.NONE, None)

        # Write content to the file
        output_stream.write(self.content.encode(), None)
        
        # Close the file stream
        output_stream.close()
        print(f"File successfully written to {self.path}")
'''

# our plugin class
class SaveLayersPng(Gimp.PlugIn):
    def do_query_procedures(self):
        return ["tris-save-layers-png"] #CONSTS.FILE_NAME]

    def do_set_i18n(self, name):
        return False

    #def do_quit(self):
    #    #This method is internally bugged :(
    #    print("Buggged")
    #    return True

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None
        )

        procedure.set_image_types("*")

        procedure.set_menu_label("[Tris] 🤞Save visible layers to .png")

        procedure.add_menu_path("<Image>/Filters/[[Tris]]/")

        procedure.set_documentation(
            "[Tris] Save visible layers as .png",
            "Save Layers to .PNG for GIMP 3.0",
            name,
        )

        procedure.set_attribution("Tris", "---", "2025")

        """
        procedure.add_string_argument(
            CONSTS.ARGU_TEXT,
            "Text",
            None,
            "Hello World!...",
            GObject.ParamFlags.READWRITE,
        )

        procedure.add_boolean_argument(
            CONSTS.ARGU_TEST_BOOL,
            "Generic BOOLean",
            "This option is a BOOL (default: false)",
            False,
            GObject.ParamFlags.READWRITE,
        )

        procedure.add_int_argument ( # GimpProcedure* procedure,
            CONSTS.ARGU_INTEGER, # const gchar* name,
            "An integer number:", # const gchar* nick,
            "(The room number)", # const gchar* blurb,
            0, # gint min,
            255, # gint max,
            0, # gint value,
            GObject.ParamFlags.READWRITE # GParamFlags flags
        )
        """
        procedure.add_file_argument(
            # GimpProcedure* procedure,
            ARGU_FOLDER,  # const gchar* name,
            "Destination folder for .png",  # const gchar* nick,
            None,  # const gchar* blurb,
            Gimp.FileChooserAction.SELECT_FOLDER,  # GimpFileChooserAction action,
            True,  # gboolean none_ok,
            None,  # GFile* default_file,
            GObject.ParamFlags.READWRITE,  # GParamFlags flags
        )

        procedure.add_boolean_argument(
            ARGU_BOOL_EXPERIMENTAL,
            "Check Layer Parasite (experimental)",
            "Skip the layer if it has a CERTAIN parasite (default: Enabled).\nConversely, if it is False (unchecked), all visible layers will be saved, regardless of the parasite.",
            True,
            GObject.ParamFlags.READWRITE,
        )

        return procedure

    def prepare_pdb_procedure(self, dest):
        pdb_proc = Gimp.get_pdb().lookup_procedure('file-png-export')
        pconf = pdb_proc.create_config()
        pconf.set_property('run-mode', Gimp.RunMode.NONINTERACTIVE)
        pconf.set_property('compression', 9) # compression
        pconf.set_property('format', "auto") #format
        pconf.set_property('save-transparent', True) #save_transparent

        pconf.set_property('image', dest)
        #result = pdb_proc.run(pconf)
        #success = result.index(0)
        return pdb_proc, pconf

    def save_single_layer(self, layer, dest, pdb_proc, pconf, folder_path):
        dest_layer = Gimp.Layer.new_from_drawable(layer, dest)
        dest.insert_layer(dest_layer, None, 0)
        dest.resize_to_layers()
        
        # using new_build_filenamev()
        pconf.set_property('file',  Gio.File.new_build_filenamev([folder_path, f"{layer.get_name()}.png"]))
        print("- Writing file:", folder_path, f"{layer.get_name()}.png")
        pdb_proc.run(pconf)
        dest.remove_layer(dest_layer)
        return True


    def show_starting_dialog(self, procedure, config, title_test = "Save visible layers"):
        dialog = GimpUi.ProcedureDialog.new(procedure, config, title_test)
        dialog.fill([ARGU_FOLDER, ARGU_BOOL_EXPERIMENTAL])

        # show the plugin Dialog:
        action_on_dialog = dialog.run()
        dialog.destroy()
        return action_on_dialog
    
    # def onDestroy(self):
    #     print(self, self.__class__)


    def run(self, procedure, run_mode, image, drawables, config, run_data):
        #print(f"Args:, \nprocedure: {procedure},\nrun_mode: {run_mode},\nimage: {image},\ndrawables: {drawables},\nconfig: {config},\nrun_data: {run_data}")
        #procarg = procedure.get_arguments()[2]
        #print(f"+++debu", *procedure.get_arguments())
        # just for debug: not required for the plugin purpose 
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE) # MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2

        # It’s a convention to use the name of the executable and _not_ the PDB procedure name.
        GimpUi.init("tris_save_layers_png")

        # generate (and show, and destroy) the plugin Dialog via method (and return if the operation was cancelled or if the plugin needs to continue):
        action_on_dialog = self.show_starting_dialog(procedure, config)

        # let's start doing stuff! 
        user_selected_folder = config.get_property(ARGU_FOLDER)
        experimental_bool = config.get_property(ARGU_BOOL_EXPERIMENTAL)
        print('🍊 Bool is True' if experimental_bool else '⚫️ Bool is False')

        # Should we stop here?
        if not action_on_dialog or user_selected_folder is None:
            print("\nPlugin safely stopped -> 'Cancel' was pressed, or no destination folder was selected.")
            return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)

        # folder path stuff: 
        user_selected_folder = user_selected_folder.get_path()

        # Iterate layers:
        ##message = ""
        if len(image.get_layers()):
            dest_image = Gimp.Image.new(1, 1, 0)
            pdb_proc, pconf = self.prepare_pdb_procedure(dest_image)
            for layer in (l for l in image.get_layers() if l.get_visible()):
                if experimental_bool and "kind" in layer.get_parasite_list() and layer.get_parasite('kind').get_data()[0] == 49:
                    print(f"Skipping: {layer.get_name()} because it is a Trigger Area")
                    continue
                self.save_single_layer(layer, dest_image, pdb_proc, pconf, user_selected_folder)

            dest_image.delete()
        # else:
        #     message = "This .xcf file has no layer"
            
        # End message
        Gimp.message_set_handler(Gimp.MessageHandlerType.MESSAGE_BOX)
        Gimp.message(f"✔️ Procedure complete!\n") #\nThe user_selected_folder was '{user_selected_folder}'")
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE)
        
        # At this point, all is ok: return Success
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(SaveLayersPng.__gtype__, sys.argv)

