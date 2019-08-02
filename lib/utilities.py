import datetime 

def timer(func):
    '''
    decorator
    
    add time that the function cost when execution to the return of the decorated function
    '''
    def wrapper(*arg):
        t1=datetime.datetime.now()
        res=func(*arg)
        t2=datetime.datetime.now()
        return res, t2-t1
    return wrapper

def report(n_iter,n_rate,n_all):
    '''
    Print the progress if the current index of iteration mod report rate is zero
    
    Args:
        n_iter(int): current iteration index
        n_rate(int): report rate
        n_all(int): upper boundary of iterations
    Returns:
        None
    '''
    if (n_iter+1)%n_rate==0:
        print("progress: {}/{}".format(n_iter+1,n_all))
    