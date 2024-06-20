# HashMap Implementations
Python implementation of HashMaps that use seperate chaining and open addressing.

## Description

The HashMaps contain methods to insert, get, and remove key-value pairs with an average O(1) time complexity. 
To maintain the average O(1) time complexity, the HashMaps utilize seperate chaining and open addressing to reduce collisions as well as resize the hash table to a prime number depending on its load factor.
In the seperate chaining implementation, multiple keys share the same table entry as a singly lniked list of nodes. On the other hand, the open addressing implementation uses quadratic probing to not only reduce collisions,
but also reduce clustering of entries as well.
