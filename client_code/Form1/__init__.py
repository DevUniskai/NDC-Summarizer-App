from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import re
from datetime import datetime
import sys

def diff_day(date1, date2):  
  # Convert strings to date objects
  date_object1 = datetime.strptime(date1, "%d %b %Y")
  date_object2 = datetime.strptime(date2, "%d %b %Y")

  # Calculate the difference in days
  difference_in_days = (date_object2 - date_object1).days

  # Print the difference
  # print("Difference in days:", difference_in_days)
  return difference_in_days

def parse_penawaran(input_text):
  print("\n Result Penawaran\n\n")
  lines = input_text.strip().split('\n')
  # print(lines)
  place_index = [ [x, y] for x,y in enumerate(lines) if len(y) == 3]
  # print(place_index)
  date_time = []
  output_text = ""
  for place in place_index:
    split_datetime = lines[place[0]+1].split(" ")
    # print(split_datetime)
    time = split_datetime[0]
    date = " ".join([split_datetime[1].replace("(",""), split_datetime[2], split_datetime[3][:4]])
    # date = " ".join([split_datetime[1].replace("(",""), split_datetime[2]])
    date_time.append([time, date])
  # print(date_time)

  length = len(place_index)
  print("*Singapore Airlines*")
  output_text += "*Singapore Airlines*\n"
  for i in range(0, length, 2):
    output_text += str(date_time[i][1] + " | " + place_index[i][1] + "-" + place_index[i+1][1] + " | " + date_time[i][0] + "-" + date_time[i+1][0])
    print(date_time[i][1], end="")
    print(" | " + place_index[i][1] + "-" + place_index[i+1][1] + " ", end="")
    print("| " + date_time[i][0] + "-" + date_time[i+1][0], end="")
    days = diff_day(date_time[i][1], date_time[i+1][1])
    if (days > 0):
      output_text += str("(+ " +str(days)+")")
      print("(+ " +str(days)+")", end="")
    
    output_text += "\n"
    print("")
  
  return output_text

def get_index(list_item, search_text):
  for idx, item in enumerate(list_item):
    if search_text in item:
      return idx
  return -1

def is_konfirmasi(input_text):
  lines = input_text.strip().split(' ')

  if "Booking" in lines:
    return True
  return False

def parse_konfirmasi(input_text):
  print("\n Result Konfirmasi\n\n")
  lines = input_text.strip().split('\n')
  pass_idx = get_index(lines, "Passenger Details") + 2

  output_text ="*Singapore Airlines*\n"
  print("*Singapore Airlines*")
  #Get Passenger Data
  for i in lines[pass_idx:]:
    if("Contact Details" in i):
      break
    split_data = i.split("\t")
    no_urut = split_data[0]
    pass_data = no_urut + ". " + split_data[1]
    if(no_urut.isnumeric()):
      output_text += str(pass_data) + "\n"
      print(pass_data)

  print("")
  output_text += "\n"
  #Get Itin
  itin_idx = get_index(lines, "Itinerary Details") + 5
  order_idx = get_index(lines, "Order Details")
  pattern = r"\((.*?)\)"

  #Check Text if they copy until Order Detail
  check_text = lines[itin_idx:] if order_idx == -1 else lines[itin_idx:order_idx]
  # print(check_text)
  #Got Place
  place = re.findall(pattern, str(check_text))
  # print(place)
  length = len(place)
  start = 0
  datetime = []
  for i in check_text:
    if len(place) == start:
      break
    # print(i)
    if place[start] in i and place[start+1] in i:

      depart = i.split("\t")[1]
      arrival = i.split("\t")[3]

      depart_date = depart[:-6]
      depart_time = depart[-5:]

      arrival_date = arrival[:-6]
      arrival_time = arrival[-5:]

      output_text += str(depart_date)
      print(depart_date, end="")
      output_text += str(" | " + place[start]+"-"+place[start+1]+" | ")
      print(" | " + place[start]+"-"+place[start+1]+" | ", end="")
      output_text += str(depart_time+"-"+arrival_time)
      print(depart_time+"-"+arrival_time, end="")
      # print(i.split("\t"))
      days = diff_day(depart_date, arrival_date)
      if (days > 0):
        output_text += " (+ " +str(days)+")"
        print(" (+ " +str(days)+")", end="")
      start+=2
      output_text += "\n"
      print("")
  return output_text

