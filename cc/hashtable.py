from pprint import pprint


def rotate(mim, n):
    layer = 0
    while layer < n // 2:
        i = base_layer = layer
        border = n - 1 - layer
        while i < border:
            offset = i - base_layer
            top = mim[base_layer][i]
            mim[base_layer][i] = mim[border - offset][base_layer]
            mim[border - offset][base_layer] = mim[border][border - offset]
            mim[border][border - offset] = mim[i][border]
            mim[i][border] = top
            i += 1
        layer += 1


def change(string, line_length):
    break_length = 2*line_length - 2

    for i in range(line_length):
        for j in range(i, len(string)):
            base_index = (j//break_length) * break_length
            last_index = base_index + break_length
            if (j - base_index) == i or last_index - j == i:
                print(string[j])

if __name__ == '__main__':
    n = 4
    # a = [list(range(n)) for i in range(n)]
    # pprint(a)
    # rotate(a, n)
    # pprint(a)
    #
    change('abcdefghijklmn', 8)
