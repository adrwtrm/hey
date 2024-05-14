import asyncio
import epson_projector as epson
from epson_projector.const import (POWER, PWR_ON, PWR_OFF, VOL_UP, VOL_DOWN)
import re

async def main_tcp():
    """Run main with TCP session."""
    await run()

async def run():
    ips = await get_projector_ips()
    for ip in ips:
        projector = epson.Projector(host=ip, type='tcp')
        data = await projector.get_power()
        await projector.send_command(PWR_OFF)
        print(f"Power status of {ip}: {data}")

async def get_projector_ips():
    """Get IP addresses of Epson projectors using arp-scan."""
    ip_list = []
    arp_scan_output = await run_shell_command("sudo arp-scan --localnet | grep 'Seiko Epson Corporation'")
    matches = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', arp_scan_output)
    if matches:
        ip_list = matches
    return ip_list

async def run_shell_command(command):
    """Run a shell command and return its output."""
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await process.communicate()
    return stdout.decode().strip()

loop = asyncio.get_event_loop()
loop.run_until_complete(main_tcp())
loop.close()