def is_penawaran(text):
  split_text = text.split("\n")
  print(split_text)
  if("Booking Details" in split_text[0]):
    return True
  return False

def handle_loc(text):
  split = text.split(" ")
  data=[]
  temp=""
  for key, item in enumerate(split):

    isLastItem = key == len(split)-1

    if(item == "-" or isLastItem):
      if isLastItem:
        temp += " " + item

      data.append(temp)
      temp = ""
      continue

    if(split[key-1] == "-"):
      continue

    if(len(temp)!=0):
      temp+= " "

    temp += item

  return str(data[0] + "-" + data[1])

def handle_time(text):
  split = text.split(" ")
  idx = split.index("-")
  start = split[idx-1][-5:]
  end = split[idx+1][:5]

  return str(start + "-" + end)

def parse_penawaran_air_asia(text):
  split_text = text.split("\n")
  print(split_text)

  output = "*By Air Asia*\n\n"
  depart_idx = split_text.index("Depart date")
  depart_date = split_text[depart_idx+1]
  depart_loc = split_text[depart_idx+2]
  depart_time = handle_time(split_text[depart_idx+3])
  depart_price = split_text[depart_idx+5]

  output += str(depart_date + " | " + depart_loc + " | " + depart_time + "\n")

  return_idx = split_text.index("Return date") if "Return date" in split_text else None

  if(return_idx):
    return_date = split_text[return_idx+1]
    return_loc = split_text[return_idx+2]
    return_time = handle_time(split_text[return_idx+3])
    return_price = split_text[return_idx+5]

    output += str(return_date + " | " + return_loc + " | " + return_time + "\n")

  return output

def parse_konfirmasi_air_asia(text):
  split = text.split("\n")
  output = ""
  schedule_output = "*By Air Asia*\n"
  idx = split.index("Flight summary")
  town = split[idx+1] + "-" + split[idx+3]
  idx = split.index("Departure:")
  date = split[idx+2]
  idx = split.index("Booking status")
  time = split[idx+3]+"-"+split[idx+7]
  schedule_output += date + "|" + town + "|" + time + "\n"
  idx = split.index("Guest Name")
  length = len(split)
  
  
  for i in range(1, length-idx):
    if(len(split[idx+i]) == 0):
      continue
    name = split[idx+i].replace('(Adult)', '')
    output += name + "\n"
  
  output += "\n" + schedule_output
  return output

def main_airasia(text):  
  
  if(is_penawaran(text)):
    return parse_penawaran_air_asia(text)
  else:
    return parse_konfirmasi_air_asia(text)

def main_sq(text):
  if is_konfirmasi(text) == True:
    kon = parse_konfirmasi(text)
    return kon

  else:
    flights = parse_penawaran(text)
    return flights

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    
  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def text_box_2_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def convert_click(self, **event_args):
    """This method is called when the button is clicked"""
    # convert_result = anvil.server.call('convert',  self.text_area.text)
    airline = self.airline.selected_value
    
    if self.text_area.text:
      summary = None
      if airline == "SQ":
        summary = main_sq(self.text_area.text)

      if airline == "Air Asia":
        summary = main_airasia(self.text_area.text)
        
      if summary:
        self.btn_copy.visible = True
        self.result.visible = True
        self.result.text = summary
        self.result.underline = False
    pass

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.text_area.text = ""
    pass

  def btn_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().call_js("cpy", self.result.text)
    n = Notification("Copied to Clipboard", title="Status", style="success")
    n.show()
    
    
    
