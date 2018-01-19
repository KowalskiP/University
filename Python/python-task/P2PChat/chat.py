#!/usr/bin/env python3
__author__ = 'kowalski'
import sys
import base.new_CSR
import base.commands
import config


def cli_chat():
    print("Запуск в текстовом формате")
    while 1:
        base.commands.pars_text_cli(input())


if len(sys.argv) > 1 and sys.argv[1] == "-cli":
    config.isCLI = True
else:
    config.isCLI = False
    import base.gui

server = base.new_CSR.Server(config.port)
server.start()

if config.isCLI:
    cli_chat()
else:
    base.gui.root.mainloop()
    base.gui.save_contacts()
