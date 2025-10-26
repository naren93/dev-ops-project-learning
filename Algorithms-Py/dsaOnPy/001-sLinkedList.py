class Node:
    """A class representing a node in a singly linked list."""
    def __init__(self, data):
        """Initialize a new node with given data."""
        self.data = data
        self.next = None

class SinglyLinkedList:
    """A class implementing a singly linked list data structure."""
    def __init__(self):
        """Initialize an empty linked list."""
        self.head = None
    
    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def delete_node(self, key):
        """Delete the first occurrence of node with given key value."""
        current = self.head
        # If head node itself holds the key
        if current and current.data == key:
            self.head = current.next
            current = None
            return
        while current:
            if current.data == key:
                break
            prev = current
            current = current.next
        if current is None:
            return
        prev.next = current.next

    def print_list(self):
        """Print all elements in the linked list."""
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")
# Example usage:
if __name__ == "__main__":
    sll = SinglyLinkedList()
    # Insert some elements
    sll.insert_at_end(1)
    sll.insert_at_end(2)
    sll.insert_at_beginning(0)
    # Print the list
    print("Initial list:")
    sll.print_list()  # Output: 0 -> 1 -> 2 -> None
    # Delete a node
    print("After deleting node with value 1:")
    sll.delete_node(1)
    sll.print_list()  # Output: 0 -> 2 -> None
