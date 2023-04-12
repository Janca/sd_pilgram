import modules.scripts as scripts
import gradio as gr

import pilgram
import copy
import re

from modules import processing, images
from modules.processing import Processed
from modules.shared import opts, state

from PIL import Image, ImageFilter, ImageEnhance


class Script(scripts.Script):

    PILGRAM_FILTERS = [
        '1977',
        'Aden',
        'Brannan',
        'Brooklyn',
        'Clarendon',
        'Earlybird',
        'Gingham',
        'Hudson',
        'Inkwell',
        'Kelvin',
        'Lark',
        'Lofi',
        'Maven',
        'Mayfair',
        'Moon',
        'Nashville',
        'Perpetua',
        'Reyes',
        'Rise',
        'Slumber',
        'Stinson',
        'Toaster',
        'Valencia',
        'Walden',
        'Willow',
        'Xpro2'
    ]

    def title(self):
        return "Pilgram Filters"

    def show(self, is_img2img):
        return not is_img2img

    def ui(self, is_img2img):
        with gr.Blocks():
            with gr.Row():
                dropdown_active_filter = gr.Dropdown(
                    label="Filter", 
                    choices=["All", *Script.PILGRAM_FILTERS], 
                    value="None", 
                    elem_id=self.elem_id("fk_pilgram_active_filter")
                )

        return [dropdown_active_filter]
    
    def __get_selected_pilgrim_filter(self, dropdown_active_filter):
        filter_func = dropdown_active_filter.lower()

        if filter_func is None or filter_func == "none":
            return None

        if filter_func == 'all':
            return Script.PILGRAM_FILTERS
        else:
            return [filter_func]
    
    def __get_pilgrim_func(self, f_name):
        if f_name == "1977":
            return getattr(pilgram, "_1977")
        else:
            return getattr(pilgram, f_name.lower())
        
    def __get_html_for_filter(self, name):
        pass

    def run(self, p, dropdown_active_filter):
        processed = processing.process_images(p)
        processed_images_length = len(processed.images)
        
        target_filter_func = self.__get_selected_pilgrim_filter(dropdown_active_filter)
        for filter_func_name in target_filter_func:
            filter_func = self.__get_pilgrim_func(filter_func_name)

            for i in range(processed_images_length):
                working_image = filter_func(processed.images[i])
                working_image_info = f"{processed.info}, Pilgram Filter: {filter_func_name}"

                images.save_image(
                    working_image, 
                    p.outpath_samples, 
                    "", 
                    p.seed,
                    p.prompt,
                    opts.samples_format,
                    working_image_info,
                    p=p
                )

                processed.images.append(working_image)
                processed.all_seeds.append(p.seed)
                processed.all_subseeds.append(p.subseed)
                processed.all_prompts.append(p.prompt)

        return processed
