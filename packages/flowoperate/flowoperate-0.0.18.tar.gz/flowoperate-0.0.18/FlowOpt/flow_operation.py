import json
import os
import random
import re
import time
from argparse import ArgumentParser, RawTextHelpFormatter
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pyautogui
import requests
from BaseColor.base_colors import green, blue, hgreen, hred, red, hblue, yellow
from PIL import Image
from skimage import draw
from skimage.feature import match_template

from FlowOpt.tools.file_lock import FLock
from FlowOpt.tools.time_format import tell_the_datetime, tell_timestamp, waiting


class ImageTool(object):

    def __init__(self):
        self.threshold_value = 90
        self._image_show = None
        self.color = {
            'red': [255, 0, 0],
            'yellow': [255, 255, 0],
            'green': [0, 255, 0],
            'cyan': [0, 255, 255],
            'blue': [0, 0, 255],
            'magenta': [255, 0, 255],
            'white': [255, 255, 255],
            'silver': [192, 192, 192],
            'gray': [128, 128, 128],
            'black': [0, 0, 0],
        }

    def locate(self,
               template_path,
               template_resize=1.0,
               img_path=None,
               locate_center=True,
               threshold_value=None,
               as_gray=False,
               as_binary=False, img_shape_times=1.0, return_score_only=False, screenshot_region=None
               ):
        if threshold_value:
            self.threshold_value = threshold_value
        if img_path:
            img_array = self._load_img(img_path, as_gray=as_gray, as_binary=as_binary, shape_times=img_shape_times)
            self._image_show = self._load_img(img_path, as_gray=as_gray, as_binary=as_binary,
                                              shape_times=img_shape_times)
        else:
            img_array = self._get_screen_shot(
                as_gray=as_gray, as_binary=as_binary, shape_times=img_shape_times, region=screenshot_region
            )

        template_array = self._load_img(template_path, as_gray=as_gray, as_binary=as_binary,
                                        shape_times=template_resize)

        result = self._get_result_score(template_array=template_array, image_array=img_array)
        score = (round(result.max(), 4) if result is not None else 0) * 100
        if return_score_only:
            return {"score": score, "template_path": template_path}
        if score and score > self.threshold_value:
            ij = np.unravel_index(np.argmax(result), result.shape)
            if not as_gray:
                c, x, y = ij[::-1]
                tem_h, tem_w, tc = template_array.shape
                ih, iw, ic = img_array.shape
            else:
                x, y = ij[::-1]
                tem_h, tem_w = template_array.shape
                ih, iw = img_array.shape
            x, y = int(x), int(y)
            center = [int(x + tem_w / 2), int(y + tem_h / 2)]
            print(f"[ {green(tell_the_datetime())} ]\n "
                  f"    matching image: [ {blue(img_path or 'ScreenShot')} ]\n "
                  f"    using template: [ {blue(template_path)} ]\n "
                  f"    >>> locate success! score: {hgreen(score)}\n")
            self._draw_box(x, y, tem_h, tem_w, ih, iw, 2, color="red")
            return center if locate_center else [int(x), int(y)]
        else:
            print(f"[ {green(tell_the_datetime())} ]\n "
                  f"    matching image: [ {blue(img_path or 'ScreenShot')} ]\n "
                  f"    using template: [ {blue(template_path)} ]\n "
                  f"    >>> score not pass! score: {hred(score)}\n")

    def patch_locate(self, template_path_list,
                     template_resize=1.0,
                     img_path=None,
                     locate_center=True,
                     threshold_value=None, as_gray=False,
                     as_binary=False, img_shape_times=1.0, screenshot_region=None):
        if threshold_value:
            self.threshold_value = threshold_value
        if img_path:
            img_array = self._load_img(img_path, as_gray=as_gray, as_binary=as_binary, shape_times=img_shape_times)
            self._image_show = self._load_img(img_path, as_gray=as_gray, as_binary=as_binary,
                                              shape_times=img_shape_times)
        else:
            img_array = self._get_screen_shot(
                as_gray=as_gray, as_binary=as_binary, shape_times=img_shape_times, region=screenshot_region
            )

        for template_path in template_path_list:
            template_array = self._load_img(template_path, as_gray=as_gray, as_binary=as_binary,
                                            shape_times=template_resize)

            result = self._get_result_score(template_array=template_array, image_array=img_array)
            score = (round(result.max(), 4) if result is not None else 0) * 100
            if score and score > self.threshold_value:
                ij = np.unravel_index(np.argmax(result), result.shape)
                if not as_gray:
                    c, x, y = ij[::-1]
                    tem_h, tem_w, tc = template_array.shape
                    ih, iw, ic = img_array.shape
                else:
                    x, y = ij[::-1]
                    tem_h, tem_w = template_array.shape
                    ih, iw = img_array.shape
                x, y = int(x), int(y)
                center = [int(x + tem_w / 2), int(y + tem_h / 2)]
                print(f"[ {green(tell_the_datetime())} ]\n "
                      f"    matching image: [  {blue(img_path or 'ScreenShot')}  ]\n "
                      f"    using template: [ {blue(template_path)} ]\n "
                      f"    >>> locate success! score: {hgreen(score)}\n")
                self._draw_box(x, y, tem_h, tem_w, ih, iw, 2, color="red")
                return center if locate_center else [int(x), int(y)]
            else:
                print(f"[ {green(tell_the_datetime())} ]\n "
                      f"    matching image: [  {blue(img_path or 'ScreenShot')}  ]\n "
                      f"    using template: [ {blue(template_path)} ]\n "
                      f"    >>> score not pass! score: {hred(score)}\n")

    def patch_locate_color(self, template_paths, img_path=None, color_tolerance=None, color_purity=None,
                           screenshot_region=None, img_shape_times=None):
        if not img_shape_times:
            img_shape_times = 1.0
        if img_path:
            img_color_map = self._load_img_color(img_path)
            self._image_show = self._load_img(img_path, as_gray=False, as_binary=False, shape_times=img_shape_times)
        else:
            img_color_map = self._get_screen_shot(
                region=screenshot_region, load_as_color_map=True, shape_times=img_shape_times
            )

        color_tolerance = 0 if not color_tolerance else color_tolerance
        color_purity = 1 if not color_purity else color_purity

        all_positions = []
        for template_path in template_paths:

            template_color_map = self._load_img_color(template_path)
            max_min_r = [0, 255]
            max_min_g = [0, 255]
            max_min_b = [0, 255]
            for x_y, rgb in template_color_map.items():
                r, g, b = rgb
                if r > max_min_r[0]:
                    max_min_r[0] = r
                elif r < max_min_r[1]:
                    max_min_r[1] = r

                if g > max_min_g[0]:
                    max_min_g[0] = g
                elif g < max_min_g[1]:
                    max_min_g[1] = g

                if b > max_min_b[0]:
                    max_min_b[0] = b
                elif b < max_min_b[1]:
                    max_min_b[1] = b
            max_min_r = [max_min_r[0] + color_tolerance, max_min_r[1] - color_tolerance]
            max_min_r = [max_min_r[0] if max_min_r[0] < 255 else 255, max_min_r[1] if max_min_r[1] > 0 else 0]

            max_min_g = [max_min_g[0] + color_tolerance, max_min_g[1] - color_tolerance]
            max_min_g = [max_min_g[0] if max_min_g[0] < 255 else 255, max_min_g[1] if max_min_g[1] > 0 else 0]

            max_min_b = [max_min_b[0] + color_tolerance, max_min_b[1] - color_tolerance]
            max_min_b = [max_min_b[0] if max_min_b[0] < 255 else 255, max_min_b[1] if max_min_b[1] > 0 else 0]

            color_zones = []
            for x_y, rgb in img_color_map.items():
                r, g, b = rgb
                in_zone_conditions = [
                    max_min_r[0] > r > max_min_r[1],
                    max_min_g[0] > g > max_min_g[1],
                    max_min_b[0] > b > max_min_b[1],
                ]
                if all(in_zone_conditions):
                    color_zones.append(x_y)

            start_lines = []
            start_column = []
            for cz_point in color_zones:
                x, y = cz_point.split('-')

                in_line_sta = False
                for line_set in start_lines:
                    if cz_point in line_set:
                        line_set.add(f"{int(x) + 1}-{y}")
                        in_line_sta = True
                if not in_line_sta:
                    start_lines.append({cz_point, f"{int(x) + 1}-{y}"})

                in_col_sta = False
                for col_set in start_column:
                    if cz_point in col_set:
                        col_set.add(f"{x}-{int(y) + 1}")
                        in_col_sta = True
                if not in_col_sta:
                    start_column.append({cz_point, f"{x}-{int(y) + 1}"})

            v_center_pts = set()
            for l_set in start_lines:
                if len(l_set) > color_purity:
                    ld = {int(x.split("-")[0]): x for x in l_set}
                    all_value = [x for x in ld.keys()]
                    all_value.sort()
                    center_pt = ld.get(all_value[int(len(all_value) / 2)])
                    v_center_pts.add(center_pt)

                    spx, spy = [int(i) for i in ld.get(all_value[0]).split("-")]
                    epx, epy = [int(i) for i in ld.get(all_value[-1]).split("-")]
                    self.draw_color(px=spx, py=spy, color=[255, 0, 0])
                    self.draw_color(px=epx, py=epy, color=[255, 0, 0])

            h_center_pts = set()
            for c_set in start_column:
                if len(c_set) > color_purity:
                    cd = {int(x.split("-")[1]): x for x in c_set}
                    all_value = [x for x in cd.keys()]
                    all_value.sort()
                    center_pt = cd.get(all_value[int(len(all_value) / 2)])
                    h_center_pts.add(center_pt)

                    spx, spy = [int(i) for i in cd.get(all_value[0]).split("-")]
                    epx, epy = [int(i) for i in cd.get(all_value[-1]).split("-")]
                    self.draw_color(px=spx, py=spy, color=[255, 0, 0])
                    self.draw_color(px=epx, py=epy, color=[255, 0, 0])

            final_center_pts = set()
            possible_pts = set()
            possible_extent = 3
            for vp in v_center_pts:
                if vp in h_center_pts and vp not in possible_pts:
                    vpx, vpy = [int(i) for i in vp.split("-")]
                    for i in range(-possible_extent, possible_extent + 1):
                        for j in range(-possible_extent, possible_extent + 1):
                            possible_pts.add(f"{vpx + i}-{vpy + j}")
                    final_center_pts.add(vp)
            for hp in h_center_pts:
                if hp in v_center_pts and hp not in possible_pts:
                    hpx, hpy = [int(i) for i in hp.split("-")]
                    for i in range(-possible_extent, possible_extent + 1):
                        for j in range(-possible_extent, possible_extent + 1):
                            possible_pts.add(f"{hpx + i}-{hpy + j}")
                    final_center_pts.add(hp)

            for fp in final_center_pts:
                dx, dy = [int(i) for i in fp.split("-")]
                self._draw_cross(x=dx, y=dy, color='yellow', weight=2)
            fpt = []
            if screenshot_region and isinstance(screenshot_region, list):
                for fp in final_center_pts:
                    fpx, fpy = [int(i) for i in fp.split("-")]
                    nx = screenshot_region[0] + fpx
                    ny = screenshot_region[1] + fpy
                    fpt.append([nx, ny])
            else:
                fpt = [[int(i) for i in j.split("-")] for j in final_center_pts]
            all_positions += fpt
        return all_positions

    def locate_color(self, template_path, img_path=None, color_tolerance=None, color_purity=None,
                     screenshot_region=None, img_shape_times=None):
        if not img_shape_times:
            img_shape_times = 1.0
        if img_path:
            img_color_map = self._load_img_color(img_path)
            self._image_show = self._load_img(img_path, as_gray=False, as_binary=False, shape_times=img_shape_times)
        else:
            img_color_map = self._get_screen_shot(
                region=screenshot_region, load_as_color_map=True, shape_times=img_shape_times
            )

        color_tolerance = 0 if not color_tolerance else color_tolerance
        color_purity = 1 if not color_purity else color_purity

        template_color_map = self._load_img_color(template_path)
        max_min_r = [0, 255]
        max_min_g = [0, 255]
        max_min_b = [0, 255]
        for x_y, rgb in template_color_map.items():
            r, g, b = rgb
            if r > max_min_r[0]:
                max_min_r[0] = r
            elif r < max_min_r[1]:
                max_min_r[1] = r

            if g > max_min_g[0]:
                max_min_g[0] = g
            elif g < max_min_g[1]:
                max_min_g[1] = g

            if b > max_min_b[0]:
                max_min_b[0] = b
            elif b < max_min_b[1]:
                max_min_b[1] = b
        max_min_r = [max_min_r[0] + color_tolerance, max_min_r[1] - color_tolerance]
        max_min_r = [max_min_r[0] if max_min_r[0] < 255 else 255, max_min_r[1] if max_min_r[1] > 0 else 0]

        max_min_g = [max_min_g[0] + color_tolerance, max_min_g[1] - color_tolerance]
        max_min_g = [max_min_g[0] if max_min_g[0] < 255 else 255, max_min_g[1] if max_min_g[1] > 0 else 0]

        max_min_b = [max_min_b[0] + color_tolerance, max_min_b[1] - color_tolerance]
        max_min_b = [max_min_b[0] if max_min_b[0] < 255 else 255, max_min_b[1] if max_min_b[1] > 0 else 0]

        color_zones = []
        for x_y, rgb in img_color_map.items():
            r, g, b = rgb
            in_zone_conditions = [
                max_min_r[0] > r > max_min_r[1],
                max_min_g[0] > g > max_min_g[1],
                max_min_b[0] > b > max_min_b[1],
            ]
            if all(in_zone_conditions):
                color_zones.append(x_y)

        start_lines = []
        start_column = []
        for cz_point in color_zones:
            x, y = cz_point.split('-')

            in_line_sta = False
            for line_set in start_lines:
                if cz_point in line_set:
                    line_set.add(f"{int(x) + 1}-{y}")
                    in_line_sta = True
            if not in_line_sta:
                start_lines.append({cz_point, f"{int(x) + 1}-{y}"})

            in_col_sta = False
            for col_set in start_column:
                if cz_point in col_set:
                    col_set.add(f"{x}-{int(y) + 1}")
                    in_col_sta = True
            if not in_col_sta:
                start_column.append({cz_point, f"{x}-{int(y) + 1}"})

        v_center_pts = set()
        for l_set in start_lines:
            if len(l_set) > color_purity:
                ld = {int(x.split("-")[0]): x for x in l_set}
                all_value = [x for x in ld.keys()]
                all_value.sort()
                center_pt = ld.get(all_value[int(len(all_value) / 2)])
                v_center_pts.add(center_pt)

                spx, spy = [int(i) for i in ld.get(all_value[0]).split("-")]
                epx, epy = [int(i) for i in ld.get(all_value[-1]).split("-")]
                self.draw_color(px=spx, py=spy, color=[255, 0, 0])
                self.draw_color(px=epx, py=epy, color=[255, 0, 0])

        h_center_pts = set()
        for c_set in start_column:
            if len(c_set) > color_purity:
                cd = {int(x.split("-")[1]): x for x in c_set}
                all_value = [x for x in cd.keys()]
                all_value.sort()
                center_pt = cd.get(all_value[int(len(all_value) / 2)])
                h_center_pts.add(center_pt)

                spx, spy = [int(i) for i in cd.get(all_value[0]).split("-")]
                epx, epy = [int(i) for i in cd.get(all_value[-1]).split("-")]
                self.draw_color(px=spx, py=spy, color=[255, 0, 0])
                self.draw_color(px=epx, py=epy, color=[255, 0, 0])

        final_center_pts = set()
        possible_pts = set()
        possible_extent = 3
        for vp in v_center_pts:
            if vp in h_center_pts and vp not in possible_pts:
                vpx, vpy = [int(i) for i in vp.split("-")]
                for i in range(-possible_extent, possible_extent + 1):
                    for j in range(-possible_extent, possible_extent + 1):
                        possible_pts.add(f"{vpx + i}-{vpy + j}")
                final_center_pts.add(vp)
        for hp in h_center_pts:
            if hp in v_center_pts and hp not in possible_pts:
                hpx, hpy = [int(i) for i in hp.split("-")]
                for i in range(-possible_extent, possible_extent + 1):
                    for j in range(-possible_extent, possible_extent + 1):
                        possible_pts.add(f"{hpx + i}-{hpy + j}")
                final_center_pts.add(hp)

        for fp in final_center_pts:
            dx, dy = [int(i) for i in fp.split("-")]
            self._draw_cross(x=dx, y=dy, color='yellow', weight=2)
        fpt = []
        if screenshot_region and isinstance(screenshot_region, list):
            for fp in final_center_pts:
                fpx, fpy = [int(i) for i in fp.split("-")]
                nx = screenshot_region[0] + fpx
                ny = screenshot_region[1] + fpy
                fpt.append([nx, ny])
        else:
            fpt = [[int(i) for i in j.split("-")] for j in final_center_pts]
        return fpt

    def _get_screen_shot(self, as_gray=False, as_binary=False, shape_times=1.0, region=None, load_as_color_map=False):
        if not region:
            img_obj = pyautogui.screenshot()
        else:
            region = region if isinstance(region, tuple) else tuple(region)
            img_obj = pyautogui.screenshot(region=region)  # (0, 0, 300, 400)
        if load_as_color_map:
            tmp_array = self._load_img(img_obj, as_gray=as_gray, as_binary=as_binary, shape_times=shape_times)
            self._image_show = tmp_array
            return self._load_img_color(img_obj)
        else:
            tmp_array = self._load_img(img_obj, as_gray=as_gray, as_binary=as_binary, shape_times=shape_times)
            self._image_show = tmp_array
            return tmp_array

    def _draw_box(self, x, y, th, tw, ih, iw, weight=1, color='red'):
        self._image_show = np.array(Image.fromarray(self._image_show).convert("RGB"))
        for Y in range(y, y + weight):
            for X in range(x, x + tw + weight):
                if Y > ih:
                    Y = ih
                if X > iw:
                    X = iw
                self.draw_color(X, Y, color=self.color.get(color))
        for Y in range(y, y + th):
            for X in range(x + tw, x + tw + weight):
                Y = Y if Y <= ih else ih
                X = X if X <= iw else iw
                self.draw_color(X, Y, color=self.color.get(color))
        for Y in range(y + th, y + th + weight):
            for X in range(x, x + tw + weight):
                Y = Y if Y <= ih else ih
                X = X if X <= iw else iw
                self.draw_color(X, Y, color=self.color.get(color))
        for Y in range(y, y + th):
            for X in range(x, x + weight):
                Y = Y if Y <= ih else ih
                X = X if X <= iw else iw
                self.draw_color(X, Y, color=self.color.get(color))

    def _draw_cross(self, x, y, weight=1, color='red'):
        self._image_show = np.array(Image.fromarray(self._image_show).convert("RGB"))
        extent_pts = {f'{x}-{y}'}
        for i in range(-weight, weight + 1):
            extent_pts.add(
                f"{x + i}-{y}"
            )
            extent_pts.add(
                f"{x}-{y + i}"
            )
        for pt in extent_pts:
            x, y = [int(x) for x in pt.split("-")]
            self.draw_color(px=x, py=y, color=self.color.get(color))

    def draw_color(self, px, py, color=None):
        if color is None:
            color = [255, 255, 255]
        draw_y = np.array([py, py, py + 1, py + 1])
        draw_x = np.array([px, px + 1, px + 1, px])
        rr, cc = draw.polygon(draw_y, draw_x)
        draw.set_color(self._image_show, [rr, cc], color)

    @staticmethod
    def _get_result_score(template_array, image_array):
        result = None
        try:
            result = match_template(image_array, template_array)
            # result = match_template(template_array, image_array)
        except ValueError as e:
            print('sth wrong when matching the template : {}'.format(e))
        finally:
            return result

    @staticmethod
    def _load_img(file_path, as_gray=False, as_binary=False, shape_times=None):
        convert_to = 'RGB'
        if as_gray:
            convert_to = 'L'
        if as_binary:
            convert_to = '1'
        if isinstance(file_path, str):
            img = Image.open(file_path).convert(convert_to)
        else:
            img = file_path.convert(convert_to)
        img = img.resize((int(x * shape_times) for x in img.size)) if shape_times else img
        img = np.array(img)
        return img

    @staticmethod
    def _load_img_color(file_path):
        if isinstance(file_path, str):
            img = Image.open(file_path).convert('RGB')
        else:
            img = file_path.convert('RGB')
        cur_size_x, cur_size_y = img.size
        color_map = {}
        for y in range(cur_size_y):
            for x in range(cur_size_x):
                color_map[f"{x}-{y}"] = img.getpixel((x, y))
        return color_map

    @staticmethod
    def _load_img_color_as_iter(file_path):
        if isinstance(file_path, str):
            img = Image.open(file_path).convert('RGB')
        else:
            img = file_path.convert('RGB')
        cur_size_x, cur_size_y = img.size
        for y in range(cur_size_y):
            for x in range(cur_size_x):
                yield list(img.getpixel((x, y)))

    @staticmethod
    def load_image_from_url(url):
        if re.findall('^https?://', url):
            res = requests.request("GET", url)
            img = res.content
        else:
            if not re.findall('^/', url):
                base_path = os.getcwd()
                path = os.path.join(base_path, url)
            else:
                path = url
            with open(path, 'rb') as rf:
                img = rf.read()
        bio = BytesIO()
        bio.write(img)
        return bio

    def show(self):
        if self._image_show is not None:
            plt.imshow(self._image_show, plt.cm.gray)
            plt.show()


