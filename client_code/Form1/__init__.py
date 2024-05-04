from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime
from anvil import TextArea 


class Form1(Form1Template):
  def __init__(self, **properties):
      
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # self.youtube_video_1.youtube_id = 'FALlhXl6CmA'
    # Any code you write here will run before the form opens.

    #comment stuff
    self.text_area_comment = TextArea(placeholder="Type your comment here...", height=100)
    self.content_panel.add_component(self.text_area_comment)  

    self.location = None
    self.count_click = 0
    self.disappearBtn.text='Make the map disappear!'
    
    self.map_1.center = GoogleMap.LatLng(30.286376,-97.737654)
    self.map_1.zoom = 15
    self.map_1.clickable_icons=False
    self.map_1.fullscreen_control=False

    pins = tables.app_tables.locations.search()
    self.markerList = []
    ind = 0
    for pin in pins:
      self.markerList.append(GoogleMap.Marker(animation=GoogleMap.Animation.DROP,position=GoogleMap.LatLng(pin['Lat'],pin['Lon'])))
      self.markerList[ind].tag = pin
      self.markerList[ind].add_event_handler('click',self.marker_click)
      self.map_1.add_component(self.markerList[ind])
      ind += 1

    # wall stuff
    # self.load_wall()

  def marker_click(self, sender, **properties):
    # Make image and description elements visible
    self.location = sender.tag
    print("Location set:", self.location)  
    self.image_1.visible = True
    self.label_6.visible = True

    # Retrieve images associated with the clicked location
    self.pictures = app_tables.images.search(Location=sender.tag)
    self.location = sender.tag

    # Reset click counter for cycling through images
    self.count_click = 0

    # Display the first image and its description
    if self.pictures:
        self.update_image_and_description()
    else:
        self.image_1.source = 'path/to/default/image.png'  # A default image if no images are found
        self.label_6.text = 'No description available'

    # Optionally, update the info about the pin
    self.infoAbtPin.visible = True
    self.infoAbtPin.text = f"You have clicked the pin at {sender.tag['Lat']}, {sender.tag['Lon']}.\n"
    self.infoAbtPin.text += f"It is called {sender.tag['Name']}."

    # Load comments related to this location
    self.load_wall()

    

  def disappearBtn_click(self, **event_args):
    if self.map_1.visible == True:
      self.map_1.visible = False
      self.disappearBtn.text='Make the map appear!'
      open_form('Form2')
    else:
      self.map_1.visible=True
      self.disappearBtn.text='Make the map disappear!'

  def signBtn_click(self, **event_args):
    if len(self.text_box_1.text.strip()) > 0 and len(self.text_area_comment.text.strip()) > 0:
        self.wallLbl.visible = True
        self.repeating_panel_1.visible = True
        now = datetime.datetime.now()
        # Add the comment to the database
        app_tables.wall.add_row(
            Signer=self.text_box_1.text.strip(), 
            When=now, 
            Location=self.location, 
            Comment=self.text_area_comment.text
        )
        self.text_box_1.text = ''  
        self.text_area_comment.text = ''  
        self.load_wall()  
    elif len(self.text_box_1.text.strip()) == 0:
        alert('You cannot sign without a name!')
    else:
        alert('You cannot post without writing a comment!')


  def load_wall(self):
    
    if self.location is None:
        print("Error: No location set.")
        return

    
    wall = app_tables.wall.search(Location=self.location)

    
    wall_list = list(wall)
    print(f"Comments fetched: {len(wall_list)}")  #  the number of comments retrieved
    if len(wall_list) > 0:
        print(f"Sample comment: {wall_list[0]}")  #  the first comment to inspect its structure

    
    if len(wall_list) == 0:
        self.wallLbl.visible = False
        self.repeating_panel_1.visible = False
        print("No comments available for this location.")
    else:
        self.wallLbl.visible = True
        self.repeating_panel_1.visible = True
        self.repeating_panel_1.items = wall_list  
        print("Comments are now displayed on the panel.")



    if not wall:
        self.wallLbl.visible = False
        self.repeating_panel_1.visible = False
    else:
        self.wallLbl.visible = True
        self.repeating_panel_1.visible = True
        self.repeating_panel_1.items = wall
        print("Items set to repeating panel:", self.repeating_panel_1.items)




  def right_btn_click(self, **event_args):
    self.count_click += 1
    self.image_1.source = self.pictures[self.count_click % len(self.pictures)]['Image']
    self.label_6.text = self.pictures[self.count_click % len(self.pictures)]['Description']

  def left_btn_click(self, **event_args):
    self.count_click -= 1
    self.image_1.source = self.pictures[self.count_click % len(self.pictures)]['Image']
    self.label_6.text = self.pictures[self.count_click % len(self.pictures)]['Description']

  def update_image_and_description(self):
        # Method to update the displayed image and description
        picture = self.pictures[self.count_click]
        self.image_1.source = picture['Image']
        self.label_6.text = picture['Description']
    
  def drop_down_1_change(self, **event_args):
    self.image_1.source = self.pictures[self.drop_down_1.selected_value % len(self.pictures)]['Image']

  def repeating_panel_1_show(self, **event_args):
    """This method is called when the repeating panel is shown on the screen"""
    pass
