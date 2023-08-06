# Socket handler for the polog lib

Обработчик для библиотеки polog. Состоит из двух компонентов: клиента и сервера. Может использоваться для проксирования отправки логов с клиентского сервера на какой-то иной. Клиентская часть обработчика подключается в polog как любой другой обработчик: 


```python
from polog import config
from socket_handler import socket_sender


HOST = '127.0.0.1'
PORT = 65432

config.add_handlers(socket_sender(HOST, PORT))
```

Серверная часть обработчика получает логи, отправляемые клиентской частью, и может как-то их обрабатывать. Например, к ней можно подключить любой иной обработчик polog. Подключаемый обработчик не будет знать о том, что логируемый код выполняется на другой машине или в другом процессе. Такой подход позволяет вынести ресурсоёмкие операции сохранения / пересылки логов с машины, где непосредственно выполняется бизнес-код, на машину, которую не так жалко.

Пример клиента:


```python
# В дополнении к коду выше, обработчик уже должен быть подключён.
from polog import flog


@flog
def logged_func(arg):
    return arg

logged_func("test polog socket handler") # По результату выполнения функции на сервер будет отправлено сообщение с логом.
```

Пример сервера:


```python
from polog.handlers.smtp.sender import SMTP_sender # Пакет polog уже должен быть установлен.
from socket_handler import Server


HOST = '127.0.0.1'
PORT = 65432

print("The Polog Socket Server started.")
server = Server(HOST, PORT, handlers=[SMTP_sender('from_me42@yandex.com', 'JHjhhb87TY(*Ny08z)', 'smtp.yandex.ru', 'to_me@yandex.ru')])
server.start()
```
