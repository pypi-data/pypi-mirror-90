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


def anim_pass_ind(obj, value, frame):
    obj.pass_index = value
    obj.keyframe_insert(data_path="pass_index", frame=frame)


def anim_loc(obj, value, frame):
    obj.location = value
    obj.keyframe_insert(data_path="location", frame=frame)

def anim_loc_x(obj, value, frame):
    obj.location[0] = value
    obj.keyframe_insert(data_path="location", frame=frame)

def anim_loc_y(obj, value, frame):
    obj.location[1] = value
    obj.keyframe_insert(data_path="location", frame=frame)

def anim_loc_z(obj, value, frame):
    obj.location[2] = value
    obj.keyframe_insert(data_path="location", frame=frame)


def anim_rot(obj, value, frame):
    obj.rotation_euler = value
    obj.keyframe_insert(data_path="rotation_euler", frame=frame)


def anim_scale(obj, value, frame):
    obj.scale = value
    obj.keyframe_insert(data_path="scale", frame=frame)


def anim_attr(obj, attr, value, frame):
    setattr(obj, attr, value)
    obj.keyframe_insert(data_path=attr, frame=frame)
