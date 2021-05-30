# ueue: FIFO

def queue_t():
    import queue
    q = queue.Queue(maxsize=0)
    q.put("1")
    q.put("2")
    q.put("3")
    print (q.get())
    print(q)


def dequeue_t():
    from collections import deque

    q = deque()
    q.append('a')
    q.append('b')
    q.append('c')

    print("Initial ueue")
    print(q)

    # Removing elements from a ueue
    print("\nElements deueued from the ueue")
    print(q.popleft())
    print(q.popleft())
    print(q.popleft())

    print("\nueue after removing elements")
    print(q)


if __name__ == "__main__":
    queue_t()
