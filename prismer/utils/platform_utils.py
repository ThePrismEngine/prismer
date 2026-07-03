import platform

def get_system_machine():
    system = platform.system().capitalize()
    machine = platform.machine().lower()

    if system == 'darwin':
        sys_name = 'macos'
    else:
        sys_name = system

    if machine in ('x86_64', 'amd64'):
        mach_name = 'x86_64'
    elif machine in ('arm64', 'aarch64'):
        mach_name = 'arm64'
    else:
        mach_name = machine

    return sys_name, mach_name