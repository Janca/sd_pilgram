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
        'All',
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
                    choices=Script.PILGRAM_FILTERS, 
                    value="None", 
                    elem_id=self.elem_id("fk_pilgram_active_filter")
                )

        return [dropdown_active_filter]

    def run(self, p, dropdown_active_filter):
        processed = processing.process_images(p)
        processed_images_length = len(processed.images)

        def do_filter(working_image, target_filter_func):
            working_image = target_filter_func(working_image)
            return working_image

        filter_func = None
        if dropdown_active_filter == '1977':
            filter_func = '_1977'

        else:
            filter_func = dropdown_active_filter.lower()

        if filter_func is None:
            return processed

        if filter_func == 'all':
            target_func = Script.PILGRAM_FILTERS[1:]
        else:
            target_func = [filter_func]

        for filter_func_name in target_func:
            if filter_func_name == "1977":
                f = getattr(pilgram, "_1977")
            else:
                f = getattr(pilgram, filter_func_name.lower())

            for i in range(processed_images_length):
                working_image = do_filter(working_image=processed.images[i], target_filter_func=f)
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
