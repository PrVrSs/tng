import socket


blank, start, exit1, visited, solution = " >X.o"


class LabyRenth(object):

    answer = ''

    def __init__(self, recv_data):
        self.data = [list(row) for row in recv_data.splitlines()]
        a = ["".join(sd) for sd in self.data]
        count = 0
        for index, i in enumerate(a):
            if "Now" in i:
                count = index + 2
        self.width = len(a[count])
        self.length = len(a[count:-1])
        self.data = "\n".join("".join(sd) for sd in a[count:-1])
        self.dd = [list(row) for row in self.data.splitlines()]

    def __repr__(self):
        return self.data

    def solve(self, x=None, y=None):
        if x is None:
            x, y = 1, 1
        if self.dd[y][x] in (blank, start):
            self.dd[y][x] = visited
            if self.solve(x+1, y):
                self.answer += "<"
                self.dd[y][x] = solution
                return True
            elif self.solve(x-1, y):
                self.answer += ">"
                self.dd[y][x] = solution
                return True
            elif self.solve(x, y+1):
                self.answer += "^"
                self.dd[y][x] = solution
                return True
            elif self.solve(x, y-1):
                self.answer += "V"
                self.dd[y][x] = solution
                return True
        elif self.dd[y][x] == exit1:
            return True
        return False


def main():
    MAZE_SERVER = ('54.69.145.229', 16000)
    RECV_SIZE = 8192
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(MAZE_SERVER)
    while 1:
        try:
            print("NEW ROUND\n")
            data = s.recv(RECV_SIZE).decode()
            laby_reth = LabyRenth(data)
            print(laby_reth)
            laby_reth.solve()
            ans = "\n".join("".join(sd) for sd in laby_reth.dd)
            print(ans)
            answer = ''
            for i in reversed(laby_reth.answer):
                if i == ">":
                    answer += "<"
                elif i == "<":
                    answer += ">"
                elif i == "^":
                    answer += "V"
                elif i == "V":
                    answer += "^"
            print(answer)
            s.send((str(answer) + "\n").encode())
        except IndexError:
            print("DATA ", data)
            s.close()

if __name__ == '__main__':
    main()
