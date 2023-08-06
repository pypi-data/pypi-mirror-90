#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import sys
import os
import shutil
import time
import pygame
import cv2
import mido
import colorama
from colorama import Fore
from typing import Dict, List, Tuple
from hashlib import sha256
pygame.init()
colorama.init()


class PrintProcess:
    def write(self, msg):
        sys.stdout.write(msg)
        sys.stdout.flush()

    def clear(self, msg):
        sys.stdout.write("{0}{1}{0}".format("\b"*len(msg), " "*len(msg)))

    def finish(self, msg):
        print(Fore.GREEN + msg + Fore.WHITE)


class Video:
    """Video class that contains midis and export."""

    def __init__(self, resolution: Tuple[int, int], fps: int, offset: int) -> None:
        """
        Initializes video.
        :param resolution: Resolution (x, y) of video.
        :param fps: Frames per second of video.
        :param offset: Offset (frames) in start time of playing.
        """
        self._res = resolution
        self._fps = fps
        self._offset = offset
        self._midi_paths = []
        self._audio_path = None
        self._gen_info()

    def _gen_info(self):
        width, height = self._res
        x_size = width * 0.95
        x_offset = width * 0.025
        y_offset = height / 2
        key_width = x_size / 52

        self._options = {
            "keys.white.gap": 2,
            "keys.white.color": (215, 215, 210),
            "keys.white.color_playing": (255, 255, 255),
            "keys.black.width_fac": 0.6,
            "keys.black.height_fac": 0.65,
            "keys.black.color": (64, 64, 64),
            "keys.black.color_playing": (144, 144, 144),
            "blocks.speed": 250,
            "blocks.color": (255, 255, 255),
            "blocks.rounding": 5,
            "blocks.motion_blur": True,
        }

        # Key positions
        self._key_width = key_width
        self._key_height = height / 4
        self._key_y_loc = y_offset
        self._key_locs = []
        for key in range(88):
            self._key_locs.append([key, self._is_white(key), self._find_x_loc(key)])

        self._key_locs = sorted(self._key_locs, key=(lambda x: 0 if x[1] else 1))

    def _is_white(self, key):
        return False if (key-3) % 12 in (1, 3, 6, 8, 10) else True

    def _find_x_loc(self, key):
        width, height = self._res
        x_size = width * 0.95
        x_offset = width * 0.025
        key_width = x_size / 52

        num_white_before = 0
        for k in range(key):
            if self._is_white(k):
                num_white_before += 1

        loc = x_offset + key_width*num_white_before
        if not self._is_white(key):
            loc -= key_width * self._options["keys.black.width_fac"] / 2
        return loc

    def configure(self, path, value):
        self._options[path] = value

    def add_midi(self, path: str) -> None:
        """Adds midi path to list."""
        self._midi_paths.append(path)

    def set_audio(self, path: str) -> None:
        """Sets audio file."""
        self._audio_path = path

    def _parse_midis(self):
        self._notes = []
        num_midis = len(self._midi_paths)
        process = PrintProcess()

        for i, path in enumerate(self._midi_paths):
            print_msg = f"Parsing midi {i+1} of {num_midis}"
            process.write(print_msg)
            midi = mido.MidiFile(path)
            tpb = midi.ticks_per_beat

            starts = [None for i in range(88)]
            tempo = 500000
            curr_frame = self._offset
            for msg in midi.tracks[0]:
                curr_frame += msg.time / tpb * tempo / 1000000 * self._fps
                if msg.is_meta and msg.type == "set_tempo":
                    tempo = msg.tempo
                elif msg.type == "note_on":
                    note, velocity = msg.note-21, msg.velocity
                    if velocity == 0:
                        self._notes.append((note, starts[note], curr_frame))
                    else:
                        starts[note] = curr_frame

            process.clear(print_msg)

        process.finish(f"Finished parsing {num_midis} midis.")

    def _calc_num_frames(self):
        max_note = max(self._notes, key=(lambda x: x[2]))
        return int(max_note[2] + 30)

    def _render_piano(self, keys):
        surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        width_white = self._key_width - self._options["keys.white.gap"]
        width_black = self._key_width * self._options["keys.black.width_fac"]
        height_white = self._key_height
        height_black = self._key_height * self._options["keys.black.height_fac"]

        for index, white, x_loc in self._key_locs:
            playing = index in keys
            if white:
                color = self._options["keys.white.color_playing"] if playing else self._options["keys.white.color"]
                pygame.draw.rect(surface, color, (x_loc, self._key_y_loc, width_white, height_white))
            else:
                color = self._options["keys.black.color_playing"] if playing else self._options["keys.black.color"]
                pygame.draw.rect(surface, color, (x_loc, self._key_y_loc, width_black, height_black))

        return surface

    def _render_blocks(self, frame):
        surface = pygame.Surface(self._res, pygame.SRCALPHA)
        width, height = self._res
        y_offset = height / 2
        white_width = width * 0.95 / 52
        black_width = white_width * self._options["keys.black.width_fac"]

        for key, start, end in self._notes:
            bottom_y = (frame-start)/self._fps*self._options["blocks.speed"] + y_offset
            top_y = bottom_y - (end-start)/self._fps*self._options["blocks.speed"]

            visible = bottom_y >= 0 and top_y <= y_offset
            if visible:
                x_loc = self._find_x_loc(key)
                width = white_width if self._is_white(key) else black_width
                height = bottom_y - top_y

                color = self._options["blocks.color"]
                radius = self._options["blocks.rounding"]
                if self._options["blocks.motion_blur"]:
                    mb_dist = self._options["blocks.speed"] / self._fps / 3
                    pygame.draw.rect(surface, (*color, 92), (x_loc, top_y-mb_dist, width-1, height+mb_dist), border_radius=radius)
                pygame.draw.rect(surface, color, (x_loc, top_y, width-1, height), border_radius=radius)

        pygame.draw.rect(surface, (0, 0, 0), (0, y_offset, *self._res))
        return surface

    def _render(self, frame):
        surface = pygame.Surface(self._res)

        playing = []
        for note in self._notes:
            if note[1] <= frame <= note[2]:
                playing.append(note[0])

        surface.blit(self._render_blocks(frame), (0, 0))
        surface.blit(self._render_piano(playing), (0, 0))

        return surface

    def export(self, path: str, frames: int = None) -> None:
        """
        Exports video to path.
        :param path: Path to export, must be .mp4
        :param frames: Fixed amount of frames to export (set to None to auto detect)
        """
        if not path.endswith(".mp4"):
            raise ValueError("Path must end with .mp4")

        print("-" * 50)
        print(f"Exporting video:")

        # Setup export
        get_hash = lambda: sha256(str(time.time()).encode()).hexdigest()[:20]
        parent = os.path.realpath(os.path.dirname(__file__))

        hash = get_hash()
        while os.path.isfile(os.path.join(parent, hash+".png")) or os.path.isfile(os.path.join(parent, hash+".mp4")):
            hash = get_hash()

        tmp_img_path = os.path.join(parent, hash+".png")
        tmp_vid_path = os.path.join(parent, hash+".mp4")
        video = cv2.VideoWriter(tmp_vid_path, cv2.VideoWriter_fourcc(*"MPEG"), self._fps, self._res)

        # Export frames
        self._parse_midis()
        if frames is None:
            frames = self._calc_num_frames()
        try:
            process = PrintProcess()
            start = time.time()
            for frame in range(frames):
                msg = f"Exporting frame {frame} of {frames}"
                elapse = time.time() - start
                left = (frames-frame-1) * elapse / (frame+1)
                percent = (frame+1) / frames
                progress = int(percent * 50)
                progress_msg = "[{}{}] {}%".format("#"*int(progress), "-"*int(50-progress), int(percent*100))
                final_msg = "{}    Remaining: {}    {}".format(msg, str(left)[:6], progress_msg)
                process.write(final_msg)

                surface = self._render(frame)
                pygame.image.save(surface, tmp_img_path)
                video.write(cv2.imread(tmp_img_path))

                process.clear(final_msg)

            process.finish(f"Finished exporting {frames} frames.")

            video.release()
            cv2.destroyAllWindows()

        except KeyboardInterrupt:
            print(Fore.RED + "Keyboard interrupt")
            os.remove(tmp_img_path)
            os.remove(tmp_vid_path)
            return

        os.remove(tmp_img_path)

        # Combine audio and video
        if self._audio_path is not None:
            print(Fore.WHITE + "Combining with audio")
            command = "ffmpeg -y -i {} -r {} -i {} -filter:a aresample=async=1 -c:a aac -c:v copy {}"
            command = command.format(self._audio_path, self._fps, tmp_vid_path, path)
            os.system(command)
        else:
            shutil.copy(tmp_vid_path, path)
        os.remove(tmp_vid_path)

        print(Fore.WHITE + "-" * 50)