class FlowTool(object):

    def __init__(self, operate_list, project_name=None):
        """
        step by step
        :param operate_list:
                [{
                    "name": "search image and click",
                    "method": "SearchClick",
                    "icon_path": "/root/... .../image.png",
                    "match_options": {
                                    "threshold_value": 90,
                                    "as_gray": True,
                                    "as_binary": False
                                    "img_shape_times": 1.0
                                }
                    "speed": "fast",  # "slow", "mid"
                    "pre_delay": None,
                    "sub_delay": 2,
                },{
                    "name": "search image with multi icons, if one of them matched, then click",
                    "method": "MulSearchClick",
                    "icon_paths": ["/root/... .../image1.png", "/root/... .../image2.png", ...],
                    "match_options": {
                                    "threshold_value": 90,
                                    "as_gray": True,
                                    "as_binary": False
                                    "img_shape_times": 1.0
                                }
                    "speed": "fast",  # "slow", "mid"
                    "pre_delay": None,
                    "sub_delay": 2,
                },
                {
                    "name": "open chrome and enter url",
                    "method": "EnterUrl",
                    "url": "http://www.xxx.com",
                    "speed": "fast",
                    "pre_delay": None,
                    "sub_delay": 2,
                },
                {
                    "name": "wait the icon show",
                    "method": "WaitIcon",
                    "icon_path": "/root/... .../icon.png",
                    "match_options": {
                                    "threshold_value": 90,
                                    "as_gray": True,
                                    "as_binary": False
                                    "img_shape_times": 1.0
                                }
                    "interval": 1,
                    "after_showed": "NextStep",   # "Return"
                    "time_out": 120,
                    "if_timeout": "End",    #  "NextStep", "Return", "JumpToStep4"
                },
                {
                    "name": "wait until the icon gone",
                    "method": "WaitIconGone",
                    "icon_path": "/root/... .../icon.png",
                    "match_options": {
                                    "threshold_value": 90,
                                    "as_gray": True,
                                    "as_binary": False
                                    "img_shape_times": 1.0
                                }
                    "interval": 1,
                    "after_gone": "NextStep",   # "Return"
                    "time_out": 120,
                    "if_timeout": "End",    #  "NextStep", "Return", "JumpToStep5"
                },
                {
                    "name": "save data to a file with vim",
                    "method": "SaveWithVim",
                    "save_path": "/root/... .../icon.json",
                },
                {
                    "name": "terminal opera",
                    "method": "TermCommand",
                    "Command": "redis-cli -p xxxx rpush GrCookies 'diahwdioawafdoanwf;ona;owdaow'",
                },
                {
                    "name": "move mouse to a position and click",
                    "method": "Click",
                    "position": "TopLeft",  #  "TopRight", "BottomLeft", "BottomRight", or [1000, 1000],
                    "pre_delay": None,
                    "sub_delay": 2,
                },
                ...]
        """
        self.project_name = project_name if project_name else f"Project_{tell_the_datetime(compact_mode=True, date_sep='_')}"
        self.operate_list = operate_list
        self.it = ImageTool()
        self.default_match_opt = {
            "template_resize": 1.0,
            "threshold_value": 90,
            "as_gray": True,
            "as_binary": False,
            "img_shape_times": 1.0,
        }
        self.base_path = os.path.split(os.path.abspath(__file__))[0]
        self.default_chrome_icon = os.path.join(self.base_path, "resource/icons/chrome_icon.png")
        self.screen_width, self.screen_height = pyautogui.size()
        self.ms_dic = dict()
        self.step_call_times = dict()
        self.total_steps = 0
        self.resources = dict()
        self.methods = self._method_map()
        self._ready_steps()

    def _method_map(self):
        return {
            "SearchClick": self._search_and_click,
            "SearchDrag": self._search_and_drag,
            "MulSearchClick": self._multi_search_and_click,
            "MulSearchDrag": self._multi_search_and_drag,
            "EnterUrl": self._open_chrome_and_enter_url,
            "WaitIcon": self._wait_icon_show,
            "WaitIconGone": self._wait_icon_gone,
            "SaveWithVim": self._save_data_with_vim,
            "TermCommand": self._terminal_operations,
            "Click": self._mouse_click,
            "HotKey": self._hot_key,
            "InputABC": self._input_abc,
            "Drag": self._mouse_drag,
        }

    def _ready_steps(self):
        print("steps: ")
        count = 1
        for step_data in self.operate_list:
            self.ms_dic[count] = step_data
            self.step_call_times[count] = 0
            data_list = step_data.get('data_list')
            if data_list:
                data_list_type = step_data.get('data_list_type') or 'array'
                data_sep = step_data.get('data_sep')
                if data_list_type == 'array':
                    pass
                elif data_list_type == 'file':
                    data_list_from_file = []
                    for f_name in data_list:
                        with open(f_name, 'r') as rf:
                            data_list_from_file += [x for x in rf.read().split('\n')]
                    data_list = data_list_from_file
                if data_sep:
                    new_list = []
                    for data in data_list:
                        name, value = data.split(data_sep)
                        new_list.append({"name": name, "value": value})
                else:
                    new_list = []
                    for data in data_list:
                        new_list.append({"name": "", "value": data})
                self.resources[count] = new_list
            print(f"    [ {green(count)} ] -- [ {green(step_data.get('name'))} ]")
            count += 1
        self.total_steps = len(self.operate_list)

    def _search_and_click(self, params):
        match_options = params.get("match_options")
        speed = params.get("speed") or "fast"
        search_method = params.get("search_method") or "shape"
        not_locate = params.get("not_locate") or "exit"  # "exit", "next1", "jump1"
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 0
        deviation = params.get("deviation") or [0, 0]
        click_times = int(params.get("click_times") or 1)
        click_sep = params.get("click_sep") or 0.2
        search_only = params.get("search_only") or False

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = params.get('take_method') or 'order'
        flow_name, icon_path = self._get_resources(cur_step, take_method)
        flow_name = flow_name if flow_name else params.get('pack', {}).get('flow_name', "")

        jump_step = re.findall(r'\d+', not_locate)
        time.sleep(int(pre_delay))
        check_region = match_options.get("check_region")
        if search_method == 'color':
            choice_method = match_options.get("choice_method") or 'random'
            icon_positions = self.it.locate_color(
                template_path=icon_path,
                color_tolerance=int(match_options.get('color_tolerance', 0)) or 0,
                color_purity=int(match_options.get('color_purity', 1)) or 1,
                screenshot_region=check_region,
                img_shape_times=float(match_options.get('img_shape_times', 1.0)) or 1.0,
            ) or [[]]
            if choice_method == 'random':
                icon_position = random.choice(icon_positions)
            else:
                icon_position = icon_positions[0]
        else:
            match_options = match_options if isinstance(match_options, dict) else self.default_match_opt
            icon_position = self.it.locate(
                template_path=icon_path,
                threshold_value=match_options.get('threshold_value'),
                as_gray=match_options.get('as_gray'),
                as_binary=match_options.get('as_binary'),
                img_shape_times=match_options.get('img_shape_times'),
                screenshot_region=check_region,
            )
        if icon_position:
            if check_region and isinstance(check_region, list):
                icon_position = [icon_position[0] + check_region[0], icon_position[1] + check_region[1]]
            icon_position = [icon_position[0] + deviation[0], icon_position[1] + deviation[1]]
            if not search_only:
                delay = self._speed(speed)
                self._delay_move(*icon_position, delay=delay)
                for i in range(click_times):
                    pyautogui.click()
                    time.sleep(click_sep)
            time.sleep(sub_delay)
            return {'next': cur_step + 1, "pack": {"position": icon_position, "flow_name": flow_name}}
        else:
            pack = params.get('pack', {})
            pack["flow_name"] = flow_name
            if not_locate.lower() == "exit":
                print(f"System exit because can not locate template: \n    {icon_path}")
                raise KeyboardInterrupt
            elif "jump" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 0
                return {'next': int(jump_step), "pack": pack}
            elif "back" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 1
                jump_step = int(params.get('cur_step', 1)) - int(jump_step)
                jump_step = jump_step if jump_step >= 0 else 0
                return {'next': jump_step, "pack": pack}
            else:
                jump_step = jump_step[0] if jump_step else 1
                return {'next': cur_step + int(jump_step), "pack": pack}

    def _search_and_drag(self, params):
        match_options = params.get("match_options")
        speed = params.get("speed") or "fast"
        search_method = params.get("search_method") or "shape"
        not_locate = params.get("not_locate") or "exit"  # "exit", "next1", "jump1"
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 0
        deviation = params.get("deviation") or [0, 0]
        start_position = params.get("start_position")  # ["pre_step", 300]/[100, 200]
        end_position = params.get("end_position")  # ["pre_step", "pre_step"]/[100, 200]

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = params.get('take_method') or 'all'
        flow_name, icon_path = self._get_resources(cur_step, take_method)
        flow_name = flow_name if flow_name else params.get('pack', {}).get('flow_name', "")

        jump_step = re.findall(r'\d+', not_locate)
        time.sleep(int(pre_delay))
        check_region = match_options.get("check_region")
        if search_method == 'color':
            choice_method = match_options.get("choice_method") or 'random'
            icon_positions = self.it.locate_color(
                template_path=icon_path,
                color_tolerance=int(match_options.get('color_tolerance', 0)) or 0,
                color_purity=int(match_options.get('color_purity', 1)) or 1,
                screenshot_region=check_region,
                img_shape_times=float(match_options.get('img_shape_times', 1.0)) or 1.0,
            ) or [[]]
            if choice_method == 'random':
                icon_position = random.choice(icon_positions)
            else:
                icon_position = icon_positions[0]
        else:
            match_options = match_options if isinstance(match_options, dict) else self.default_match_opt
            icon_position = self.it.locate(
                template_path=icon_path,
                threshold_value=match_options.get('threshold_value'),
                as_gray=match_options.get('as_gray'),
                as_binary=match_options.get('as_binary'),
                img_shape_times=match_options.get('img_shape_times'),
                screenshot_region=check_region,
            )
        if icon_position:
            if check_region and isinstance(check_region, list):
                icon_position = [icon_position[0] + check_region[0], icon_position[1] + check_region[1]]
            icon_position = [icon_position[0] + deviation[0], icon_position[1] + deviation[1]]

            delay = self._speed(speed)
            if start_position:
                sx, sy = start_position
                if isinstance(sx, str) and "pre_step" in sx:
                    sx = params.get('pack', {}).get('position', [])[0]
                else:
                    sx = icon_position[0]
                if isinstance(sy, str) and "pre_step" in sy:
                    sy = params.get('pack', {}).get('position', [0, ])[1]
                else:
                    sy = icon_position[1]
                self._delay_move(sx, sy, delay=0.5)
                self._delay_drag(*icon_position, delay=delay)
            elif end_position:
                ex, ey = end_position
                if isinstance(ex, str) and "pre_step" in ex:
                    ex = params.get('pack', {}).get('position', [])[0]
                else:
                    ex = icon_position[0]
                if isinstance(ey, str) and "pre_step" in ey:
                    ey = params.get('pack', {}).get('position', [0, ])[1]
                else:
                    ey = icon_position[1]
                self._delay_move(*icon_position, delay=0.5)
                self._delay_drag(ex, ey, delay=delay)
            else:
                self._delay_drag(*icon_position, delay=delay)
            time.sleep(sub_delay)
            return {'next': cur_step + 1, "pack": {"position": icon_position, "flow_name": flow_name}}
        else:
            pack = params.get('pack', {})
            pack["flow_name"] = flow_name
            if not_locate.lower() == "exit":
                print(f"System exit because can not locate template: \n    {icon_path}")
                raise KeyboardInterrupt
            elif "jump" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 0
                return {'next': int(jump_step), "pack": pack}
            elif "back" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 1
                jump_step = int(params.get('cur_step', 1)) - int(jump_step)
                jump_step = jump_step if jump_step >= 0 else 0
                return {'next': jump_step, "pack": pack}
            else:
                jump_step = jump_step[0] if jump_step else 1
                return {'next': cur_step + int(jump_step), "pack": pack}

    def _multi_search_and_click(self, params):
        match_options = params.get("match_options")
        not_locate = params.get("not_locate") or "next1"  # jump1
        speed = params.get("speed") or "fast"
        search_method = params.get("search_method") or "shape"
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 0
        jump_step = re.findall(r'\d+', not_locate)
        deviation = params.get("deviation") or [0, 0]
        click_times = int(params.get("click_times") or 1)
        click_sep = params.get("click_sep") or 0.2
        search_only = params.get("search_only") or False

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = "all"
        icon_paths = self._get_resources(cur_step, take_method)
        icon_paths = [x.get("value") for x in icon_paths]
        flow_name = params.get('pack', {}).get('flow_name', "")

        time.sleep(int(pre_delay))
        check_region = match_options.get("check_region")
        if search_method == 'color':
            choice_method = match_options.get("choice_method") or 'random'
            icon_positions = self.it.patch_locate_color(
                template_paths=icon_paths,
                color_tolerance=int(match_options.get('color_tolerance', 0)) or 0,
                color_purity=int(match_options.get('color_purity', 1)) or 1,
                screenshot_region=check_region,
                img_shape_times=float(match_options.get('img_shape_times', 1.0)) or 1.0,
            ) or [[]]
            if choice_method == 'random':
                icon_position = random.choice(icon_positions)
            else:
                icon_position = icon_positions[0]
        else:
            match_options = match_options if isinstance(match_options, dict) else self.default_match_opt
            icon_position = self.it.patch_locate(
                template_path_list=icon_paths,
                threshold_value=match_options.get('threshold_value'),
                as_gray=match_options.get('as_gray'),
                as_binary=match_options.get('as_binary'),
                img_shape_times=match_options.get('img_shape_times'),
                screenshot_region=check_region,
            )
        if icon_position:
            if check_region and isinstance(check_region, list):
                icon_position = [icon_position[0] + check_region[0], icon_position[1] + check_region[1]]
            icon_position = [icon_position[0] + deviation[0], icon_position[1] + deviation[1]]
            if not search_only:
                delay = self._speed(speed)
                self._delay_move(*icon_position, delay=delay)
                for i in range(click_times):
                    pyautogui.click()
                    time.sleep(click_sep)
            time.sleep(sub_delay)
            return {'next': cur_step + 1, "pack": {"position": icon_position, "flow_name": flow_name}}
        else:
            pack = params.get('pack', {})
            pack["flow_name"] = flow_name
            not_locate = not_locate.lower()
            if not_locate == "exit":
                print(f"System exit because can not locate template: \n    {icon_paths}")
                raise KeyboardInterrupt
            elif "jump" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 0
                return {'next': int(jump_step), "pack": pack}
            elif "back" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 1
                jump_step = int(params.get('cur_step', 1)) - int(jump_step)
                jump_step = jump_step if jump_step >= 0 else 0
                return {'next': jump_step, "pack": pack}
            else:
                jump_step = jump_step[0] if jump_step else 1
                return {'next': cur_step + int(jump_step), "pack": pack}

    def _multi_search_and_drag(self, params):
        match_options = params.get("match_options")
        speed = params.get("speed") or "fast"
        search_method = params.get("search_method") or "shape"
        not_locate = params.get("not_locate") or "exit"  # "exit", "next1", "jump1"
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 0
        deviation = params.get("deviation") or [0, 0]
        start_position = params.get("start_position")  # ["pre_step", 300]/[100, 200]
        end_position = params.get("end_position")  # ["pre_step", "pre_step"]/[100, 200]

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = "all"
        icon_paths = self._get_resources(cur_step, take_method)
        icon_paths = [x.get("value") for x in icon_paths]
        flow_name = params.get('pack', {}).get('flow_name', "")

        jump_step = re.findall(r'\d+', not_locate)
        time.sleep(int(pre_delay))
        check_region = match_options.get("check_region")
        if search_method == 'color':
            choice_method = match_options.get("choice_method") or 'random'
            icon_positions = self.it.patch_locate_color(
                template_paths=icon_paths,
                color_tolerance=int(match_options.get('color_tolerance', 0)) or 0,
                color_purity=int(match_options.get('color_purity', 1)) or 1,
                screenshot_region=check_region,
                img_shape_times=float(match_options.get('img_shape_times', 1.0)) or 1.0,
            ) or [[]]
            if choice_method == 'random':
                icon_position = random.choice(icon_positions)
            else:
                icon_position = icon_positions[0]
        else:
            icon_position = self.it.patch_locate(
                template_path_list=icon_paths,
                threshold_value=match_options.get('threshold_value'),
                as_gray=match_options.get('as_gray'),
                as_binary=match_options.get('as_binary'),
                img_shape_times=match_options.get('img_shape_times'),
                screenshot_region=check_region,
            )
        if icon_position:
            if check_region and isinstance(check_region, list):
                icon_position = [icon_position[0] + check_region[0], icon_position[1] + check_region[1]]
            icon_position = [icon_position[0] + deviation[0], icon_position[1] + deviation[1]]

            delay = self._speed(speed)
            cur_x, cur_y = [x for x in pyautogui.position()]
            if start_position:
                sx, sy = start_position
                if isinstance(sx, str) and "pre_step" in sx:
                    sx = params.get('pack', {}).get('position', [])[0]
                else:
                    sx = cur_x
                if isinstance(sy, str) and "pre_step" in sy:
                    sy = params.get('pack', {}).get('position', [0, ])[1]
                else:
                    sy = cur_y
                self._delay_move(sx, sy, delay=0.5)
                self._delay_drag(*icon_position, delay=delay)
            elif end_position:
                ex, ey = end_position
                if isinstance(ex, str) and "pre_step" in ex:
                    ex = params.get('pack', {}).get('position', [])[0]
                else:
                    ex = cur_x
                if isinstance(ey, str) and "pre_step" in ey:
                    ey = params.get('pack', {}).get('position', [0, ])[1]
                else:
                    ey = cur_y
                self._delay_move(*icon_position, delay=0.5)
                self._delay_drag(ex, ey, delay=delay)
            else:
                self._delay_drag(*icon_position, delay=delay)
            time.sleep(sub_delay)
            return {'next': cur_step + 1, "pack": {"position": icon_position, "flow_name": flow_name}}
        else:
            pack = params.get('pack', {})
            pack["flow_name"] = flow_name
            if not_locate.lower() == "exit":
                print(f"System exit because can not locate template: \n    {icon_paths}")
                raise KeyboardInterrupt
            elif "jump" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 0
                return {'next': int(jump_step), "pack": pack}
            elif "back" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 1
                jump_step = int(params.get('cur_step', 1)) - int(jump_step)
                jump_step = jump_step if jump_step >= 0 else 0
                return {'next': jump_step, "pack": pack}
            else:
                jump_step = jump_step[0] if jump_step else 1
                return {'next': cur_step + int(jump_step), "pack": pack}

    def _open_chrome_and_enter_url(self, params):
        not_locate = params.get("not_locate") or "next1"  # jump1
        chrome_icon = params.get("chrome_icon")
        speed = params.get("speed") or "fast"
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 5
        jump_step = re.findall(r'\d+', not_locate)

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = params.get('take_method') or 'order'
        flow_name, url = self._get_resources(cur_step, take_method)
        flow_name = flow_name if flow_name else params.get('pack', {}).get('flow_name', "")

        time.sleep(pre_delay)
        if not chrome_icon or not os.path.exists(chrome_icon):
            chrome_icon = self.default_chrome_icon
        chrome_position = self.it.locate(
            template_path=chrome_icon,
            as_gray=True,
        )
        if chrome_position:
            self._delay_move(*chrome_position)
            time.sleep(0.1)
            pyautogui.click()
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'l')
            self._delay_write(url, name=flow_name, delay_for_each=self._speed(speed))
            pyautogui.press('enter')
            time.sleep(sub_delay)
            return {'next': cur_step + 1, "pack": {"position": chrome_position, "flow_name": flow_name}}
        else:
            not_locate = not_locate.lower()
            pack = params.get('pack', {})
            pack["flow_name"] = flow_name
            if not_locate == "exit":
                print(f"System exit because can not locate chrome icon: \n    {chrome_icon}")
                raise KeyboardInterrupt
            elif "jump" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 0
                return {'next': int(jump_step), "pack": pack}
            elif "back" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 1
                jump_step = int(params.get('cur_step', 1)) - int(jump_step)
                jump_step = jump_step if jump_step >= 0 else 0
                return {'next': jump_step, "pack": pack}
            else:
                jump_step = jump_step[0] if jump_step else 1
                return {'next': cur_step + int(jump_step), "pack": pack}

    def _wait_icon_show(self, params):
        """
        "icon_path": "/root/... .../icon.png",
        "interval": 1,
        "after_showed": "NextStep",   # "ReturnPosition"
        "time_out": 120,
        "if_timeout": "End",    #  "NextStep", "JumpToStep4"
        "match_options": {
                                    "threshold_value": 90,
                                    "as_gray": True,
                                    "as_binary": False
                                    "img_shape_times": 1.0
                                }
        :return:
        """
        match_options = params.get("match_options")
        interval = float(params.get("interval", 1)) or 1.0
        after_showed = params.get("after_showed") or "next1"
        time_out = int(params.get("time_out", 120)) or 120
        if_timeout = params.get("if_timeout") or "exit"

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = params.get('take_method') or 'order'
        flow_name, icon_path = self._get_resources(cur_step, take_method)
        flow_name = flow_name if flow_name else params.get('pack', {}).get('flow_name', "")

        match_options = match_options if isinstance(match_options, dict) else self.default_match_opt
        show_sta = False
        times_start = time.time()
        icon_position = [0, 0]
        while True:
            if time.time() - times_start > time_out:
                break
            icon_position = self.it.locate(
                template_path=icon_path,
                template_resize=match_options.get("template_resize"),
                threshold_value=match_options.get('threshold_value'),
                as_gray=match_options.get('as_gray'),
                img_shape_times=match_options.get('img_shape_times'),
            )
            if icon_position:
                show_sta = True
                break
            time.sleep(interval)
        jump_step = re.findall(r'\d+', after_showed)

        if show_sta:
            jump_step = jump_step[0] if jump_step else 1
            r_dic = {'next': cur_step + int(jump_step), 'pack': {'position': icon_position, "flow_name": flow_name}}
            return r_dic
        else:
            timeout_jump = re.findall(r'\d+', if_timeout)
            pack = params.get('pack', {})
            pack["flow_name"] = flow_name
            if if_timeout == 'exit':
                print(red("\nSys out because icon not found!"))
                print(f"    [ {red(icon_path)} ]\n    [ {tell_the_datetime()} ]")
                raise KeyboardInterrupt
            elif "jump" in if_timeout.lower():
                timeout_jump = timeout_jump[0] if timeout_jump else 0
                return {'next': int(timeout_jump), "pack": pack}
            elif "back" in if_timeout.lower():
                timeout_jump = timeout_jump[0] if timeout_jump else 1
                timeout_jump = int(params.get('cur_step', 1)) - int(timeout_jump)
                timeout_jump = timeout_jump if timeout_jump >= 0 else 0
                return {'next': timeout_jump, "pack": pack}
            else:
                timeout_jump = timeout_jump[0] if timeout_jump else 1
                return {'next': cur_step + int(timeout_jump), "pack": pack}

    def _wait_icon_gone(self, params):
        match_options = params.get("match_options")
        interval = float(params.get("interval", 1)) or 1
        after_gone = params.get("after_gone") or "next1"
        time_out = int(params.get("time_out", 120)) or 120
        if_timeout = params.get("if_timeout") or "exit"

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = params.get('take_method') or 'order'
        flow_name, icon_path = self._get_resources(cur_step, take_method)
        flow_name = flow_name if flow_name else params.get('pack', {}).get('flow_name', "")

        match_options = match_options if isinstance(match_options, dict) else self.default_match_opt
        gone_sta = False
        times_start = time.time()
        icon_position = [0, 0]
        count = 0
        while True:
            if count > 1 and count % 10 == 0:
                print(f"icon still exist: \n  {icon_path}")
            if time.time() - times_start > time_out:
                break
            icon_position = self.it.locate(
                template_path=icon_path,
                template_resize=match_options.get("template_resize"),
                threshold_value=match_options.get('threshold_value'),
                as_gray=match_options.get('as_gray'),
                img_shape_times=match_options.get('img_shape_times'),
            )
            if not icon_position:
                gone_sta = True
                break
            time.sleep(interval)
            count += 1
        jump_step = re.findall(r'\d+', after_gone)
        if gone_sta:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': int(params.get('cur_step', 1)) + int(jump_step),
                    'pack': {'position': icon_position, "flow_name": flow_name}}
        else:
            timeout_jump = re.findall(r'\d+', if_timeout)
            pack = params.get('pack', {})
            pack["flow_name"] = flow_name
            if if_timeout == 'exit':
                print(red("\nSys out because timeout when waiting icon gone!"))
                print(f"    [ {red(icon_path)} ]\n    [ {tell_the_datetime()} ]")
                raise KeyboardInterrupt
            elif "jump" in if_timeout.lower():
                timeout_jump = timeout_jump[0] if timeout_jump else 0
                return {'next': int(timeout_jump), "pack": pack}
            elif "back" in if_timeout.lower():
                timeout_jump = timeout_jump[0] if timeout_jump else 1
                timeout_jump = int(params.get('cur_step', 1)) - int(timeout_jump)
                timeout_jump = timeout_jump if timeout_jump >= 0 else 0
                return {'next': timeout_jump, "pack": pack}
            else:
                timeout_jump = timeout_jump[0] if timeout_jump else 1
                return {'next': int(params.get('cur_step', 1)) + int(timeout_jump), "pack": pack}

    def _save_data_with_vim(self, params):
        file_full_path = params.get("file_full_path")
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 0
        after = params.get("after") or 'next1'
        flow_name = params.get('pack', {}).get('flow_name', "")

        time.sleep(pre_delay)
        pyautogui.hotkey('ctrl', 'alt', 't')
        time.sleep(0.7)
        self._delay_write(f"vim {file_full_path}", name=flow_name, delay_for_each=0.01)
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press(['g', 'g', 'd'])
        pyautogui.hotkey('shift', 'G')
        time.sleep(0.1)
        pyautogui.press('i')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'shift', 'v')
        inserting_vim = True
        while inserting_vim:
            time.sleep(0.5)
            inserting_vim = self.it.locate(
                template_path=os.path.join(self.base_path, 'resource/icons/vim_insert_end.png'),
                threshold_value=95,
                as_gray=True,
                # img_shape_times=1.0
            )
        pyautogui.press('esc')
        time.sleep(0.1)
        pyautogui.hotkey('shift', ';')
        time.sleep(0.1)
        self._delay_write("wq", delay_for_each=0.01)
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'shift', 'q')
        time.sleep(sub_delay)

        jump_step = re.findall(r'\d+', after.lower())
        pack = params.get('pack', {})
        pack["flow_name"] = flow_name
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': int(params.get('cur_step', 1)) + int(jump_step), "pack": pack}
        elif "back" in after.lower():
            jump_step = jump_step[0] if jump_step else 1
            jump_step = int(params.get('cur_step', 1)) - int(jump_step)
            jump_step = jump_step if jump_step >= 0 else 0
            return {'next': jump_step, "pack": pack}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': int(jump_step), "pack": pack}

    def _terminal_operations(self, params):
        root_password = params.get("root_password")
        after = params.get("after") or 'next1'
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 0

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = params.get('take_method') or 'order'
        flow_name, cmd = self._get_resources(cur_step, take_method)
        flow_name = flow_name if flow_name else params.get('pack', {}).get('flow_name', "")

        time.sleep(pre_delay)
        pyautogui.hotkey('ctrl', 'alt', 't')
        time.sleep(0.7)
        self._delay_write(f"{cmd}", name=flow_name, delay_for_each=0.01)
        time.sleep(0.3)
        pyautogui.press('enter')
        if self.it.locate(
                template_path=os.path.join(self.base_path, 'resource/icons/terminal_input_password.png'),
                as_gray=True,
        ):
            if root_password:
                self._delay_write(f"{root_password}", name=flow_name, delay_for_each=0.01)
                time.sleep(0.3)
                pyautogui.press('enter')
            else:
                print("please input password!")
                self._wait_icon_gone({
                    "icon_path": os.path.join(self.base_path, 'resource/icons/terminal_input_password.png'),
                    "match_options": {'as_gray': True},
                    "time_out": 1000000}
                )
        time.sleep(sub_delay)
        jump_step = re.findall(r'\d+', after.lower())
        pack = params.get('pack', {})
        pack["flow_name"] = flow_name
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': int(params.get('cur_step', 1)) + int(jump_step), "pack": pack}
        elif "back" in after.lower():
            jump_step = jump_step[0] if jump_step else 1
            jump_step = int(params.get('cur_step', 1)) - int(jump_step)
            jump_step = jump_step if jump_step >= 0 else 0
            return {'next': jump_step, "pack": pack}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': int(jump_step), "pack": pack}

    def _hot_key(self, params):
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 0
        after = params.get("after") or 'next1'
        time.sleep(pre_delay)

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = params.get('take_method') or 'order'
        flow_name, key_list = self._get_resources(cur_step, take_method)
        flow_name = flow_name if flow_name else params.get('pack', {}).get('flow_name', "")

        if len(key_list) > 1:
            pyautogui.hotkey(*key_list)
        else:
            pyautogui.press(*key_list)
        time.sleep(sub_delay)

        jump_step = re.findall(r'\d+', after.lower())
        pack = params.get('pack', {})
        pack["flow_name"] = flow_name
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': cur_step + int(jump_step), "pack": pack}
        elif "back" in after.lower():
            jump_step = jump_step[0] if jump_step else 1
            jump_step = int(params.get('cur_step', 1)) - int(jump_step)
            jump_step = jump_step if jump_step >= 0 else 0
            return {'next': jump_step, "pack": pack}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': int(jump_step), "pack": pack}

    def _input_abc(self, params):
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 0
        after = params.get("after") or 'next1'
        time.sleep(pre_delay)

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = params.get('take_method') or 'only'
        flow_name, words = self._get_resources(cur_step, take_method)
        flow_name = flow_name if flow_name else params.get('pack', {}).get('flow_name', "")

        self._delay_write(f"{words}", name=flow_name, delay_for_each=0.01)
        time.sleep(sub_delay)

        jump_step = re.findall(r'\d+', after.lower())
        pack = params.get('pack', {})
        pack["flow_name"] = flow_name
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': cur_step + int(jump_step), "pack": pack}
        elif "back" in after.lower():
            jump_step = jump_step[0] if jump_step else 1
            jump_step = int(params.get('cur_step', 1)) - int(jump_step)
            jump_step = jump_step if jump_step >= 0 else 0
            return {'next': jump_step, "pack": pack}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': int(jump_step), "pack": pack}

    def _mouse_click(self, params):
        """
        position: ["left/center/right/pre_step", "top/center/bottom/pre_step"], or [1000, 1000],
        :return:
        """
        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = params.get('take_method') or 'only'
        click_side = params.get('click_side') or 'left'
        click_times = params.get('click_times') or 1
        click_sep = params.get('click_sep') or 0.2
        flow_name, position = self._get_resources(cur_step, take_method)
        flow_name = flow_name if flow_name else params.get('pack', {}).get('flow_name', "")

        pre_delay = int(params.get("pre_delay", 0)) or 0
        sub_delay = int(params.get("sub_delay", 1)) or 1
        after = params.get("after") or 'next1'
        time.sleep(pre_delay)

        cur_x, cur_y = pyautogui.position()
        pre_position = params.get('pack', {}).get('position') or [cur_x, cur_y]

        click_point = self._point_format(position=position, pre_position=pre_position)
        self._delay_move(*click_point)

        for i in range(click_times):
            if click_side == "left":
                pyautogui.click()
            elif click_side == "middle":
                pyautogui.middleClick()
            else:
                pyautogui.rightClick()
            time.sleep(click_sep)
        time.sleep(sub_delay)

        jump_step = re.findall(r'\d+', after.lower())
        pack = params.get('pack', {})
        pack["flow_name"] = flow_name
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': cur_step + int(jump_step), "pack": pack}
        elif "back" in after.lower():
            jump_step = jump_step[0] if jump_step else 1
            jump_step = int(params.get('cur_step', 1)) - int(jump_step)
            jump_step = jump_step if jump_step >= 0 else 0
            return {'next': jump_step, "pack": pack}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': int(jump_step), "pack": pack}

    def _mouse_drag(self, params):
        """
        position: [["left/center/right/pre_step", "top/center/bottom/pre_step"], [1000, 1000]]
        :return:
        """

        cur_step = int(params.get('cur_step', 1))
        self.step_call_times[cur_step] += 1
        take_method = params.get('take_method') or 'only'
        flow_name, position = self._get_resources(cur_step, take_method)
        flow_name = flow_name if flow_name else params.get('pack', {}).get('flow_name', "")
        drag_speed = int(params.get("drag_speed", 0)) or 0.5
        pre_delay = int(params.get("pre_delay", 0)) or 0
        sub_delay = int(params.get("sub_delay", 1)) or 1
        after = params.get("after") or 'next1'
        time.sleep(pre_delay)

        cur_x, cur_y = pyautogui.position()
        pre_position = params.get('pack', {}).get('position') or [cur_x, cur_y]

        start_point = position[0]
        end_point = position[-1]

        start_point = self._point_format(position=start_point, pre_position=pre_position)
        end_point = self._point_format(position=end_point, pre_position=pre_position)

        self._delay_move(*start_point, delay=0.2)
        self._delay_drag(*end_point, delay=drag_speed)

        time.sleep(sub_delay)
        jump_step = re.findall(r'\d+', after.lower())
        pack = params.get('pack', {})
        pack["flow_name"] = flow_name
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': cur_step + int(jump_step), "pack": pack}
        elif "back" in after.lower():
            jump_step = jump_step[0] if jump_step else 1
            jump_step = int(params.get('cur_step', 1)) - int(jump_step)
            jump_step = jump_step if jump_step >= 0 else 0
            return {'next': jump_step, "pack": pack}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': int(jump_step), "pack": pack}

    def _get_resources(self, cur_step, take_method):
        ips = self.resources.get(cur_step)
        if "pop" not in take_method:
            if "only" in take_method:
                resource = self.resources[cur_step][0]
            elif "order" in take_method:
                resource = self.resources[cur_step][self.step_call_times.get(cur_step, 1) - 1]
            elif "all" in take_method:
                return self.resources[cur_step]
            else:
                resource = random.choice(self.resources[cur_step])
            name = resource.get('name')
            value = resource.get('value')
        else:
            if "all" in take_method:
                return self.resources.pop(cur_step)
            elif "order" in take_method:
                pop_index = 0
            else:
                pop_index = random.randint(0, len(ips) - 1)
            resource = self.resources[cur_step].pop(pop_index)
            name = resource.get('name')
            value = resource.get('value')
        return name, value

    def _point_format(self, position, pre_position):
        cur_x, cur_y = pyautogui.position()
        cpx = cur_x
        cpy = cur_y
        px = position[0]
        py = position[-1]
        if isinstance(px, int):
            cpx = px
        elif isinstance(px, str):
            if "left" in px:
                cpx = 1
            elif "right" in px:
                cpx = self.screen_width - 1
            elif "center" in px:
                cpx = int(self.screen_width / 2)
            elif "pre_step" in px:
                cpx = pre_position[0]
        if isinstance(py, int):
            cpy = py
        elif isinstance(py, str):
            if "top" in py:
                cpy = 1
            elif "bottom" in py:
                cpy = self.screen_height - 1
            elif "center" in py:
                cpy = int(self.screen_height / 2)
            elif "pre_step" in py:
                cpy = pre_position[0]
        final_point = [cpx, cpy]
        return final_point

    @staticmethod
    def _speed(speed):
        if isinstance(speed, int) or isinstance(speed, float):
            return speed
        if speed == 'fast':
            delay = 0.5
        elif speed == 'mid':
            delay = 1
        else:
            delay = 2
        return delay

    @staticmethod
    def _delay_move(x, y, delay=0.5):
        pyautogui.moveTo(x, y, duration=delay, tween=pyautogui.easeInOutQuad)

    @staticmethod
    def _delay_drag(x, y, delay=2):
        x1 = random.randint(-20, 20) + x
        y1 = random.randint(-5, 5) + y
        delay1 = round(delay / 3 * 2, 1)
        delay = delay - delay1 - 0.1

        pyautogui.mouseDown()
        pyautogui.moveTo(x1, y1, duration=delay1, tween=pyautogui.easeInOutBounce)
        time.sleep(0.1)
        pyautogui.moveTo(x, y, duration=delay, tween=pyautogui.easeInOutBounce)
        pyautogui.mouseUp()

    @staticmethod
    def _delay_write(words, name='', delay_for_each=0.1):
        if "[NAME]" in words:
            words = words.replace("[NAME]", name)
        pyautogui.write(words, interval=delay_for_each)

    def start(self):
        step = 1
        pre_pack = {}
        try:
            while True:
                if not self.resources.get(step):
                    print(red("process done! one or more resource used up"))
                    break
                step_data = self.ms_dic.get(int(step))
                if step_data:
                    name = step_data.get("name")
                    method = step_data.get("method")
                    params = step_data
                    params['cur_step'] = step
                    if pre_pack:
                        params.update(pre_pack)
                    print(f"running step: [ {hgreen(step)} ] -- [ {name} ]")
                    run_result = self.methods.get(method)(params=params)
                    step = run_result.pop('next')
                    pre_pack = run_result
                    print(f"next step [ {hgreen(step)} ]")
                else:
                    print("all process done!")
                    break
        except KeyboardInterrupt:
            print(red(f"[ {tell_the_datetime()} ] sys exit!"))


