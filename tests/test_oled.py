import sys, types, unittest, importlib.util, logging, os
from PIL import Image, ImageFont
from pathlib import Path
root = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(root/'pironman5_text')]

# Load the real 1.2.5 OLED controller, replacing only hardware/status dependencies.
pkg = types.ModuleType('fixture'); pkg.__path__ = []; sys.modules['fixture'] = pkg
driver = types.ModuleType('fixture.ssd1306')
class Screen:
    def __init__(self, **kwargs):
        font = os.environ.get('OLED_TEST_FONT', 'DejaVuSans.ttf')
        self.font_8 = ImageFont.truetype(font, 8)
        self.font_12 = ImageFont.truetype(font, 12)
        self.frames = []; self.image = Image.new('1', (128,64))
    def is_ready(self): return True
    def clear(self): self.image.paste(0,(0,0,128,64))
    def display(self): self.frames.append(self.image.copy())
    def set_rotation(self, value): pass
    def off(self): pass
driver.SSD1306 = Screen; driver.Rect = object; sys.modules[driver.__name__] = driver
utils = types.ModuleType('fixture.utils')
utils.format_bytes = lambda *a, **k: None
utils.log_error = lambda f: f
sys.modules[utils.__name__] = utils
status = types.ModuleType('sf_rpi_status')
for name in ['get_cpu_temperature','get_cpu_percent','get_memory_info','get_disks_info','get_ips']:
    setattr(status, name, lambda: None)
sys.modules[status.__name__] = status
spec = importlib.util.spec_from_file_location('fixture.oled', root/'tests/upstream_oled.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
# Standard-screen rendering is outside this test; count returns to that path.
def normal(self): self.normal_count = getattr(self, 'normal_count', 0) + 1
module.OLED.draw_oled = normal
from text_oled import make_text_oled, validate_message
from api import register
from flask import Flask

class Tests(unittest.TestCase):
    def setUp(self):
        self.oled = make_text_oled(module.OLED)({'oled_enable':True, 'oled_sleep_timeout':0})
        self.now = 100.; self.oled._clock = lambda: self.now
        self.app = Flask(__name__); register(self.app, self.oled); self.client = self.app.test_client()
    def test_expiry_returns_to_normal(self):
        self.oled.set_text({'lines':['Hello'], 'duration':30}); self.oled.run()
        self.assertIsNotNone(self.oled.oled.frames[-1].getbbox())
        self.now = 130; self.oled.run(); self.assertEqual(self.oled.normal_count, 1)
    def test_persistent_replace_clear(self):
        self.oled.set_text({'lines':['A'], 'duration':0}); self.now += 100000
        self.assertTrue(self.oled.text_status()['active'])
        self.oled.set_text({'lines':['B'], 'duration':0}); self.oled.run()
        self.assertEqual(self.oled.text_status()['lines'], ['B'])
        self.oled.clear_text(); self.oled.run(); self.assertEqual(self.oled.normal_count,1)
    def test_disabled_rejects_and_stays_off(self):
        self.oled.set_text({'lines':['A']}); self.oled.update_config({'oled_enable':False})
        self.assertFalse(self.oled.text_status()['active']); frames = len(self.oled.oled.frames)
        self.oled.run(); self.oled.wake(); self.assertEqual(len(self.oled.oled.frames),frames)
        self.assertEqual(self.client.post('/api/v1.0/set-oled-text',json={'lines':['A']}).status_code,409)
    def test_initial_disabled(self):
        oled = make_text_oled(module.OLED)({'oled_enable':False})
        with self.assertRaises(RuntimeError): oled.set_text({'lines':['A']})
    def test_wakes_sleeping_and_timeout_resumes(self):
        self.oled.sleep_timeout=1; self.oled.sleep(); self.oled.set_text({'lines':['A'],'duration':30})
        self.oled.run(); self.assertTrue(self.oled.wake_flag)
        self.now += 30; self.oled.run(); self.assertEqual(self.oled.normal_count,1)
    def test_bounds(self):
        self.oled.set_text({'lines':['W'*80]*4}); self.oled.run()
        box = self.oled.oled.frames[-1].getbbox()
        self.assertLessEqual(box[2],128); self.assertLessEqual(box[3],64)
    def test_bad_payloads(self):
        for data in [None,{}, {'lines':[]},{'lines':['x']*5},{'lines':[3]}, {'lines':['x'*81]}, {'lines':['\n']}, {'lines':['ðŸ˜€']}, {'lines':['x'],'duration':True}, {'lines':['x'],'duration':-1}, {'lines':['x'],'duration':float('nan')}, {'lines':['x'],'duration':86401}]:
            with self.subTest(data=data):
                self.assertEqual(self.client.post('/api/v1.0/set-oled-text',json=data).status_code,400)
    def test_api_success_get_clear(self):
        self.assertTrue(self.client.post('/api/v1.0/set-oled-text',json={'lines':['Temp: 21.5 \u00b0C']}).json['status'])
        self.assertTrue(self.client.get('/api/v1.0/get-oled-text').json['data']['active'])
        self.assertFalse(self.client.post('/api/v1.0/clear-oled-text').json['data']['active'])
    def test_malformed_and_large(self):
        self.assertEqual(self.client.post('/api/v1.0/set-oled-text',data='{',content_type='application/json').status_code,400)
        self.assertEqual(self.client.post('/api/v1.0/set-oled-text',data='x'*5000,content_type='application/json').status_code,413)
    def test_render_failure_does_not_escape(self):
        self.oled.set_text({'lines':['A']})
        self.oled.oled.display = lambda: (_ for _ in ()).throw(OSError('simulated'))
        with self.assertLogs(level=logging.ERROR): self.oled.run()
        self.assertFalse(self.oled.text_status()['active'])
        self.oled.run(); self.assertEqual(self.oled.normal_count,1)

if __name__ == '__main__': unittest.main(verbosity=2)
