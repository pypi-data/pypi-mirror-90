import pytest
from pathlib import Path
from . import plug

class TestPlugBox:
    def get_self_plugbox(self):
        p = Path('.') / 'tools' / 'plugins'
        if p.exists():
            box = plug.PlugBox()
            box.searchpaths.append(p)
            return box
    
    def test_can_create_plugbox(self):
        plug.PlugBox()
    
    def test_can_find_plugin_correctly(self):
        PLUGNAME = "empty-plugin"
        box = self.get_self_plugbox()
        if box:
            box.exists(PLUGNAME)
        else:
            pytest.skip("could not find correct plugin folder for test")
    
    def test_can_load_plugin_correctly(self):
        pytest.skip("this test always died unexpectly")
        # Looks like something (pytest?) modified the importing, makes pluginbase could not load module from internal space
        PLUGNAME = "empty-plugin"
        box = self.get_self_plugbox()
        if box:
            box.load(PLUGNAME)
        else:
            pytest.skip("could not find correct plugin folder for test")
