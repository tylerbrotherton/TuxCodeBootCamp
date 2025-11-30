use std::collections::{HashMap, VecDeque};
use std::hash::Hash;
use parking_lot::Mutex;
use crossbeam::thread;

/// A thread‑safe Least‑Recently‑Used (LRU) cache.
///
/// The cache stores key/value pairs up to a fixed capacity. When the 
capacity
/// is exceeded, the least recently used entry is evicted. Every public 
method
/// acquires the cache’s internal `Mutex` – the implementation is 
intentionally
/// simple, prioritising clarity over raw performance.
///
/// # Examples
///
/// ```
/// let cache = LruCache::new(2);
/// cache.insert(1, "one");
/// cache.insert(2, "two");
/// assert_eq!(cache.get(&1), Some("one".to_string()));
/// cache.insert(3, "three");               // Evicts key `2`.
/// assert!(cache.get(&2).is_none());
/// ```
pub struct LruCache<K, V> {
    /// Internal state protected by a `parking_lot::Mutex`.
    inner: Mutex<Inner<K, V>>,
}

struct Inner<K, V> {
    capacity: usize,
    /// Stores the actual key/value pairs.
    map: HashMap<K, V>,
    /// Keeps track of key usage order – the front is the most recently 
used.
    usage: VecDeque<K>,
}

impl<K, V> LruCache<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    /// Creates a new cache with the specified maximum number of entries.
    pub fn new(capacity: usize) -> Self {
        Self {
            inner: Mutex::new(Inner {
                capacity,
                map: HashMap::with_capacity(capacity),
                usage: VecDeque::with_capacity(capacity),
            }),
        }
    }

    /// Inserts a key/value pair. If the key already exists, its value is
    /// overwritten and the key is moved to the front of the usage queue.
    /// When capacity is exceeded, the LRU entry is evicted.
    pub fn insert(&self, key: K, value: V) {
        let mut inner = self.inner.lock();

        // If the key already exists, update the value and move it to the 
front.
        if inner.map.contains_key(&key) {
            inner.map.insert(key.clone(), value);
            Self::move_to_front(&mut inner.usage, &key);
            return;
        }

        // Insert new key/value pair.
        inner.map.insert(key.clone(), value);
        inner.usage.push_front(key);

        // Evict if we’re over capacity.
        if inner.map.len() > inner.capacity {
            if let Some(oldest) = inner.usage.pop_back() {
                inner.map.remove(&oldest);
            }
        }
    }

    /// Returns a clone of the value associated with `key`, or `None` if 
it
    /// does not exist. The key is promoted to the most‑recently‑used
    /// position.
    pub fn get(&self, key: &K) -> Option<V> {
        let mut inner = self.inner.lock();

        if let Some(value) = inner.map.get(key) {
            Self::move_to_front(&mut inner.usage, key);
            Some(value.clone())
        } else {
            None
        }
    }

    /// Helper: move an existing key to the front of the `VecDeque`.
    fn move_to_front(queue: &mut VecDeque<K>, key: &K) {
        if let Some(pos) = queue.iter().position(|k| k == key) {
            queue.remove(pos);
            queue.push_front(key.clone());
        }
    }
}

// ---------------------------------------------------------------------------------------------------------------------------------------------------
// Demo that spawns a few threads accessing the cache concurrently.
// ---------------------------------------------------------------------------------------------------------------------------------------------------

fn main() {
    let cache = LruCache::new(3);

    // Pre‑populate the cache.
    cache.insert(1, "one".to_string());
    cache.insert(2, "two".to_string());
    cache.insert(3, "three".to_string());

    // Spawn three threads that all read/write the cache.
    thread::scope(|s| {
        for i in 0..3 {
            let c = &cache;
            s.spawn(move |_| {
                // Each thread performs a small number of operations.
                for j in 0..5 {
                    let key = (i + j) % 5;
                    c.insert(key, format!("value-{}", key));
                    println!("Thread {} inserted key {}", i, key);
                }

                for j in 0..5 {
                    let key = (i + j) % 5;
                    if let Some(v) = c.get(&key) {
                        println!("Thread {} read key {} -> {}", i, key, 
v);
                    } else {
                        println!("Thread {} read key {} -> <miss>", i, 
key);
                    }
                }
            });
        }
    })
    .unwrap();

    // After the threads finish, print the final cache state.
    println!("\nFinal cache contents:");
    for key in 1..6 {
        if let Some(v) = cache.get(&key) {
            println!("  {} => {}", key, v);
        } else {
            println!("  {} => <evicted>", key);
        }
    }
}
