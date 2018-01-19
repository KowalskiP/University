__author__ = 'kowalski'
isCLI = False
# Хранит текущие соединения
connection_init = None
statusConnect = None

send_array = []
get_array = []

address_array = []
username_array = dict()
# ключ: открытый сокет в connection_array
# значение: никнеймы для подключения
contact_array = dict()
# ключ: адрес
# значение: [порт, имя]

username = "Self"

location = 0
port = 4242
top = None

main_body_text = None