# Name: Anthony Prudent
# OSU Email: prudenta@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: HashMap Implementation
# Due Date: 6/6/2024
# Description: The program implements the hash map data structure using an array of singly linked lists.
#              Entries are indexed at buckets with the use of a hash function. Collisions are resolved through chaining
#              entries. The hash table maintains its load by resizing when there are an equal number of buckets and
#              entries.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds the key/value pair to the hash map if key is not already in the map or updates the value of the key
        if the key is already present.

        :param key: A string
        :param value: An object

        :return:    None
        """

        # Resizes hash table
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # Computes the index of the key's bucket
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        bucket = self._buckets[index]

        # Size only increases for new insertions not updates
        if not bucket.remove(key):
            self._size += 1

        bucket.insert(key, value)

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table based on the new capacity, rehashing existing key/value pairs.

        :param new_capacity: An integer

        :return:    None
        """

        if new_capacity >= 1:

            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

            # Recreates the hash table
            pairs_arr = self.get_keys_and_values()
            self._capacity = new_capacity
            self._size = 0

            self._buckets = DynamicArray()

            for bucket in range(self._capacity):
                self._buckets.append(LinkedList())

            # Rehashes existing elements
            for pair_index in range(pairs_arr.length()):
                (key, value) = pairs_arr[pair_index]
                self.put(key, value)

    def table_load(self) -> float:
        """
        Calculates the load factor of the current hash table.

        :return:    A float representing the table load
        """

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Calculates the number of empty buckets in the hash table.

        :return:    An integer
        """

        empty_count = 0

        for bucket_index in range(self._buckets.length()):

            if self._buckets[bucket_index].length() == 0:
                empty_count += 1

        return empty_count

    def get(self, key: str) -> object:
        """
        Retrieves the value associated with the key.

        :param key: A string

        :return:    An object
        """

        # Computes the index of the key's bucket
        hash = self._hash_function(key)
        index = hash % self._buckets.length()

        for node in self._buckets[index]:

            if node.key == key:
                return node.value

    def contains_key(self, key: str) -> bool:
        """
        Confirms the existence of the key in the hash map.

        :param key: A string

        :return:    A boolean depending on the existence of the key
        """

        # Computes the index of the key's bucket
        hash = self._hash_function(key)
        index = hash % self._buckets.length()

        if self._buckets[index].contains(key) is not None:
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Deletes the key and its value from the hash map.

        :param key: A string

        :return:    None
        """

        # Computes the index of the key's bucket
        hash = self._hash_function(key)
        index = hash % self._buckets.length()

        if self._buckets[index].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Retrieves all key/value pairs from the hash map and copies them into a dynamic array as tuples.

        :return:    Dynamic array of tuples representing key/value pairs
        """

        pairs_arr = DynamicArray()

        for bucket_index in range(self._buckets.length()):

            for node in self._buckets[bucket_index]:

                pairs_arr.append((node.key, node.value))

        return pairs_arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map.

        :return:    None
        """

        for bucket_index in range(self._buckets.length()):
            self._buckets[bucket_index] = LinkedList()

        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds the mode and its frequency of the given dynamic array.

    :param da: A dynamic array

    :return:    Tuple with a dynamic array of the mode(s) and an integer representing the mode(s) frequency
    """

    map = HashMap()

    # Places the elements of the array into a hash map with key as the element and its value as its frequency
    for arr_index in range(da.length()):

        arr_element = da[arr_index]
        element_frequency = map.get(arr_element)

        if not map.contains_key(arr_element):  # Places new unique element in the hash map
            map.put(arr_element, 1)

        else:
            map.put(arr_element, element_frequency + 1)  # Updates the existing elements frequency

    pair_arr = map.get_keys_and_values()
    mode_arr = DynamicArray()
    mode_frequency = 0

    # Compares the frequency of each element in the hash map to find the mode
    for arr_index in range(pair_arr.length()):

        element_frequency = pair_arr[arr_index][1]

        # There is a new mode, updating current mode frequency and recreating the mode array,
        if element_frequency > mode_frequency:
            mode_frequency = element_frequency
            mode_arr = DynamicArray()
            mode_arr.append(pair_arr[arr_index][0])

        # The current element has the same frequency as the mode
        elif element_frequency == mode_frequency:
            mode_arr.append(pair_arr[arr_index][0])

    result_tuple = (mode_arr, mode_frequency)

    return result_tuple

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
