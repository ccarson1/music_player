
import os
import random
import time
import kivy

kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config

from os.path import exists

Window.size = (400, 600)



class MyApp(MDApp):
  
  def on_start(self):
    print("App started...")
    self.start = 0
    self.end = 8
    self.scrolltitle = Clock.schedule_interval(self.scrolltitle, 1)

  def build(self):
      
      self.icon = 'icons/v4.png'
      self.title = "RuneStick"
      layout = MDRelativeLayout(md_bg_color=[.2, .2, .2, .8])
      self.pos = 0
      self.music_dir =  os.getcwd() + "/Music"
      music_files = os.listdir(self.music_dir)

      # print("This are music files " + str(music_files))

      self.song_list = [x for x in music_files if x.endswith('mp3') ]
      #print("this is the song list " + str(self.song_list))

      self.song_count = len(self.song_list)
      self.songlabel = Label(pos_hint={'center_x': 0.5, 'center_y': .96},
                             size_hint=(.5, .5),
                             font_size=18)
      self.albumimage = Image(pos_hint={'center_x': 0.5, 'center_y': 0.55},
                              size_hint=(.8, .75))
      self.currenttime = Label(text="00:00",
                               pos_hint={'center_x': .16, 'center_y': .145},
                               size_hint=(1, 1),
                               font_size=18)
      self.totaltime = Label(text="00:00",
                             pos_hint={'center_x': 0.84, 'center_y': .145},
                             size_hint=(1, 1),
                             font_size=18)

      self.progressbar = ProgressBar(max=100,
                                     value=0,
                                     pos_hint={'center_x': 0.5, 'center_y': 0.12},
                                     size_hint=(.8, .75))
      self.volumeslider = Slider(min=0,
                                 max=1,
                                 value=0.5,
                                 orientation='vertical',
                                 pos_hint={'center_x': 0.05, 'center_y': 0.50},
                                 size_hint=(.5, .5))
      self.loopLabel = Label(text="Loop", pos_hint={'center_x': 0.8, 'center_y': .99},
                             size_hint=(.5, .5),
                             font_size=10)
      self.switch = Switch( pos_hint={'center_x': 0.80, 'center_y': 0.95})
      self.backbutton = MDIconButton(pos_hint={'center_x': 0.25, 'center_y': 0.05},
                                      icon="icons/icons8-back-48.png",
                                      on_press=self.backaudio, disabled=False)

      self.playbutton = MDIconButton(pos_hint={'center_x': 0.4, 'center_y': 0.05},
                                     icon="icons/icons8-circled-play-48.png",
                                     on_press=self.playaudio)

      self.stopbutton = MDIconButton(pos_hint={'center_x': 0.55, 'center_y': 0.05},
                                     icon="icons/icons8-stop-48.png",
                                     on_press=self.stopaudio, disabled=True)
      self.nextbutton = MDIconButton(pos_hint={'center_x': 0.70, 'center_y': 0.05},
                                      icon="icons/icons8-next-48.png",
                                      on_press=self.nextaudio, disabled=False)
      self.folderButton = MDIconButton(pos_hint={'center_x': 0.10, 'center_y': 0.95},
                                      icon="icons/folder.png",
                                      on_press=self.folder, disabled=False)
      layout.add_widget(self.folderButton)
      layout.add_widget(self.songlabel)
      layout.add_widget(self.albumimage)
      layout.add_widget(self.currenttime)
      layout.add_widget(self.totaltime)
      layout.add_widget(self.progressbar)
      layout.add_widget(self.volumeslider)
      layout.add_widget(self.loopLabel)
      layout.add_widget(self.switch)
      layout.add_widget(self.playbutton)
      layout.add_widget(self.stopbutton)
      layout.add_widget(self.backbutton)
      layout.add_widget(self.nextbutton)

      def loopAudio(instance, value):
          if value == True:
              self.sound.loop = True
          else:
              self.sound.loop = False
          print(value)


      self.switch.bind(active=loopAudio)

      def volume(instance, value):
          print(value)
          self.sound.volume = value

      self.volumeslider.bind(value=volume)
      Clock.schedule_once(self.playaudio)

      return layout

  def playaudio(self, obj):
      

      self.playbutton.disabled = True
      self.stopbutton.disabled = False

      self.song_title = self.song_list[self.pos]
      song_title = str(self.song_title).split(".")
      #print(song_title)
      # self.songlabel.text = self.song_title[:-4] 
      self.songlabel.text = song_title[0][0:8]
      self.sound = SoundLoader.load('{}/{}'.format(self.music_dir, self.song_title))
      #print("The self songtitile is " + self.song_title)
      if os.path.exists("images/" + song_title[0] + ".jpg"):
        self.albumimage.source = "images/" + song_title[0] + ".jpg"
        
      else:
        self.albumimage.source = "icons/v4.png"
        
      #print(str(self.albumimage.source))
      self.sound.volume = 0.5
      self.sound.play()
      #print(self.sound.length)
      self.progressbarEvent = Clock.schedule_interval(self.updateprogressbar, self.sound.length/60/5)
      self.timeEvent = Clock.schedule_interval(self.settime, 1)

      #print(str("the progress bar value is" + str(self.sound.length)))


  def scrolltitle(self, t):
    print(song_title)

  def updateprogressbar(self, value):
    
    if self.progressbar.value < self.sound.length:
        self.progressbar.value += (1/self.sound.length)*100
    #print(str(self.progressbar.value) + ":" + str(self.sound.length))

    


  def settime(self, t):
    
    current_time = time.strftime('%M:%S', time.gmtime(self.progressbar.value))
    total_time = time.strftime('%M:%S', time.gmtime(self.sound.length))
    self.currenttime.text = current_time
    self.totaltime.text = total_time
    # if current_time == total_time:
    #   current_time = 0.0
    # print(current_time)

    if self.end == len(self.song_title):
      self.start = 0
      self.end = 8
    else:
      self.start += 1
      self.end +=1
    #print(str(self.start) + ":" +  str(self.end))
    #print(len(self.song_title))
    self.songlabel.text = self.song_title[self.start:self.end]

  def stopaudio(self, obj):
    self.playbutton.disabled = False
    self.stopbutton.disabled = True
    self.sound.stop()

  def nextaudio(self, obj):
    self.sound.stop()

    if self.pos == len(self.song_list)-1:
      self.pos = 0
    else:
      #print('End of list...')
      self.pos = self.song_list.index(self.song_title)+1
      
    self.playaudio(obj)
    #print(str(self.pos) + ':' + str(len(self.song_list)-1))
  def backaudio(self, obj):
    self.sound.stop()
    self.pos = self.song_list.index(self.song_title)-1
    self.playaudio(obj)

  def folder(self, obj):
    #print("Folder accessed...")
    pass

if __name__ == '__main__':
    MyApp().run()