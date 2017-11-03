def process_commands(*args):
    while True:
        line=''
        while not line.endswith('\n'):
            line+=read_next_char()
        if line=='quit\n':
            print "are you sure?"
            if read_next_char()!="y":
                continue    #忽略指令
        process_commands(line)