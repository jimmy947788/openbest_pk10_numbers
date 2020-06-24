import itertools

if __name__ == '__main__':


    all_balls = list(itertools.product( range(1, 81), repeat=20))
    print(len(all_balls))