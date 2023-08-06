import datetime

from .exceptions import ENoDeliveryException

class BusinessDatasetFormatter:
    def return_15_days_data(self, current_date, db_deliveries, id_field, qty_field):
        deliveries = self._return_data_15_days(current_date, db_deliveries, id_field, qty_field)
        return deliveries

    def _return_data_15_days(self, current_date, db_deliveries, id_field, qty_field):
        number_of_days = 15
        saturday = 5
        size_deliveries = len(db_deliveries)
        self._validate_deliveries(size_deliveries)
        size_deliveries = number_of_days if size_deliveries >= number_of_days else size_deliveries
        current_date = datetime.datetime(year=current_date.year, month=current_date.month, day=current_date.day)
        deliveries = []
        counter = 0
        while counter < size_deliveries:
            found = self._find_for_delivery(current_date, db_deliveries, id_field)
            found_deliveries = len(found) > 0
            day_in_weekend = current_date.weekday() >= saturday
            weekend_no_deliveries = day_in_weekend and not(found_deliveries)
            if weekend_no_deliveries:
                current_date -= datetime.timedelta(days=1)
                continue
            delivery = dict()
            delivery['date'] = current_date
            if found_deliveries:
                delivery[qty_field] = found[0][qty_field]
            else:
                delivery[qty_field] = 0
            deliveries.append(delivery)
            current_date -= datetime.timedelta(days=1)
            counter += 1
        return deliveries

    def _find_for_delivery(self, current_date, db_deliveries, id_field):
        return list( filter( lambda x: x[id_field] == current_date, db_deliveries ) )

    def _validate_deliveries(self, size_deliveries):
        if size_deliveries == 0:
            raise ENoDeliveryException
