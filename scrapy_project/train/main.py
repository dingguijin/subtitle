from train import trainIters


def run():
    iteration = 10000
    learning_rate = 0.01
    batch_size = 1
    layers = 1
    hidden_size = 200
    
    trainIters(iteration, learning_rate, batch_size, layers, hidden_size)


if __name__ == '__main__':
    run()
