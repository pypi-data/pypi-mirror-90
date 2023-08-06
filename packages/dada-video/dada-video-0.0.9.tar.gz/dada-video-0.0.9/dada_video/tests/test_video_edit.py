import os
import unittest
from datetime import datetime

from moviepy.editor import *

from dada_test import BaseTest
from dada_utils import dates, path
import dada_settings
import dada_video


class VideoEditTests(BaseTest):
    def test_load(self):
        clip = dada_video.load(self.get_fixture("test-vid.mp4"))
        self.assertTrue(isinstance(clip, VideoFileClip))
