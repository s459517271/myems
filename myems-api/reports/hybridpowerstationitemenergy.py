import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import falcon
import mysql.connector
import simplejson as json
from core import utilities
import config
from core.useractivity import access_control, api_key_control


class Reporting:
    def __init__(self):
        """Initializes Class"""
        pass

    @staticmethod
    def on_options(req, resp):
        resp.status = falcon.HTTP_200

    ####################################################################################################################
    # PROCEDURES
    # Step 1: valid parameters
    # Step 2: query the hybrid power station
    # Step 3: query charge energy data in 7 days
    # Step 4: query discharge energy data in 7 days
    # Step 5: query fuel consumption data in 7 days
    # Step 6: query charge energy data in this month
    # Step 7: query discharge energy data in this month
    # Step 9: query discharge energy data in this month
    # Step 9: query charge energy data in this year
    # Step 10: query discharge energy data in this year
    # Step 11: query discharge energy data in this year
    # Step 12: construct the report
    ####################################################################################################################
    @staticmethod
    def on_get(req, resp):
        if 'API-KEY' not in req.headers or \
                not isinstance(req.headers['API-KEY'], str) or \
                len(str.strip(req.headers['API-KEY'])) == 0:
            access_control(req)
        else:
            api_key_control(req)
        # this procedure accepts hybrid power station id or uuid
        hybrid_power_station_id = req.params.get('id')
        hybrid_power_station_uuid = req.params.get('uuid')

        ################################################################################################################
        # Step 1: valid parameters
        ################################################################################################################
        if hybrid_power_station_id is None and hybrid_power_station_uuid is None:
            raise falcon.HTTPError(status=falcon.HTTP_400, title='API.BAD_REQUEST',
                                   description='API.INVALID_HYBRID_POWER_STATION_ID')

        if hybrid_power_station_id is not None:
            hybrid_power_station_id = str.strip(hybrid_power_station_id)
            if not hybrid_power_station_id.isdigit() or int(hybrid_power_station_id) <= 0:
                raise falcon.HTTPError(status=falcon.HTTP_400, title='API.BAD_REQUEST',
                                       description='API.INVALID_HYBRID_POWER_STATION_ID')

        if hybrid_power_station_uuid is not None:
            regex = re.compile(r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
            match = regex.match(str.strip(hybrid_power_station_uuid))
            if not bool(match):
                raise falcon.HTTPError(status=falcon.HTTP_400, title='API.BAD_REQUEST',
                                       description='API.INVALID_HYBRID_POWER_STATION_UUID')

        ################################################################################################################
        # Step 2: query the hybrid power station
        ################################################################################################################
        cnx_system_db = mysql.connector.connect(**config.myems_system_db)
        cursor_system_db = cnx_system_db.cursor()
        # Get Spaces associated with hybrid power stations
        query = (" SELECT se.hybrid_power_station_id, s.name "
                 " FROM tbl_spaces s, tbl_spaces_hybrid_power_stations se "
                 " WHERE se.space_id = s.id ")
        cursor_system_db.execute(query)
        rows_spaces = cursor_system_db.fetchall()

        space_dict = dict()
        if rows_spaces is not None and len(rows_spaces) > 0:
            for row in rows_spaces:
                space_dict[row[0]] = row[1]
        print(space_dict)
        # Get hybrid power station
        if hybrid_power_station_id is not None:
            query = (" SELECT id, name, uuid, "
                     "        address, latitude, longitude, rated_capacity, rated_power, "
                     "        contact_id, cost_center_id "
                     " FROM tbl_hybrid_power_stations "
                     " WHERE id = %s ")
            cursor_system_db.execute(query, (hybrid_power_station_id,))
            row = cursor_system_db.fetchone()
        elif hybrid_power_station_uuid is not None:
            query = (" SELECT id, name, uuid, "
                     "        address, latitude, longitude, rated_capacity, rated_power, "
                     "        contact_id, cost_center_id "
                     " FROM tbl_hybrid_power_stations "
                     " WHERE uuid = %s ")
            cursor_system_db.execute(query, (hybrid_power_station_uuid,))
            row = cursor_system_db.fetchone()

        if row is None:
            cursor_system_db.close()
            cnx_system_db.close()
            raise falcon.HTTPError(status=falcon.HTTP_404, title='API.NOT_FOUND',
                                   description='API.HYBRID_POWER_STATION_NOT_FOUND')
        else:
            hybrid_power_station_id = row[0]
            hybrid_power_station = {
                "id": row[0],
                "name": row[1],
                "uuid": row[2],
                "address": row[3],
                "space_name": space_dict.get(row[0]),
                "latitude": row[4],
                "longitude": row[5],
                "rated_capacity": row[6],
                "rated_power": row[7]
            }

        ################################################################################################################
        # Step 3: query charge energy data in 7 days
        ################################################################################################################
        timezone_offset = int(config.utc_offset[1:3]) * 60 + int(config.utc_offset[4:6])
        if config.utc_offset[0] == '-':
            timezone_offset = -timezone_offset
        reporting = dict()
        reporting['charge_7_days'] = dict()
        reporting['charge_this_month'] = dict()
        reporting['charge_this_year'] = dict()
        reporting['discharge_7_days'] = dict()
        reporting['discharge_this_month'] = dict()
        reporting['discharge_this_year'] = dict()
        reporting['fuel_consumption_7_days'] = dict()
        reporting['fuel_consumption_this_month'] = dict()
        reporting['fuel_consumption_this_year'] = dict()

        end_datetime_utc = datetime.utcnow()
        end_datetime_local = datetime.utcnow() + timedelta(minutes=timezone_offset)
        period_type = 'daily'
        start_datetime_local = end_datetime_local.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=6)
        start_datetime_utc = start_datetime_local - timedelta(minutes=timezone_offset)
        print('start_datetime_local:' + start_datetime_local.isoformat())
        print('end_datetime_local:' + end_datetime_local.isoformat())
        print('start_datetime_utc:' + start_datetime_utc.isoformat())
        print('end_datetime_utc:' + end_datetime_utc.isoformat())

        cnx_energy_db = mysql.connector.connect(**config.myems_energy_db)
        cursor_energy_db = cnx_energy_db.cursor()

        reporting['charge_7_days'] = dict()
        reporting['charge_7_days']['timestamps_array'] = list()
        reporting['charge_7_days']['values_array'] = list()

        timestamps = list()
        values = list()
        query = (" SELECT start_datetime_utc, actual_value "
                 " FROM tbl_hybrid_power_station_charge_hourly "
                 " WHERE hybrid_power_station_id = %s "
                 " AND start_datetime_utc >= %s "
                 " AND start_datetime_utc < %s "
                 " ORDER BY start_datetime_utc ")
        cursor_energy_db.execute(query, (hybrid_power_station_id, start_datetime_utc, end_datetime_utc))
        rows_charge_hourly = cursor_energy_db.fetchall()

        rows_charge_periodically = utilities.aggregate_hourly_data_by_period(rows_charge_hourly,
                                                                             start_datetime_utc,
                                                                             end_datetime_utc,
                                                                             period_type)
        for row_charge_periodically in rows_charge_periodically:
            current_datetime_local = row_charge_periodically[0].replace(tzinfo=timezone.utc) + \
                                     timedelta(minutes=timezone_offset)
            if period_type == 'hourly':
                current_datetime = current_datetime_local.isoformat()[0:19]
            elif period_type == 'daily':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'weekly':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'monthly':
                current_datetime = current_datetime_local.isoformat()[0:7]
            elif period_type == 'yearly':
                current_datetime = current_datetime_local.isoformat()[0:4]

            actual_value = Decimal(0.0) if row_charge_periodically[1] is None else row_charge_periodically[1]
            timestamps.append(current_datetime)
            values.append(actual_value)
        reporting['charge_7_days']['timestamps_array'].append(timestamps)
        reporting['charge_7_days']['values_array'].append(values)
        ################################################################################################################
        # Step 4: query discharge energy data in 7 days
        ################################################################################################################
        reporting['discharge_7_days'] = dict()
        reporting['discharge_7_days']['timestamps_array'] = list()
        reporting['discharge_7_days']['values_array'] = list()
        timestamps = list()
        values = list()
        query = (" SELECT start_datetime_utc, actual_value "
                 " FROM tbl_hybrid_power_station_discharge_hourly "
                 " WHERE hybrid_power_station_id = %s "
                 " AND start_datetime_utc >= %s "
                 " AND start_datetime_utc < %s "
                 " ORDER BY start_datetime_utc ")
        cursor_energy_db.execute(query, (hybrid_power_station_id, start_datetime_utc, end_datetime_utc))
        rows_charge_hourly = cursor_energy_db.fetchall()

        rows_charge_periodically = utilities.aggregate_hourly_data_by_period(rows_charge_hourly,
                                                                             start_datetime_utc,
                                                                             end_datetime_utc,
                                                                             period_type)

        for row_charge_periodically in rows_charge_periodically:
            current_datetime_local = row_charge_periodically[0].replace(tzinfo=timezone.utc) + \
                                     timedelta(minutes=timezone_offset)
            if period_type == 'hourly':
                current_datetime = current_datetime_local.isoformat()[0:19]
            elif period_type == 'daily':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'weekly':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'monthly':
                current_datetime = current_datetime_local.isoformat()[0:7]
            elif period_type == 'yearly':
                current_datetime = current_datetime_local.isoformat()[0:4]

            actual_value = Decimal(0.0) if row_charge_periodically[1] is None else row_charge_periodically[1]
            timestamps.append(current_datetime)
            values.append(actual_value)
        reporting['discharge_7_days']['timestamps_array'].append(timestamps)
        reporting['discharge_7_days']['values_array'].append(values)

        ################################################################################################################
        # Step 5: query fuel consumption data in 7 days
        ################################################################################################################
        reporting['fuel_consumption_7_days'] = dict()
        reporting['fuel_consumption_7_days']['timestamps_array'] = list()
        reporting['fuel_consumption_7_days']['values_array'] = list()
        timestamps = list()
        values = list()
        query = (" SELECT start_datetime_utc, actual_value "
                 " FROM tbl_hybrid_power_station_fuel_hourly "
                 " WHERE hybrid_power_station_id = %s "
                 " AND start_datetime_utc >= %s "
                 " AND start_datetime_utc < %s "
                 " ORDER BY start_datetime_utc ")
        cursor_energy_db.execute(query, (hybrid_power_station_id, start_datetime_utc, end_datetime_utc))
        rows_fuel_consumption_hourly = cursor_energy_db.fetchall()

        rows_fuel_consumption_periodically = utilities.aggregate_hourly_data_by_period(rows_fuel_consumption_hourly,
                                                                                       start_datetime_utc,
                                                                                       end_datetime_utc,
                                                                                       period_type)

        for row_fuel_consumption_periodically in rows_fuel_consumption_periodically:
            current_datetime_local = row_fuel_consumption_periodically[0].replace(tzinfo=timezone.utc) + \
                                     timedelta(minutes=timezone_offset)
            if period_type == 'hourly':
                current_datetime = current_datetime_local.isoformat()[0:19]
            elif period_type == 'daily':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'weekly':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'monthly':
                current_datetime = current_datetime_local.isoformat()[0:7]
            elif period_type == 'yearly':
                current_datetime = current_datetime_local.isoformat()[0:4]

            actual_value = Decimal(0.0) if row_fuel_consumption_periodically[1] is None else \
                row_fuel_consumption_periodically[1]
            timestamps.append(current_datetime)
            values.append(actual_value)
        reporting['fuel_consumption_7_days']['timestamps_array'].append(timestamps)
        reporting['fuel_consumption_7_days']['values_array'].append(values)

        ################################################################################################################
        # Step 6: query charge energy data in this month
        ################################################################################################################
        end_datetime_utc = datetime.utcnow()
        end_datetime_local = datetime.utcnow() + timedelta(minutes=timezone_offset)
        period_type = 'daily'
        start_datetime_local = end_datetime_local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_datetime_utc = start_datetime_local - timedelta(minutes=timezone_offset)
        print('start_datetime_local:' + start_datetime_local.isoformat())
        print('end_datetime_local:' + end_datetime_local.isoformat())
        print('start_datetime_utc:' + start_datetime_utc.isoformat())
        print('end_datetime_utc:' + end_datetime_utc.isoformat())

        reporting['charge_this_month'] = dict()
        reporting['charge_this_month']['timestamps_array'] = list()
        reporting['charge_this_month']['values_array'] = list()

        timestamps = list()
        values = list()
        query = (" SELECT start_datetime_utc, actual_value "
                 " FROM tbl_hybrid_power_station_charge_hourly "
                 " WHERE hybrid_power_station_id = %s "
                 " AND start_datetime_utc >= %s "
                 " AND start_datetime_utc < %s "
                 " ORDER BY start_datetime_utc ")
        cursor_energy_db.execute(query, (hybrid_power_station['id'], start_datetime_utc, end_datetime_utc))
        rows_charge_hourly = cursor_energy_db.fetchall()

        rows_charge_periodically = utilities.aggregate_hourly_data_by_period(rows_charge_hourly,
                                                                             start_datetime_utc,
                                                                             end_datetime_utc,
                                                                             period_type)

        for row_charge_periodically in rows_charge_periodically:
            current_datetime_local = row_charge_periodically[0].replace(tzinfo=timezone.utc) + \
                                     timedelta(minutes=timezone_offset)
            if period_type == 'hourly':
                current_datetime = current_datetime_local.isoformat()[0:19]
            elif period_type == 'daily':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'weekly':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'monthly':
                current_datetime = current_datetime_local.isoformat()[0:7]
            elif period_type == 'yearly':
                current_datetime = current_datetime_local.isoformat()[0:4]

            actual_value = Decimal(0.0) if row_charge_periodically[1] is None else row_charge_periodically[1]
            timestamps.append(current_datetime)
            values.append(actual_value)
        reporting['charge_this_month']['timestamps_array'].append(timestamps)
        reporting['charge_this_month']['values_array'].append(values)

        ################################################################################################################
        # Step 7: query discharge energy data in this month
        ################################################################################################################
        reporting['discharge_this_month'] = dict()
        reporting['discharge_this_month']['timestamps_array'] = list()
        reporting['discharge_this_month']['values_array'] = list()

        timestamps = list()
        values = list()
        query = (" SELECT start_datetime_utc, actual_value "
                 " FROM tbl_hybrid_power_station_discharge_hourly "
                 " WHERE hybrid_power_station_id = %s "
                 " AND start_datetime_utc >= %s "
                 " AND start_datetime_utc < %s "
                 " ORDER BY start_datetime_utc ")
        cursor_energy_db.execute(query, (hybrid_power_station['id'], start_datetime_utc, end_datetime_utc))
        rows_discharge_hourly = cursor_energy_db.fetchall()

        rows_discharge_periodically = utilities.aggregate_hourly_data_by_period(rows_discharge_hourly,
                                                                                start_datetime_utc,
                                                                                end_datetime_utc,
                                                                                period_type)

        for row_discharge_periodically in rows_discharge_periodically:
            current_datetime_local = row_discharge_periodically[0].replace(tzinfo=timezone.utc) + \
                                     timedelta(minutes=timezone_offset)
            if period_type == 'hourly':
                current_datetime = current_datetime_local.isoformat()[0:19]
            elif period_type == 'daily':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'weekly':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'monthly':
                current_datetime = current_datetime_local.isoformat()[0:7]
            elif period_type == 'yearly':
                current_datetime = current_datetime_local.isoformat()[0:4]

            actual_value = Decimal(0.0) if row_discharge_periodically[1] is None else row_discharge_periodically[1]
            timestamps.append(current_datetime)
            values.append(actual_value)
        reporting['discharge_this_month']['timestamps_array'].append(timestamps)
        reporting['discharge_this_month']['values_array'].append(values)

        ################################################################################################################
        # Step 8: query fuel consumption data in this month
        ################################################################################################################
        reporting['fuel_consumption_this_month'] = dict()
        reporting['fuel_consumption_this_month']['timestamps_array'] = list()
        reporting['fuel_consumption_this_month']['values_array'] = list()

        timestamps = list()
        values = list()
        query = (" SELECT start_datetime_utc, actual_value "
                 " FROM tbl_hybrid_power_station_fuel_hourly "
                 " WHERE hybrid_power_station_id = %s "
                 " AND start_datetime_utc >= %s "
                 " AND start_datetime_utc < %s "
                 " ORDER BY start_datetime_utc ")
        cursor_energy_db.execute(query, (hybrid_power_station['id'], start_datetime_utc, end_datetime_utc))
        rows_fuel_consumption_hourly = cursor_energy_db.fetchall()

        rows_fuel_consumption_periodically = utilities.aggregate_hourly_data_by_period(rows_fuel_consumption_hourly,
                                                                                       start_datetime_utc,
                                                                                       end_datetime_utc,
                                                                                       period_type)

        for row_fuel_consumption_periodically in rows_fuel_consumption_periodically:
            current_datetime_local = row_fuel_consumption_periodically[0].replace(tzinfo=timezone.utc) + \
                                     timedelta(minutes=timezone_offset)
            if period_type == 'hourly':
                current_datetime = current_datetime_local.isoformat()[0:19]
            elif period_type == 'daily':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'weekly':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'monthly':
                current_datetime = current_datetime_local.isoformat()[0:7]
            elif period_type == 'yearly':
                current_datetime = current_datetime_local.isoformat()[0:4]

            actual_value = Decimal(0.0) if row_fuel_consumption_periodically[1] is None else \
                row_fuel_consumption_periodically[1]
            timestamps.append(current_datetime)
            values.append(actual_value)
        reporting['fuel_consumption_this_month']['timestamps_array'].append(timestamps)
        reporting['fuel_consumption_this_month']['values_array'].append(values)

        ################################################################################################################
        # Step 9: query charge energy data in this year
        ################################################################################################################
        end_datetime_utc = datetime.utcnow()
        end_datetime_local = datetime.utcnow() + timedelta(minutes=timezone_offset)
        period_type = 'monthly'
        start_datetime_local = end_datetime_local.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        start_datetime_utc = start_datetime_local - timedelta(minutes=timezone_offset)
        print('start_datetime_local:' + start_datetime_local.isoformat())
        print('end_datetime_local:' + end_datetime_local.isoformat())
        print('start_datetime_utc:' + start_datetime_utc.isoformat())
        print('end_datetime_utc:' + end_datetime_utc.isoformat())

        reporting['charge_this_year'] = dict()
        reporting['charge_this_year']['timestamps_array'] = list()
        reporting['charge_this_year']['values_array'] = list()

        timestamps = list()
        values = list()
        query = (" SELECT start_datetime_utc, actual_value "
                 " FROM tbl_hybrid_power_station_charge_hourly "
                 " WHERE hybrid_power_station_id = %s "
                 " AND start_datetime_utc >= %s "
                 " AND start_datetime_utc < %s "
                 " ORDER BY start_datetime_utc ")
        cursor_energy_db.execute(query, (hybrid_power_station['id'], start_datetime_utc, end_datetime_utc))
        rows_charge_hourly = cursor_energy_db.fetchall()

        rows_charge_periodically = utilities.aggregate_hourly_data_by_period(rows_charge_hourly,
                                                                             start_datetime_utc,
                                                                             end_datetime_utc,
                                                                             period_type)
        for row_charge_periodically in rows_charge_periodically:
            current_datetime_local = row_charge_periodically[0].replace(tzinfo=timezone.utc) + \
                                     timedelta(minutes=timezone_offset)
            if period_type == 'hourly':
                current_datetime = current_datetime_local.isoformat()[0:19]
            elif period_type == 'daily':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'weekly':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'monthly':
                current_datetime = current_datetime_local.isoformat()[0:7]
            elif period_type == 'yearly':
                current_datetime = current_datetime_local.isoformat()[0:4]

            actual_value = Decimal(0.0) if row_charge_periodically[1] is None else row_charge_periodically[1]
            timestamps.append(current_datetime)
            values.append(actual_value)
        reporting['charge_this_year']['timestamps_array'].append(timestamps)
        reporting['charge_this_year']['values_array'].append(values)

        ################################################################################################################
        # Step 10: query discharge energy data in this year
        ################################################################################################################
        reporting['discharge_this_year'] = dict()
        reporting['discharge_this_year']['timestamps_array'] = list()
        reporting['discharge_this_year']['values_array'] = list()

        timestamps = list()
        values = list()
        query = (" SELECT start_datetime_utc, actual_value "
                 " FROM tbl_hybrid_power_station_discharge_hourly "
                 " WHERE hybrid_power_station_id = %s "
                 " AND start_datetime_utc >= %s "
                 " AND start_datetime_utc < %s "
                 " ORDER BY start_datetime_utc ")
        cursor_energy_db.execute(query, (hybrid_power_station['id'], start_datetime_utc, end_datetime_utc))
        rows_discharge_hourly = cursor_energy_db.fetchall()

        rows_discharge_periodically = utilities.aggregate_hourly_data_by_period(rows_discharge_hourly,
                                                                                start_datetime_utc,
                                                                                end_datetime_utc,
                                                                                period_type)
        for row_discharge_periodically in rows_discharge_periodically:
            current_datetime_local = row_discharge_periodically[0].replace(tzinfo=timezone.utc) + \
                                     timedelta(minutes=timezone_offset)
            if period_type == 'hourly':
                current_datetime = current_datetime_local.isoformat()[0:19]
            elif period_type == 'daily':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'weekly':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'monthly':
                current_datetime = current_datetime_local.isoformat()[0:7]
            elif period_type == 'yearly':
                current_datetime = current_datetime_local.isoformat()[0:4]

            actual_value = Decimal(0.0) if row_discharge_periodically[1] is None else row_discharge_periodically[1]
            timestamps.append(current_datetime)
            values.append(actual_value)
        reporting['discharge_this_year']['timestamps_array'].append(timestamps)
        reporting['discharge_this_year']['values_array'].append(values)

        ################################################################################################################
        # Step 12: query fuel consumption energy data in this year
        ################################################################################################################
        reporting['fuel_consumption_this_year'] = dict()
        reporting['fuel_consumption_this_year']['timestamps_array'] = list()
        reporting['fuel_consumption_this_year']['values_array'] = list()

        timestamps = list()
        values = list()
        query = (" SELECT start_datetime_utc, actual_value "
                 " FROM tbl_hybrid_power_station_fuel_hourly "
                 " WHERE hybrid_power_station_id = %s "
                 " AND start_datetime_utc >= %s "
                 " AND start_datetime_utc < %s "
                 " ORDER BY start_datetime_utc ")
        cursor_energy_db.execute(query, (hybrid_power_station['id'], start_datetime_utc, end_datetime_utc))
        rows_fuel_consumption_hourly = cursor_energy_db.fetchall()

        rows_fuel_consumption_periodically = utilities.aggregate_hourly_data_by_period(rows_fuel_consumption_hourly,
                                                                                       start_datetime_utc,
                                                                                       end_datetime_utc,
                                                                                       period_type)
        for row_fuel_consumption_periodically in rows_fuel_consumption_periodically:
            current_datetime_local = row_fuel_consumption_periodically[0].replace(tzinfo=timezone.utc) + \
                                     timedelta(minutes=timezone_offset)
            if period_type == 'hourly':
                current_datetime = current_datetime_local.isoformat()[0:19]
            elif period_type == 'daily':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'weekly':
                current_datetime = current_datetime_local.isoformat()[0:10]
            elif period_type == 'monthly':
                current_datetime = current_datetime_local.isoformat()[0:7]
            elif period_type == 'yearly':
                current_datetime = current_datetime_local.isoformat()[0:4]

            actual_value = Decimal(0.0) if row_fuel_consumption_periodically[1] is None else \
                row_fuel_consumption_periodically[1]
            timestamps.append(current_datetime)
            values.append(actual_value)
        reporting['fuel_consumption_this_year']['timestamps_array'].append(timestamps)
        reporting['fuel_consumption_this_year']['values_array'].append(values)

        ################################################################################################################
        # Step 12: construct the report
        ################################################################################################################
        if cursor_system_db:
            cursor_system_db.close()
        if cnx_system_db:
            cnx_system_db.close()

        if cursor_energy_db:
            cursor_energy_db.close()
        if cnx_energy_db:
            cnx_energy_db.close()

        result = dict()
        result['hybrid_power_station'] = hybrid_power_station
        result['reporting'] = reporting
        resp.text = json.dumps(result)