def load_mission_from_json(jf_path):
    with open(jf_path, 'r') as rf:
        m_list = json.loads(rf.read())
    try:
        ft = FlowTool(operate_list=m_list)
        ft.start()
    except pyautogui.FailSafeException:
        print(red("sys exist because you move the mouse to corner"))
        exit(1)
    except KeyboardInterrupt:
        exit(1)


def start_missions():
    dp = '    自动化流程小工具，如果还不清楚怎么使用，请参考 README.md。\n' \
         '    https://github.com/ga1008/basecolors'
    # da = "--->      "
    da = ""
    parser = ArgumentParser(description=dp, formatter_class=RawTextHelpFormatter, add_help=True)
    parser.add_argument("json_file", type=str, help=f'{da}json format step file path, see README.md')
    parser.add_argument("-l", "--loop", dest="loop", default=False, action='store_true',
                        help=f'{da}is loop operation? ')
    parser.add_argument("-i", "--interval", type=float, dest="interval",
                        default=0.0, help=f'{da}interval seconds between loops')
    parser.add_argument("-s", "--start_time", type=str, dest="start_time", default=None,
                        help=f'{da}when to start, default NOW')
    parser.add_argument("-e", "--end_time", type=str, dest="end_time", default=None,
                        help=f'{da}when to end, default FOREVER')

    args = parser.parse_args()
    json_file = args.json_file
    loop = args.loop
    start_time = args.start_time or tell_the_datetime()
    end_time = args.end_time or tell_the_datetime(time_stamp=(time.time() + 3600 * 24 * 365 * 900))

    if not os.path.exists(json_file):
        print(hred(f"File Not Exists!\n    {json_file}"))
        exit(1)
    fl = FLock()
    if not loop:
        print(f"running mission with json file [ {hblue(1)} ]: \n    {blue(json_file)}")
        fl.acquire()
        load_mission_from_json(json_file)
        fl.release()
        print("mission complete!")
    else:
        start_sec = tell_timestamp(start_time)
        end_sec = tell_timestamp(end_time)
        count = 1
        wait_sec = start_sec - time.time()
        if wait_sec > 0:
            print(f"waiting start time [ {red(start_time)} ] ...")
            time.sleep(wait_sec)

        while True:
            now_sec = time.time()
            if now_sec > end_sec:
                print("end time")
                print("mission complete!")
                break
            print(f"running mission with json file [ {hblue(count)} ]: \n    {blue(json_file)}")
            print(f"mission will end at time: [ {red(end_time)} ]")
            fl.acquire()
            load_mission_from_json(json_file)
            fl.release()
            print(f"waiting [ {red(args.interval)} ] to next loop ...")
            time.sleep(args.interval)
            waiting(
                reset_time=args.interval,
                warning=f"waiting [ {red(args.interval)} ] to next loop ...",
                stop_wait_warning=f"[ {tell_the_datetime()} ] mission start again!"
            )
            count += 1


