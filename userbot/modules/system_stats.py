# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """

import platform
import sys
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from datetime import datetime
from os import remove
from platform import python_version, uname
from shutil import which

import psutil
from git import Repo
from telethon import __version__, version

from userbot import (
    ALIVE_NAME,
    CMD_HELP,
    CODENAME,
    LOGO,
    UPSTREAM_REPO_BRANCH,
    OUBnew_VER,
    bot,
)
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
VER = str(OUBnew_VER)
CN = str(CODENAME)
repo = Repo()
modules = CMD_HELP
# ============================================

MODULESTR = 0


@register(outgoing=True, pattern=r"^\.spc")
async def psu(event):
    uname = platform.uname()
    softw = "**System Information**\n"
    softw += f"`System   : {uname.system}`\n"
    softw += f"`Release  : {uname.release}`\n"
    softw += f"`Version  : {uname.version}`\n"
    softw += f"`Machine  : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`Boot Time: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**CPU Info**\n"
    cpuu += "`Physical cores   : " + str(
        psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "`Total cores      : " + str(
        psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"`Max Frequency    : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency    : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"`Core {i}  : {percentage}%`\n"
    cpuu += "**Total CPU Usage**\n"
    cpuu += f"`All Core: {psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**Memory Usage**\n"
    memm += f"`Total     : {get_size(svmem.total)}`\n"
    memm += f"`Available : {get_size(svmem.available)}`\n"
    memm += f"`Used      : {get_size(svmem.used)}`\n"
    memm += f"`Percentage: {svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "**Bandwith Usage**\n"
    bw += f"`Upload  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "**Engine Info**\n"
    help_string += f"`Python {sys.version}`\n"
    help_string += f"`Telethon {__version__}`"
    await event.edit(help_string)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@register(outgoing=True, pattern=r"^\.sysd$")
async def sysdetails(sysd):
    # Prevent Channel Bug to run sysd commad
    if sysd.is_channel and not sysd.is_group:
        await sysd.edit("`sysd Commad isn't permitted on channels`")
        return
    """ For .sysd command, get system info using neofetch. """
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + str(
                stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch first !!`")


@register(outgoing=True, pattern="^.botver$")
async def bot_ver(event):
    # Prevent Channel Bug to run botver commad
    if event.is_channel and not event.is_group:
        await event.edit("`botver Commad isn't permitted on channels`")
        return
    """ For .botver command, get the bot version. """
    if which("git") is not None:
        invokever = "git describe --all --long"
        ver = await asyncrunapp(
            invokever,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        invokerev = "git rev-list --all --count"
        rev = await asyncrunapp(
            invokerev,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        await event.edit("`Userbot Version: "
                         f"{verout}"
                         "` \n"
                         "`Revision: "
                         f"{revout}"
                         "`")
    else:
        await event.edit(
            f"Shame that you don't have git, You're running {VER} - '{CN}' anyway"
        )
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        if which("git") is not None:
            ver = await asyncrunapp(
                "git",
                "describe",
                "--all",
                "--long",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) + str(
                stderr.decode().strip())

            rev = await asyncrunapp(
                "git",
                "rev-list",
                "--all",
                "--count",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) + str(
                stderr.decode().strip())

            await event.edit("`Userbot Version: "
                             f"{verout}"
                             "` \n"
                             "`Revision: "
                             f"{revout}"
                             "`")
        else:
            await event.edit(
                "Shame that you don't have git, you're running - 'v1.beta.4' anyway!"
            )


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
async def pipcheck(pip):
    # Prevent Channel Bug to run pip commad
    if pip.is_channel and not pip.is_group:
        await pip.edit("`pip Commad isn't permitted on channels`")
        return
    """ For .pip command, do a pip search. """
    if not pip.text[0].isalpha() and pip.text[0] not in ("/", "#", "@", "!"):
        pipmodule = pip.pattern_match.group(1)
        if pipmodule:
            await pip.edit("`Searching . . .`")
            pipc = await asyncrunapp(
                "pip3",
                "search",
                pipmodule,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await pipc.communicate()
            pipout = str(stdout.decode().strip()) + str(
                stderr.decode().strip())

            if pipout:
                if len(pipout) > 4096:
                    await pip.edit("`Output too large, sending as file`")
                    file = open("output.txt", "w+")
                    file.write(pipout)
                    file.close()
                    await pip.client.send_file(
                        pip.chat_id,
                        "output.txt",
                        reply_to=pip.id,
                    )
                    remove("output.txt")
                    return
                await pip.edit("**Query: **\n`"
                               f"pip3 search {pipmodule}"
                               "`\n**Result: **\n`"
                               f"{pipout}"
                               "`")
            else:
                await pip.edit("**Query: **\n`"
                               f"pip3 search {pipmodule}"
                               "`\n**Result: **\n`No Result Returned/False`")
        else:
            await pip.edit("`Use .help pip to see an example`")


@register(outgoing=True, pattern=r"^\.(?:live|on)\s?(.)?")
async def amireallyalive(alive):
    # Prevent Channel Bug to run alive commad
    if alive.is_channel and not alive.is_group:
        await alive.edit("`alive Commad isn't permitted on channels`")
        return
    """ For .alive command, check if the bot is running.  """
    logo = LOGO
    output = (f"running on __{UPSTREAM_REPO_BRANCH}__ \n"
              "----------------------------------------\n"
              "`Bot Version Info` \n"
              f"`CODENAME       : {CN} v{VER} `\n"
              f"`Telethon       : v{version.__version__} `\n"
              f"`Python         : v{python_version()} `\n"
              "----------------------------------------\n"
              f"`User           : `{DEFAULTUSER} \n"
              f"`Module loaded  : `{len(modules)} \n\n"
              f"`All modules loaded with ({MODULESTR}) errors`")
    await bot.send_file(alive.chat_id, logo, caption=output)
    await alive.delete()


@register(outgoing=True, pattern="^.aliveu")
async def amireallyaliveuser(username):
    # Prevent Channel Bug to run aliveu commad
    if username.is_channel and not username.is_group:
        await username.edit("`aliveu Commad isn't permitted on channels`")
        return
    """ For .aliveu command, change the username in the .alive command. """
    message = username.text
    output = ".aliveu [new user without brackets] nor can it be empty"
    if message != ".aliveu" and message[7:8] == " ":
        newuser = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = newuser
        output = "Successfully changed user to " + newuser + "!"
    await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern="^.resetalive$")
async def amireallyalivereset(ureset):
    # Prevent Channel Bug to run resetalive commad
    if ureset.is_channel and not ureset.is_group:
        await ureset.edit("`resetalive Commad isn't permitted on channels`")
        return
    """ For .resetalive command, reset the username in the .alive command. """
    global DEFAULTUSER
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("`" "Successfully reset user for alive!" "`")


CMD_HELP.update({
    "sysd":
    "`.sysd`"
    "\nUsage: Shows system information using neofetch."
    "\n\n`.spc`"
    "\nUsage: Show system specification.",
})
CMD_HELP.update({"botver": "`.botver`" "\nUsage: Shows the userbot version."})
CMD_HELP.update(
    {"pip": "`.pip` <module(s)>"
     "\nUsage: Does a search of pip modules(s)."})
CMD_HELP.update({
    "on":
    "`.live` | `.on`"
    "\nUsage: See wether your bot is working or not."
    "\n\n`.aliveu` <text>"
    "\nUsage: Changes the 'user' in alive to the text you want."
    "\n\n`.resetalive`"
    "\nUsage: Resets the user to default."
})
