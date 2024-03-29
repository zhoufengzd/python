# ueue: FIFO

def queue_t():
    import queue
    # to share data between two threads
    q = queue.Queue(maxsize=0)
    q.put("1")
    q.put("2")
    q.put("3")
    print(q.get())
    print(q)


def dequeue_t():
    from collections import deque
    # FIFO

    q = deque()
    q.append('a')
    q.append('b')
    q.append('col')
    q.extend(["d", "e", "f"])

    print("Initial queue")
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
    dequeue_t()
