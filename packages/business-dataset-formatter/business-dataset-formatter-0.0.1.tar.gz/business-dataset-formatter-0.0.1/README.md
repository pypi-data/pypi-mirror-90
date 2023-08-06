# Business Dataset Formatter

This package was born with the need to organize a dataset with the following structure:

```python
[{'_id': datetime.datetime(2020, 4, 29, 0, 0), 'deliveries': 1}, #wednesday
{'_id': datetime.datetime(2020, 4, 27, 0, 0), 'deliveries': 1}, #monday
{'_id': datetime.datetime(2020, 4, 26, 0, 0), 'deliveries': 1}] #sunday
```

It is possible to notice a lack of one day within the dataset above. In this case, this algorithm will deliver the following result:

```python
[{'date': datetime.datetime(2020, 4, 29, 0, 0), 'deliveries': 1}, #wednesday
 {'date': datetime.datetime(2020, 4, 29, 0, 0), 'deliveries': 0}, #tuesday
 {'date': datetime.datetime(2020, 4, 27, 0, 0), 'deliveries': 1}, #monday
 {'date': datetime.datetime(2020, 4, 26, 0, 0), 'deliveries': 1}] #sunday
 ```

 If there is a weekend day within the dataset, it will be mantained. Otherwise, it will not appear. This version is limited to 15 days.

 ## Install

 pip install business-dataset-formatter

 ## How to use

```python
from bdf.bdf import BusinessDatasetFormatter
bd_obj = BusinessDatasetFormatter()
deliveries = [
                {'_id': datetime.datetime(2020, 4, 29, 0, 0), 'deliveries': 1}, #wednesday
                {'_id': datetime.datetime(2020, 4, 27, 0, 0), 'deliveries': 1}, #monday
                {'_id': datetime.datetime(2020, 4, 26, 0, 0), 'deliveries': 1}, #sunday
                {'_id': datetime.datetime(2020, 4, 24, 0, 0), 'deliveries': 2}, #friday
                {'_id': datetime.datetime(2020, 4, 21, 0, 0), 'deliveries': 3},
                {'_id': datetime.datetime(2020, 4, 19, 0, 0), 'deliveries': 3}, #sunday
                {'_id': datetime.datetime(2020, 4, 18, 0, 0), 'deliveries': 2}, #saturday
                {'_id': datetime.datetime(2020, 4, 17, 0, 0), 'deliveries': 1},
                {'_id': datetime.datetime(2020, 4, 16, 0, 0), 'deliveries': 1},
                {'_id': datetime.datetime(2020, 4, 15, 0, 0), 'deliveries': 2},
                {'_id': datetime.datetime(2020, 4, 14, 0, 0), 'deliveries': 1},
                {'_id': datetime.datetime(2020, 4, 13, 0, 0), 'deliveries': 1},
                {'_id': datetime.datetime(2020, 4, 11, 0, 0), 'deliveries': 1}, #saturday
                {'_id': datetime.datetime(2020, 4, 10, 0, 0), 'deliveries': 1},
                {'_id': datetime.datetime(2020, 4, 9, 0, 0), 'deliveries': 2},
                {'_id': datetime.datetime(2020, 4, 8, 0, 0), 'deliveries': 4},
                {'_id': datetime.datetime(2020, 4, 7, 0, 0), 'deliveries': 3},
                {'_id': datetime.datetime(2020, 4, 6, 0, 0), 'deliveries': 1},
                {'_id': datetime.datetime(2020, 4, 5, 0, 0), 'deliveries': 5}
            ]
current_date = datetime.date(year=2020, month=4, day=29)
id_field = '_id'
qty_field = 'deliveries'
adj_dataset = bd_obj.return_15_days_data(current_date, deliveries, id_field, qty_field)
```

The variable adj_dataset will contain the following result:
```python
[
    {'date': datetime.datetime(2020, 4, 29, 0, 0), 'deliveries': 1},
    {'date': datetime.datetime(2020, 4, 28, 0, 0), 'deliveries': 0},
    {'date': datetime.datetime(2020, 4, 27, 0, 0), 'deliveries': 1},
    {'date': datetime.datetime(2020, 4, 26, 0, 0), 'deliveries': 1},
    {'date': datetime.datetime(2020, 4, 24, 0, 0), 'deliveries': 2},
    {'date': datetime.datetime(2020, 4, 23, 0, 0), 'deliveries': 0},
    {'date': datetime.datetime(2020, 4, 22, 0, 0), 'deliveries': 0},
    {'date': datetime.datetime(2020, 4, 21, 0, 0), 'deliveries': 3},
    {'date': datetime.datetime(2020, 4, 20, 0, 0), 'deliveries': 0},
    {'date': datetime.datetime(2020, 4, 19, 0, 0), 'deliveries': 3},
    {'date': datetime.datetime(2020, 4, 18, 0, 0), 'deliveries': 2},
    {'date': datetime.datetime(2020, 4, 17, 0, 0), 'deliveries': 1},
    {'date': datetime.datetime(2020, 4, 16, 0, 0), 'deliveries': 1},
    {'date': datetime.datetime(2020, 4, 15, 0, 0), 'deliveries': 2},
    {'date': datetime.datetime(2020, 4, 14, 0, 0), 'deliveries': 1}
]
```