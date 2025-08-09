import os
import psutil
import pyautogui
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



# === VOLUME TOOLS ===
def set_volume_tool(input: str) -> str:
    try:
        level = int(input.strip())
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        return f"✅ Volume successfully set to {level}%."
    except Exception as e:
        return f"❌ Failed to set volume: {e}"

def get_volume_tool(input: str) -> str:
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        level = int(volume.GetMasterVolumeLevelScalar() * 100)
        return f"🔊 Current volume is {level}%."
    except Exception as e:
        return f"❌ Failed to get volume: {e}"

# === BRIGHTNESS TOOLS ===
def set_brightness_tool(input: str) -> str:
    try:
        level = int(input.strip())
        sbc.set_brightness(level)
        return f"✅ Brightness successfully set to {level}%."
    except Exception as e:
        return f"❌ Failed to set brightness: {e}"

def get_brightness_tool(input: str) -> str:
    try:
        level = sbc.get_brightness()[0]
        return f"🌞 Current brightness is {level}%."
    except Exception as e:
        return f"❌ Failed to get brightness: {e}"

# === BATTERY STATUS ===
def get_battery_status_tool(input: str) -> str:
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return "⚠️ Battery status not available."
        charging = "charging 🔌" if battery.power_plugged else "not charging 🔋"
        return f"🔋 Battery is at {battery.percent}%, and is currently {charging}."
    except Exception as e:
        return f"❌ Failed to get battery status: {e}"

# === SCREENSHOT ===
def take_screenshot_tool(input: str) -> str:
    try:
        filename = input.strip() if input.strip() else "screenshot.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return f"📸 Screenshot saved as '{filename}'. ✅"
    except Exception as e:
        return f"❌ Failed to take screenshot: {e}"

# === LOCK, SHUTDOWN, RESTART ===
def lock_system_tool(input: str) -> str:
    try:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "🔒 System locked successfully. ✅"
    except Exception as e:
        return f"❌ Failed to lock system: {e}"

def shutdown_system_tool(input: str) -> str:
    try:
        os.system("shutdown /s /t 1")
        return "🛑 System shutdown initiated. ✅"
    except Exception as e:
        return f"❌ Failed to shutdown system: {e}"

def restart_system_tool(input: str) -> str:
    try:
        os.system("shutdown /r /t 1")
        return "🔁 System restart initiated. ✅"
    except Exception as e:
        return f"❌ Failed to restart system: {e}"
import subprocess

def wifi_off(input: str) -> str:
    try:
        subprocess.run(["netsh", "wlan", "disconnect"], check=True)
        return "✅ Wi-Fi disconnected."
    except Exception as e:
        return f"❌ Error disconnecting Wi-Fi: {e}"

def wifi_on(input: str) -> str:
    try:
        # Auto-connect to strongest known network
        subprocess.run(["netsh", "wlan", "connect", "name=<YourNetworkName>"], check=True)
        return "✅ Wi-Fi connected to saved network."
    except Exception as e:
        return f"❌ Error connecting Wi-Fi: {e}"

def list_wifi_networks(input: str) -> str:
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "networks"], encoding='utf-8')
        return "📶 Available Wi-Fi Networks:\n" + result
    except Exception as e:
        return f"❌ Failed to list Wi-Fi networks: {e}"

def check_internet(input: str) -> str:
    try:
        subprocess.check_call(["ping", "-n", "1", "8.8.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "🌐 Internet is reachable. ✅"
    except subprocess.CalledProcessError:
        return "❌ No internet connection."
def bluetooth_on(input: str) -> str:
    try:
        subprocess.run(["powershell", "-Command", "Start-Service bthserv"], check=True)
        return "✅ Bluetooth has been turned ON."
    except Exception as e:
        return f"❌ Failed to turn on Bluetooth: {e}"

def bluetooth_off(input: str) -> str:
    try:
        subprocess.run(["powershell", "-Command", "Stop-Service bthserv"], check=True)
        return "✅ Bluetooth has been turned OFF."
    except Exception as e:
        return f"❌ Failed to turn off Bluetooth: {e}"
def set_dark_mode(input: str) -> str:
    try:
        subprocess.run(["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize", "/v", "AppsUseLightTheme", "/t", "REG_DWORD", "/d", "0", "/f"], check=True)
        return "🌙 Dark mode enabled. ✅"
    except Exception as e:
        return f"❌ Failed to set dark mode: {e}"

def set_light_mode(input: str) -> str:
    try:
        subprocess.run(["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize", "/v", "AppsUseLightTheme", "/t", "REG_DWORD", "/d", "1", "/f"], check=True)
        return "☀️ Light mode enabled. ✅"
    except Exception as e:
        return f"❌ Failed to set light mode: {e}"
def rotate_screen(input: str) -> str:
    orientation = input.strip().lower()
    orientations = {
        "landscape": 0,
        "portrait": 1,
        "landscape_flipped": 2,
        "portrait_flipped": 3
    }
    if orientation not in orientations:
        return "❌ Invalid input. Use: landscape, portrait, landscape_flipped, portrait_flipped."

    try:
        subprocess.run(["DisplaySwitch.exe", "/internal"], check=True)
        subprocess.run(["powershell", f"(Get-CimInstance -Namespace root\\wmi -ClassName WmiMonitorBasicDisplayParams).DisplayOrientation={orientations[orientation]}"], check=True)
        return f"✅ Screen rotated to {orientation.replace('_', ' ')} mode."
    except Exception as e:
        return f"❌ Failed to rotate screen: {e}"
def change_resolution(input: str) -> str:
    try:
        width, height = map(int, input.strip().split("x"))
        subprocess.run([r".\QRes.exe", "/x", str(width), "/y", str(height)], check=True)
        return f"✅ Resolution changed to {width}x{height}."
    except Exception as e:
        return f"❌ Failed to change resolution: {e}"
def set_display_mode(input: str) -> str:
    mode = input.strip().lower()
    display_modes = {
        "pc screen only": "/internal",
        "duplicate": "/clone",
        "extend": "/extend",
        "second screen only": "/external"
    }
    if mode not in display_modes:
        return "❌ Invalid input. Use: PC screen only, duplicate, extend, second screen only."

    try:
        subprocess.run(["DisplaySwitch.exe", display_modes[mode]], check=True)
        return f"✅ Display mode set to: {mode}"
    except Exception as e:
        return f"❌ Failed to set display mode: {e}"
