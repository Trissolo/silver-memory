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

# Glib is used mostly for GLib.Error()
# or utility functions like:
# GLib.build_pathv(GLib.DIR_SEPARATOR_S, [GLib.get_home_dir(), "my_file_name.txt"])
from gi.repository import GLib

# GObject is for GObject.ParamFlags:
# G_PARAM_READABLE: 1
# G_PARAM_WRITABLE: 2
# G_PARAM_READWRITE: 3 # -> Alias for: G_PARAM_READABLE | G_PARAM_WRITABLE
from gi.repository import GObject

# I/O and files
from gi.repository import Gio


# other custom imports
import json
#import os

#print("---------")

# constants:
class CONSTS:
    FILE_NAME = GLib.path_get_basename(__file__).removesuffix(".py") # "tris_base_simple" # GLib.path_get_basename(__file__).removesuffix(".py")
    ID_IN_PLUGIN_BROWSER = "tris-obtain-path-controlpoints"
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
    #def_mes_han = Gimp.message_get_handler()

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


# our plugin class
class PathControlpointsGrabber(Gimp.PlugIn):
    as_pointlike = []
    as_string = []
    thinned_out_list = []

    def add_container(self):
        cont = []
        self.as_pointlike.append(cont)
        return cont
    

    def store_pointlike(self, point_x, point_y, cont = []):
        cont.append({'x': point_x, 'y': point_y})

    # procedure(s) name in Procedure Browser. Note that this string value CANNOT have underscores, only hyphens/dashes.
    def do_query_procedures(self):
        return [CONSTS.ID_IN_PLUGIN_BROWSER]


    def do_set_i18n(self, name):
        return False


    #def do_quit(self):
    #    #This method is internally bugged :(
    #    print("Buggged")
    #    return True


    # The ImageProcedure (mostly hardcoded strings)
    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None
        )

        procedure.set_image_types("*")

        procedure.set_menu_label("[Tris] 🔹 Print Path controlpoints")

        procedure.add_menu_path("<Image>/Filters/[[Tris]]/")

        procedure.set_documentation(
            "[Tris] Extracts and prints the controlpoints of any visible path.",
            "Nothing to say - GIMP 3.0",
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
        
        procedure.add_file_argument(
            # GimpProcedure* procedure,
            CONSTS.ARGU_FOLDER,  # const gchar* name,
            "Destination folder for .png",  # const gchar* nick,
            None,  # const gchar* blurb,
            Gimp.FileChooserAction.SELECT_FOLDER,  # GimpFileChooserAction action,
            True,  # gboolean none_ok,
            None,  # GFile* default_file,
            GObject.ParamFlags.READWRITE,  # GParamFlags flags
        )
        """
        return procedure


    def quick_generator(self, image, grab_layers = False):
       return (item for item in (image.get_layers() if grab_layers else image.get_paths()) if item.get_visible())


    def isolate_points(self, controlpoints, point_container):
        res = []
        for idx in range(0, len(controlpoints), 6):
            x = int(controlpoints[idx])
            y = int(controlpoints[idx + 1])
            res.append(x)
            res.append(y)
            self.store_pointlike(x, y, point_container)
        return res


    def list_to_single_string(self, listarg):
        return " ".join(str(elem) for elem in listarg)
    

    def iterate_strokes(self, visible_path):
        for stroke_idx in visible_path.get_strokes():
            points_cont = self.add_container()
            controlpoints = visible_path.stroke_get_points(stroke_idx).controlpoints
            #prune controlpoints:
            thinned_out = self.isolate_points(controlpoints, points_cont)
            self.thinned_out_list.append(thinned_out)
            #print(f'{visible_path.get_name()} thinned_out: {thinned_out}')
            self.as_string.append(self.list_to_single_string(thinned_out))
            #return thinned_out


    def run(self, procedure, run_mode, image, drawables, config, run_data):
        #print(f"Args:, \nprocedure: {procedure},\nrun_mode: {run_mode},\nimage: {image},\ndrawables: {drawables},\nconfig: {config},\nrun_data: {run_data}")

        # just for debug: not required for the plugin purpose 
        Gimp.message_set_handler(Gimp.MessageHandlerType.MESSAGE_BOX) #CONSOLE) # MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2

        # Any plug-in that provides a user interface should call this function
        # (It’s a convention to use the name of the executable and _not_ the PDB procedure name)
        GimpUi.init(CONSTS.FILE_NAME)

        for visible_path in self.quick_generator(image, False):
            self.iterate_strokes(visible_path)

        #Gimp.message("CONTROLPOINTS (VsCode)! Is a warning?")

        total_result = {'id': 0, 'coords':self.as_string}
        Gimp.message(json.dumps(total_result, indent = 2))

        #total_result={'asPoints': self.as_pointlike}
        #Gimp.message(json.dumps(total_result))

        #raw list:
        #print("thinned_out_list", self.thinned_out_list)

        #print("CP END")

        # At this point, all is ok: return Success
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(PathControlpointsGrabber.__gtype__, sys.argv)

