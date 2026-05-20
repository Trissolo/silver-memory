#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from gi.repository import GObject
from gi.repository import Gio
import sys

def is_inside(px, py, x1=0, y1=0, x2=162, y2=64):
    """Check if a point is within the specified boundary."""
    return x1 <= px <= x2 and y1 <= py <= y2

def bresenham_points(x1, y1, x2, y2):
    """Calculate line points using the Bresenham algorithm."""
    results = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    if is_inside(x1, y1):
        results.append((x1, y1))

    while x1 != x2 or y1 != y2:
        e2 = err << 1
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
        if is_inside(x1, y1):
            results.append((x1, y1))
            
    return results

def get_diagonal_lines(perc=0.0, translate_x=79, gap_top=16, gap_bottom=64):
    """Calculate all diagonal line points for a given animation percentage."""
    points = []
    y_top = 0
    y_bottom = 64

    for i in range(-5, 5):
        x1 = gap_top * i + translate_x + round(gap_top * perc)
        x2 = gap_bottom * i + translate_x + round(gap_bottom * perc)
        
        line_points = bresenham_points(x1, y_top, x2, y_bottom)
        if line_points:
            points.extend(line_points)

    return points

def generate_pseudo3d_grid(image, steps, gap_top, gap_bottom):
    """Main generation logic wrapped in a single undo transaction."""
    fg_color = Gimp.context_get_foreground()
    
    # Freeze undo history to massively boost layer creation speed
    image.undo_freeze()
    
    try:
        for step in range(steps + 1):
            # Create and insert the animation frame layer
            layer = Gimp.Layer.new(
                image,
                f"Grid_{step}",
                image.get_width(),
                image.get_height(),
                Gimp.ImageType.RGB_IMAGE,
                100,
                Gimp.LayerMode.NORMAL,
            )
            image.insert_layer(layer, None, 0)
            layer.fill(Gimp.FillType.BACKGROUND)
            
            # Draw the calculated vector points onto the GIMP layer
            points = get_diagonal_lines(perc=step / steps, gap_top=gap_top, gap_bottom=gap_bottom)
            for x, y in points:
                layer.set_pixel(x, y, fg_color)
                
    finally:
        # Restore the undo stack and refresh the canvas
        image.undo_thaw()
        Gimp.displays_flush()

class Pseudo3DLinesPlugin(Gimp.PlugIn):
    """GIMP 3.0 compliant Plug-in class."""

    ## Define the procedures available inside this plugin
    def do_query_procedures(self):
        return ["plug-in-pseudo3d-lines"]

    ## Register and describe the procedure and its graphical sliders/inputs
    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.ProcedureSensitivityMask.DRAWABLE,
            self.run,
            None
        )
        
        procedure.set_image_types("RGB*")
        procedure.set_documentation(
            "Generate pseudo-3D moving lines",
            "Creates multiple layers mimicking a pseudo-3D grid line animation.",
            name
        )
        procedure.set_menu_label("Pseudo-3D Lines Grid...")
        procedure.add_menu_path("<Image>/Filters/Render/")

        # Configurable parameters that GIMP 3.0 uses to auto-generate the GUI dialog
        procedure.add_int_argument(
            "steps",
            "Steps",
            "Number of animation frames/layers to generate",
            1, 100, 10,
            GObject.ParamFlags.READWRITE
        )
        procedure.add_int_argument(
            "gap-top",
            "Gap Top",
            "Spacing distance at the top of the horizon",
            1, 500, 16,
            GObject.ParamFlags.READWRITE
        )
        procedure.add_int_argument(
            "gap-bottom",
            "Gap Bottom",
            "Spacing distance at the bottom of the viewport",
            1, 500, 64,
            GObject.ParamFlags.READWRITE
        )
        
        return procedure

    ## The execution entry point called when running the filter
    def run(self, procedure, run_mode, image, drawables, config, data):
        # Extract parameter values from the auto-generated UI config
        steps = config.get_property("steps")
        gap_top = config.get_property("gap-top")
        gap_bottom = config.get_property("gap-bottom")

        # Automatically pop up the settings dialog if run interactively
        if run_mode == Gimp.RunMode.INTERACTIVE:
            Gimp.context_push()
            if not procedure.dialog_box(config, None):
                return procedure.new_return_values(Gimp.PdbStatusType.CANCEL, None)

        generate_pseudo3d_grid(image, steps, gap_top, gap_bottom)

        if run_mode == Gimp.RunMode.INTERACTIVE:
            Gimp.context_pop()

        return procedure.new_return_values(Gimp.PdbStatusType.SUCCESS, None)

# Main entry point to register the script into GIMP's process environment
if __name__ == '__main__':
    Gimp.main(Pseudo3DLinesPlugin.__gtype__, sys.argv)


'''

def is_inside(px, py, x1 = 0, y1 = 0, x2 = 162, y2= 64):
    # Returns True if the point (px, py) is inside or on the boundary
    return x1 <= px <= x2 and y1 <= py <= y2

def BresenhamPoints(x1, y1, x2, y2, min_x = 0, max_x = 160):
    results = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx =  1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    if is_inside(x1, y1):
        results.append({ 'x': x1, 'y': y1 })
    i = 1
    while (not ((x1 == x2) and (y1 == y2))):
        e2 = err << 1
        if (e2 > -dy):
            err -= dy
            x1 += sx
        if (e2 < dx):
            err += dx
            y1 += sy
        if is_inside(x1, y1):
            results.append({ 'x': x1, 'y': y1 })
        i+= 1
    return results



image = Gimp.get_images()[0]

gapTop = 16

gapBottom = 64

yTop = 0

yBottom = 64

steps = 10

# allPoints= []

col = Gimp.context_get_foreground()

def diagonal_lines(layer, perc = 0, translate_x = 79):
    points = []
    for i in range(-5, 5):
        abs_x1 = gapTop * i + translate_x
        x1 = (abs_x1 + round(gapTop * perc))
        abs_x2 = gapBottom * i + translate_x
        x2 = (abs_x2 + round(gapBottom * perc))
        # print(f'{{x: {abs_x1}, y: 0}} {{x: {abs_x2}, y: 64}}')
        # //Gimp.pencil(layer, [x1, yTop, x2, yBottom])
        #points.append(*BresenhamPoints(x1, yTop, x2, yBottom))
        b = BresenhamPoints(x1, yTop, x2, yBottom)
        if len(b):
            points.extend(b)
        
    # allPoints.append(points)
    return points
        

for p in range(steps + 1):
    l = Gimp.Layer.new(image, f'Grid_{p}', image.get_width(), image.get_height(), Gimp.ImageType.RGB_IMAGE, 100, Gimp.LayerMode.NORMAL)
    image.insert_layer(l, None, 0)
    l.fill(Gimp.FillType.BACKGROUND)
    # //diagonal_lines(l, p / steps)
    for p in diagonal_lines(l, p / steps):
        if p:
            l.set_pixel(p['x'], p['y'], col)

'''
