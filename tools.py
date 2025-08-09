from System_Control.system_cmd import (
    set_volume_tool,
    get_volume_tool,    
    set_brightness_tool,
    get_brightness_tool,
    get_battery_status_tool,
    take_screenshot_tool,
    lock_system_tool,
    shutdown_system_tool,
    restart_system_tool,
    wifi_on,
    wifi_off,
    list_wifi_networks,
    check_internet,
    set_dark_mode,
    set_light_mode,
    rotate_screen,
    change_resolution,
    set_display_mode
)
from System_Control.file_management import (
    create_file,
    read_file,
    write_file,
    append_file,
    delete_file,
    execute_file
)
from langchain.agents import Tool  # or your own Tool class if custom
from System_Control.browser import browse_web
tools = [
    Tool(
        name="set_volume",
        func=set_volume_tool,
        description="Set the system's volume level from 0 to 100. Input should be a number like '50'. If the response includes ✅, the volume was successfully set."
    ),
    Tool(
        name="get_volume",
        func=get_volume_tool,
        description="Get the current system volume level. If the response includes 🔊, the value was fetched successfully."
    ),
    Tool(
        name="set_brightness",
        func=set_brightness_tool,
        description="Set the screen brightness level from 0 to 100. Input should be a number like '70'. If the response includes ✅, the brightness was successfully set."
    ),
    Tool(
        name="get_brightness",
        func=get_brightness_tool,
        description="Get the current screen brightness level. If the response includes 🌞, the value was fetched successfully."
    ),
    Tool(
        name="get_battery_status",
        func=get_battery_status_tool,
        description="Get the battery percentage and charging status. If the response includes 🔋 or 🔌, the value was fetched successfully."
    ),
    Tool(
        name="take_screenshot",
        func=take_screenshot_tool,
        description="Take a screenshot and save it with an optional filename. Input example: 'screenshot1.png'. If the response includes 📸 and ✅, the screenshot was saved successfully."
    ),
    Tool(
        name="lock_system",
        func=lock_system_tool,
        description="Lock the system immediately (Windows only). If the response includes 🔒 and ✅, the system was locked successfully."
    ),
    Tool(
        name="shutdown_system",
        func=shutdown_system_tool,
        description="Shutdown the system immediately (Windows only). If the response includes 🛑 and ✅, the shutdown command was issued successfully."
    ),
    Tool(
        name="restart_system",
        func=restart_system_tool,
        description="Restart the system immediately (Windows only). If the response includes 🔁 and ✅, the restart command was issued successfully."
    ),
    Tool(name="wifi_on", func=wifi_on, description="Turn Wi-Fi ON. Returns ✅ when done."),
    Tool(name="wifi_off", func=wifi_off, description="Turn Wi-Fi OFF. Returns ✅ when done."),
    Tool(name="list_wifi_networks", func=list_wifi_networks, description="Show available Wi-Fi networks."),
    Tool(name="check_internet", func=check_internet, description="Check if internet is available."),
    
    Tool(name="set_dark_mode", func=set_dark_mode, description="Enable dark mode on Windows. Returns ✅ when done."),
    Tool(name="set_light_mode", func=set_light_mode, description="Enable light mode on Windows. Returns ✅ when done."),
    Tool(name="rotate_screen", func=rotate_screen, description="Rotate screen orientation. Input: landscape, portrait, etc. Returns ✅ when done."),
    Tool(name="change_resolution", func=change_resolution, description="Change screen resolution. Input: '1920x1080'. Returns ✅ when done."),
    Tool(name="set_display_mode", func=set_display_mode, description="Set multi-display mode. Input: 'extend', 'duplicate', etc. Returns ✅ when done."),
    Tool(name="create_file", func=create_file, description="Create a new file at the given path. Input: 'C:/Users/.../file.txt'. ✅ means success."),
Tool(name="read_file", func=read_file, description="Read contents of the file. Input: path string. 📄 + ✅ means success."),
Tool(name="write_file", func=write_file, description="Write content to file. Input: dict with 'path' and 'content'. ✅ means success."),
Tool(name="append_file", func=append_file, description="Append content to file. Input: dict with 'path' and 'content'. ✅ means success."),
Tool(name="delete_file", func=delete_file, description="Delete a file at the given path. Input: path string. ✅ means success."),
Tool(name="execute_file", func=execute_file, description="Execute a script/batch/exe file at the given path. Input: path string. ✅ means it ran."),
Tool(
        name="browse_web",
        func=browse_web,
        description="Use Hyperbrowser to perform a web browsing task. Input: 'search X', 'get link Y'. Returns the result of the browsing task."
    )
]