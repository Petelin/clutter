import asyncio


async def hello_world():
    # yield "hello_world"
    print("Hello World!")
    return 1


async def work(reader, writer):
    await asyncio.sleep(1)
    writer.write(b"""HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: Apache/2.2.14 (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Type: text/html
Connection: Closed

<html> <body> <h1>Hello, World!</h1> </body> </html>""")
    await writer.drain()
    writer.close()


loop = asyncio.get_event_loop()
future = asyncio.start_server(work, '127.0.0.1', 8000, loop=loop)
server = loop.run_until_complete(future)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
