"""GPL-2.0-only. Real Pillow rendering with a simulated physical OLED."""
import unittest
import test_oled as baseline
from PIL import ImageFont
from visuals import ICONS, SIZES, icon_image, render_frame, fit_text
from text_oled import validate_message

class VisualTests(baseline.Tests):
    def test_sizes_increase_actual_pixel_height(self):
        heights=[]
        for size in SIZES:
            result=self.client.post('/api/v1.0/set-oled-text',json={'lines':['Hg'],'font_size':size})
            self.assertEqual(result.status_code,200)
            self.oled.run(); box=self.oled.oled.frames[-1].getbbox()
            heights.append(box[3]-box[1]); self.assertLessEqual(box[3],64)
        self.assertEqual(heights,sorted(set(heights)))

    def test_line_limits_preserve_previous_message(self):
        for size,(_,limit) in SIZES.items():
            self.oled.set_text({'lines':['OK']*limit,'font_size':size})
            response=self.client.post('/api/v1.0/set-oled-text',json={'lines':['NO']*(limit+1),'font_size':size})
            self.assertEqual(response.status_code,400)
            self.assertEqual(self.oled.text_status()['lines'],['OK']*limit)

    def test_icons_and_spin_frames(self):
        for name in ICONS:
            self.assertIsNotNone(icon_image(name).getbbox())
            self.oled.set_text({'icon':name}); self.oled.run()
        for name in ('fan','spinner'):
            self.assertNotEqual(icon_image(name,0,'spin').tobytes(),icon_image(name,1,'spin').tobytes())

    def test_pulse_frames_follow_time_and_expire(self):
        self.oled.set_text({'icon':'heart','animation':'pulse','duration':4})
        self.oled.run(); first=self.oled.oled.frames[-1].tobytes()
        self.now+=1; self.oled.run()
        self.assertNotEqual(first,self.oled.oled.frames[-1].tobytes())
        self.now+=3; self.oled.run(); self.assertEqual(self.oled.normal_count,1)

    def test_blink_keeps_text_visible(self):
        message=validate_message({'lines':['OK'],'icon':'home','animation':'blink'})
        a=render_frame(message,self.oled.oled.font_8,0)
        b=render_frame(message,self.oled.oled.font_8,1)
        self.assertIsNotNone(a.crop((0,0,32,64)).getbbox())
        self.assertIsNone(b.crop((0,0,32,64)).getbbox())
        self.assertEqual(a.crop((40,0,128,64)).tobytes(),b.crop((40,0,128,64)).tobytes())

    def test_truncation_reserves_icon_column(self):
        for size in SIZES:
            font=ImageFont.truetype(self.oled.oled.font_8.path,size)
            for width in (88,128):
                fitted=fit_text('W'*80,font,width)
                self.assertTrue(fitted.endswith('...'))
                self.assertLessEqual(font.getlength(fitted),width)

    def test_invalid_options(self):
        for data in [{'lines':['x'],'font_size':True},{'lines':['x'],'font_size':15},{'icon':{}},{'icon':'unknown'},{'animation':'spin'},{'icon':'heart','animation':'spin'},{'icon':'home','animation':[]},{'lines':['x'],'duration':10**300},{'lines':['x'],'url':'http://example.com'}]:
            with self.subTest(data=data):
                self.assertEqual(self.client.post('/api/v1.0/set-oled-text',json=data).status_code,400)

    def test_disabled_animation_and_status(self):
        self.oled.set_text({'icon':'thermometer','lines':['21.5 C'],'font_size':16})
        state=self.client.get('/api/v1.0/get-oled-text').json['data']
        self.assertEqual(state['font_size'],16); self.assertEqual(state['icon'],'thermometer')
        self.oled.update_config({'oled_enable':False})
        self.assertEqual(self.client.post('/api/v1.0/set-oled-text',json={'icon':'fan','animation':'spin'}).status_code,409)
        self.assertFalse(self.oled.text_status()['active'])

if __name__=='__main__': unittest.main(verbosity=2)
