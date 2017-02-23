from os.path import dirname
import sys

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import subprocess

__author__ = 'kfarwell'

LOGGER = getLogger(__name__)

class QuodLibetSkill(MycroftSkill):
    def __init__(self):
        super(QuodLibetSkill, self).__init__(name="QuodLibetSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        pause_intent = IntentBuilder("PauseMediaIntent")\
            .require("PauseMediaKeyword")\
            .build()
        self.register_intent(pause_intent, self.handle_pause_intent)

        resume_intent = IntentBuilder("ResumeMediaIntent")\
            .require("ResumeMediaKeyword")\
            .build()
        self.register_intent(resume_intent, self.handle_resume_intent)

        next_intent = IntentBuilder("NextMediaIntent")\
            .require("NextMediaKeyword")\
            .build()
        self.register_intent(next_intent, self.handle_next_intent)

        prev_intent = IntentBuilder("PrevMediaIntent")\
            .require("PreviousMediaKeyword")\
            .build()
        self.register_intent(prev_intent, self.handle_prev_intent)

        play_intent = IntentBuilder("PlayMediaIntent")\
            .require("PlayMediaKeyword")\
            .require("Query")\
            .build()
        self.register_intent(play_intent, self.handle_play_intent)

        enqueue_intent = IntentBuilder("EnqueueMediaIntent")\
            .require("EnqueueMediaKeyword")\
            .require("Query")\
            .build()
        self.register_intent(enqueue_intent, self.handle_enqueue_intent)

        filter_intent = IntentBuilder("FilterMediaIntent")\
            .require("FilterMediaKeyword")\
            .require("Query")\
            .build()
        self.register_intent(filter_intent, self.handle_filter_intent)

        clear_queue_intent = IntentBuilder("ClearQueueMediaIntent")\
            .require("ClearQueueMediaKeyword")\
            .build()
        self.register_intent(clear_queue_intent, self.handle_clear_queue_intent)

        unqueue_intent = IntentBuilder("UnqueueMediaIntent")\
            .require("UnqueueMediaKeyword")\
            .require("Query")\
            .build()
        self.register_intent(unqueue_intent, self.handle_unqueue_intent)

        whats_playing_intent = IntentBuilder("WhatsPlayingMediaIntent")\
            .require("WhatsPlayingMediaKeyword")\
            .build()
        self.register_intent(whats_playing_intent,
                             self.handle_whats_playing_intent)

    def handle_pause_intent(self, message):
        subprocess.check_output(["quodlibet", "--pause"])

    def handle_resume_intent(self, message):
        subprocess.check_output(["quodlibet", "--play"])

    def handle_next_intent(self, message):
        subprocess.check_output(["quodlibet", "--next"])

    def handle_prev_intent(self, message):
        subprocess.check_output(["quodlibet", "--force-previous"])

    def handle_play_intent(self, message):
        subprocess.check_output(["quodlibet", "--unqueue", ""])
        subprocess.check_output(["quodlibet", "--enqueue", message.data.get("Query")])
        subprocess.check_output(["quodlibet", "--next"])

    def handle_enqueue_intent(self, message):
        subprocess.check_output(["quodlibet", "--enqueue", message.data.get("Query")])
 
    def handle_filter_intent(self, message):
        subprocess.check_output(["quodlibet", "--unqueue", ""])
        subprocess.check_output(["quodlibet", "--query", message.data.get("Query")])
        subprocess.check_output(["quodlibet", "--next"])

    def handle_clear_queue_intent(self, message):
        subprocess.check_output(["quodlibet", "--unqueue", ""])
        subprocess.check_output(["quodlibet", "--unfilter"])

    def handle_unqueue_intent(self, message):
        subprocess.check_output(["quodlibet", "--unqueue", message.data.get("Query")])

    def handle_whats_playing_intent(self, message):
        spec = {
            "playing": subprocess.check_output(["quodlibet", "--print-playing", "<title> by <artist> on <album>"])
        }
        self.speak_dialog("whats_playing", spec)

    def stop(self):
        pass

def create_skill():
    return QuodLibetSkill()