def locate_image():
    dp = '    自动化流程小工具，如果还不清楚怎么使用，请参考 README.md。\n' \
         '    https://github.com/ga1008/basecolors'
    # da = "--->      "
    da = ""
    parser = ArgumentParser(description=dp, formatter_class=RawTextHelpFormatter, add_help=True)
    parser.add_argument("template_image_path", type=str, help=f'{da}the template image path')
    parser.add_argument("-tr", "--template_resize", type=float, dest="template_resize",
                        default=1.0, help=f'{da}resize the template to 1.5/0.7/2 times...')
    parser.add_argument("-th", "--threshold_value", type=int, dest="threshold_value",
                        default=90, help=f'{da} int type, 0-100')
    parser.add_argument("-ag", "--as_gray", dest="as_gray", action='store_true',
                        default=False, help=f'{da} turn the image to gray, it will faster the not')
    parser.add_argument("-ab", "--as_binary", dest="as_binary", action='store_true',
                        default=False, help=f'{da} turn the image to white or black mode, '
                                            f'more faster, but may fail the match in most time')
    parser.add_argument("-ip", "--image_path", type=str, dest="image_path",
                        default=None, help=f'{da}the image wait tobe match, if you not input this param, '
                                           f'program will automatic get a screenshot')
    parser.add_argument("-ir", "--image_resize", type=float, dest="image_resize",
                        default=1.0, help=f'{da}resize the image')
    parser.add_argument("-ssr", "--screenshot_region", type=str, dest="screenshot_region",
                        default=None, help=f'{da}screenshot region, '
                                           f'require 4 nums sep by ",": left,top,width,high like 0,0,1920,1080')
    parser.add_argument("-d", "--delay", type=float, dest="delay",
                        default=0.0, help=f'{da}delay seconds to start')
    args = parser.parse_args()
    it = ImageTool()
    print("searching ...")
    delay = args.delay
    print(f"delay [ {red(delay)} ] seconds ...")
    time.sleep(delay)
    sr = args.screenshot_region
    ssr = tuple([int(x) for x in re.findall(r'\d+', sr)]) if sr else None
    it.locate(
        template_path=args.template_image_path,
        template_resize=args.template_resize,
        threshold_value=args.threshold_value,
        as_gray=args.as_gray,
        as_binary=args.as_binary,
        img_path=args.image_path,
        img_shape_times=args.image_resize,
        screenshot_region=ssr
    )
    it.show()


