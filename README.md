# HSA L19: Database Sharding

## Overview
This is an example project to show how to set up PostgreSQL Horizontal Sharding.

### Task:
* Create 3 docker containers: postgresql_main, postgresql_shard1, postgresql_shard2.
* Setup horizontal sharding.
* Insert 1_000_000 rows into books.
* Measure performance with and without sharding.
* Compare performance.


## Getting Started

### Preparation
1. Make sure that you have installed Python3 with the next plugins:
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- [Faker](https://pypi.org/project/Faker/)
- [memory-profiler](https://pypi.org/project/memory-profiler/)

2. Run the docker containers to setup PostgreSQL Horizontal Sharding.
```bash
  docker-compose up -d
```

Be sure to use ```docker-compose down -v``` to clean up after you're done with tests.

## Test cases

### Check query planning on shards
```sql
$ EXPLAIN SELECT * FROM books;
With Sharding:
+----------------------------------------------------------------------+
|QUERY PLAN                                                            |
+----------------------------------------------------------------------+
|Append  (cost=100.00..275.09 rows=1574 width=80)                      |
|  ->  Foreign Scan on books_1  (cost=100.00..133.61 rows=787 width=80)|
|  ->  Foreign Scan on books_2  (cost=100.00..133.61 rows=787 width=80)|
+----------------------------------------------------------------------+
Without Sharding:
+-----------------------------------------------------------------------+
|QUERY PLAN                                                             |
+-----------------------------------------------------------------------+
|Seq Scan on books  (cost=0.00..18587.85 rows=1000085 width=38)         |
+-----------------------------------------------------------------------+

```

### Check performance
```bash
$ python ./application/check_performance.py
======================================
Measure sharding performance:
======================================
=> Measure insert:
Number of inserted rows: 100000
Run Time: 418.3s
Used Memory: 51Mb

=> Measure select:
Number of selected rows: 1000000
Run Time: 0.979s
Used Memory: 48Mb

=> Measure delete:
Number of deleted rows: 1000000
Run Time: 0.7033s
Used Memory: 48Mb

======================================
Measure performance without sharding:
======================================
=> Measure insert:
Number of inserted rows: 1000000
Run Time: 211.1s
Used Memory: 57Mb

=> Measure select:
Number of selected rows: 1000000
Run Time: 0.5206s
Used Memory: 57Mb

=> Measure delete:
Number of deleted rows: 1000000
Run Time: 0.6006s
Used Memory: 57Mb
```