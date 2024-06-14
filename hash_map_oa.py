# Name: Anthony Prudent
# OSU Email: prudenta@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: HashMap Implementation
# Due Date: 6/6/2024
# Description: The program implements the hash map data structure using a dynamic array. Entries are indexed at buckets
#              with the use of a hash function. Collisions are resolved through open addressing, quadratically probing
#              for the requested bucket. The hash table maintains its load by resizing when the number of entries is
#              greater than or equal to half the number of buckets.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        # Compute the key's initial bucket index
        hash = self._hash_function(key)
        initial_index = hash % self._buckets.length()

        probe_index = initial_index
        probe = 0
        bucket = self._buckets[probe_index]

        # Probes for an empty bucket or tombstone to place entry or entry with associated key to update its value
        while bucket is not None and bucket.is_tombstone is False and bucket.key != key:
            probe_index = (initial_index + probe ** 2) % self._buckets.length()
            probe += 1
            bucket = self._buckets[probe_index]

        if self._buckets[probe_index] is None or bucket.is_tombstone is True:  # Size only changes with new entries
            self._size += 1

        self._buckets[probe_index] = HashEntry(key, value)

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table based on the new capacity, rehashing existing key/value pairs.

        :param new_capacity: An integer

        :return:    None
        """

        if new_capacity > self._size:

            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

            # Recreate the hash table
            pairs_arr = self.get_keys_and_values()
            self._capacity = new_capacity
            self._size = 0

            self._buckets = DynamicArray()

            for bucket in range(self._capacity):
                self._buckets.append(None)

            # Rehashes existing pairs
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

            bucket = self._buckets[bucket_index]

            if bucket is None or bucket is not None and bucket.is_tombstone is True:
                empty_count += 1

        return empty_count

    def get(self, key: str) -> object:
        """
        Retrieves the value associated with the key.

        :param key: A string

        :return:    An object
        """

        # Compute the key's initial bucket index
        hash = self._hash_function(key)
        initial_index = hash % self._buckets.length()

        probe_index = initial_index
        probe = 0

        # Probes buckets until key is found or end of cluster
        while self._buckets[probe_index] is not None:

            if self._buckets[probe_index].key == key and self._buckets[probe_index].is_tombstone is False:
                return self._buckets[probe_index].value

            probe_index = (initial_index + probe ** 2) % self._buckets.length()
            probe += 1

    def contains_key(self, key: str) -> bool:
        """
        Confirms the existence of the key in the hash map.

        :param key: A string

        :return:    A boolean depending on the existence of the key
        """

        # Compute the key's initial bucket index
        hash = self._hash_function(key)
        initial_index = hash % self._buckets.length()

        probe_index = initial_index
        probe = 0

        # Probes buckets until key is found or end of cluster
        while self._buckets[probe_index] is not None:

            if self._buckets[probe_index].key == key:
                return True

            probe_index = (initial_index + probe ** 2) % self._buckets.length()
            probe += 1

        return False

    def remove(self, key: str) -> None:
        """
        Deletes the key and its value from the hash map.

        :param key: A string

        :return:    None
        """

        # Compute the key's initial bucket index
        hash = self._hash_function(key)
        initial_index = hash % self._buckets.length()

        if self._buckets[initial_index] is not None:

            probe_index = initial_index
            probe = 0

            # Probes buckets until the key is found or empty bucket
            while self._buckets[probe_index] is not None and self._buckets[probe_index].key != key:
                probe_index = (initial_index + probe ** 2) % self._buckets.length()
                probe += 1

            if self._buckets[probe_index] is not None and self._buckets[probe_index].is_tombstone is False:
                self._buckets[probe_index].is_tombstone = True
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Retrieves all key/value pairs from the hash map and copies them into a dynamic array as tuples.

        :return:    Dynamic array of tuples representing key/value pairs
        """

        pairs_arr = DynamicArray()

        for bucket_index in range(self._buckets.length()):

            bucket = self._buckets[bucket_index]

            if bucket is not None and bucket.is_tombstone is False:

                pair = (bucket.key, bucket.value)
                pairs_arr.append(pair)

        return pairs_arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map.

        :return:    None
        """

        for bucket_index in range(self._buckets.length()):
            self._buckets[bucket_index] = None

        self._size = 0

    def __iter__(self):
        """
        Initializes the index used for iteration
        """

        self._index = 0
        return self

    def __next__(self):
        """
        Returns value at the hash map's index and advances its index.
        """

        try:

            bucket = self._buckets[self._index]

            # Finds a bucket that is not empty and not a tombstone
            while bucket is not None and bucket.is_tombstone is True or bucket is None:
                self._index += 1
                bucket = self._buckets[self._index]

            curr_value = self._buckets[self._index]

        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return curr_value

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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