def locate_color():
    dp = '    自动化流程小工具，如果还不清楚怎么使用，请参考 README.md。\n' \
         '    https://github.com/ga1008/flow_operate'
    # da = "--->      "
    da = ""
    parser = ArgumentParser(description=dp, formatter_class=RawTextHelpFormatter, add_help=True)
    parser.add_argument("template_color_img_path", type=str, help=f'{da}the color template image path')

    parser.add_argument("-ct", "--color_tolerance", type=int, dest="color_tolerance",
                        default=0, help=f'{da}the tolerance of matching img color, do not over 127')
    parser.add_argument("-cp", "--color_purity", type=int, dest="color_purity",
                        default=1, help=f'{da}the purity of matching color, default 1, do not lower then 1')

    parser.add_argument("-ip", "--image_path", type=str, dest="image_path",
                        default=None, help=f'{da}the image wait tobe match, if you not input this param, '
                                           f'program will automatic get a screenshot')
    parser.add_argument("-ir", "--image_resize", type=float, dest="image_resize",
                        default=1.0, help=f'{da}resize the image')
    parser.add_argument("-ssr", "--screenshot_region", type=str, dest="screenshot_region",
                        default=None, help=f'{da}screenshot region, '
                                           f'require 4 nums sep by ",": left,top,width,high like 0,0,1920,1080')
    parser.add_argument("-d", "--delay", type=float, dest="delay",
                        default=0.0, help=f'{da}delay seconds to start')

    args = parser.parse_args()
    it = ImageTool()
    print("searching ...")
    delay = args.delay
    print(f"delay [ {red(delay)} ] seconds ...")
    time.sleep(delay)
    sr = args.screenshot_region
    ssr = tuple([int(x) for x in re.findall(r'\d+', sr)]) if sr else None
    located_pts = it.locate_color(
        template_path=args.template_color_img_path,
        img_path=args.image_path,
        img_shape_times=args.image_resize,
        screenshot_region=ssr,
        color_tolerance=args.color_tolerance,
        color_purity=args.color_purity
    )
    if located_pts:
        print("positions:")
        for pt in located_pts:
            print(f"    {yellow(pt)}")
    else:
        print("cannot locate anything, "
              "maybe you can change the 'color_tolerance' [-ct] or 'color_purity' [-cp] options to see defference results")
    it.show()


if __name__ == '__main__':
    it = ImageTool()
    # time.sleep(1)
    # tlc = it.locate(
    #     template_path="/home/ga/Guardian/For-TiZi/BossZP/boss_zp/boss_zp/resource/process_img/t000.png",
    #     template_resize=1.0,
    #     as_gray=True,
    #     as_binary=False,
    #     threshold_value=90,
    #     img_shape_times=1.0,
    # )
    # it.show()
    it.locate_color(
        template_path="/home/ga/Guardian/For-TiZi/BossZP/boss_zp/boss_zp/resource/test_color_format/t01.jpg",
        img_path="/home/ga/Guardian/For-TiZi/BossZP/boss_zp/boss_zp/resource/test_color_format/i02.jpg",
        color_tolerance=20,
        color_purity=10
    )
    it.show()
    # jfp = "/home/ga/Guardian/For-TiZi/LaGou/lg_web/flow_get_cookies.json"
    # load_mission_from_json(jfp)
