# performance review:
* references:
* https://cloud.google.com/blog/products/data-analytics/benchmarking-cloud-data-warehouse-bigquery-to-scale-fast
* https://stackoverflow.com/questions/56022874/bigquery-replaced-most-of-my-spark-jobs-am-i-missing-something
* https://panoply.io/data-warehouse-guide/bigquery-architecture/

## query performance
* most queries under a few minutes, should be under 30 minutes

## load into postgres:
* 1.2 billion in less than 2 hours to one single postgres server
* postgres indexing could take longer time

## alternative: TiDB
* Limits the response time for queries to 90 ms or less
* https://pingcap.com/case-studies/lesson-learned-from-queries-over-1.3-trillion-rows-of-data-within-milliseconds-of-response-time-at-zhihu
