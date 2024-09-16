import threading
import time
from datetime import datetime, timedelta
import requests
from utils import Configuration
from services.RawService import RawService
from services.StatusService import StatusService
from services.UserService import UserService
from services.LeaveService import LeaveService
from services.LeaveTxnService import LeaveTxnService
from services.DesignationService import DesignationService
from database import DataSourceConfiguration
from entity.ObjectMapper import ObjectMapper
from entity.Raw import Raw
from entity.Status import Status
from entity.User import User
from entity.Leave import Leave
from entity.LeaveTransaction import LeaveTransaction
from entity.Designation import Designation
status_service = StatusService(DataSourceConfiguration.mysql_datasource)
aquisition_service = RawService(DataSourceConfiguration.mysql_datasource)
user_service = UserService(DataSourceConfiguration.mysql_datasource)
leave_service = LeaveService(DataSourceConfiguration.mysql_datasource)
leave_txn_service = LeaveTxnService(DataSourceConfiguration.mysql_datasource)
designation_service = DesignationService(DataSourceConfiguration.mysql_datasource)


class Acquisition:
    def __init__(self):
        pass
    
    @staticmethod
    def insert_status(status_type,start_date=None, end_date=None):
        status_json = {
            "status_type":status_type,
            "status":0,
            "start_date":start_date,
            "end_date":end_date
        }
        print(status_json)
        space = ObjectMapper().map_to(status_json, Status)
        return status_service.save(space)[0]['id']
    
    @staticmethod
    def update_status(id,status):
        if status_service.find_by_id(id)[0]['status'] != 2:
            status_json = {
                "id":id,
                "status":status
            }
            space = ObjectMapper().map_to(status_json, Status)
            status_service.update(space)
    
    @staticmethod
    def fetch_leave_data(start_date, end_date, page, size=10000):
        url = Configuration.LEAVE_API_URL
        params = {
            'fetchType': 'all',
            'startDate': start_date,
            'endDate': end_date,
            'size': size,
            'roleType': 'issuer',
            'page': page
        }
        headers = {
            'Authorization': Configuration.LEAVE_API_HEADER
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for bad responses
        return response.json()

    @staticmethod
    def create_date_ranges(start, end):
        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")
        date_ranges = []
        duration = (end - start).days

        if duration > 30:
            current_start = start
            while current_start < end:
                current_end = current_start + timedelta(days=30)  # Approx. month-long
                if current_end > end:
                    current_end = end
                date_ranges.append((current_start.strftime("%Y-%m-%d"), current_end.strftime("%Y-%m-%d")))
                current_start = current_end
        else:
            date_ranges.append((start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))

        return date_ranges
    
    @staticmethod
    def convert_to_camel_case(snake_str):
        # Split the string by underscores
        components = snake_str.split('_')
        
        # Capitalize the first letter of each component and join them
        camel_case_str = ''.join(x.capitalize() for x in components)
        
        return camel_case_str

    @staticmethod
    def camel_to_snake(name):
        import re
        s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return s1.lower()

    @staticmethod
    def process_leave_data(data,mapper,service):
        processed_data = [
            {Acquisition.camel_to_snake(key): value for key, value in item.items()}
            for item in data
        ]
        raw = ObjectMapper().map_to(processed_data,mapper)
        service.save_bulk(raw)

    # @staticmethod
    # def process_from_log(table_name,date):

    @staticmethod
    def fetch_and_process_data(start_date, end_date, page,status_id):
        try:
            response_data = Acquisition.fetch_leave_data(start_date, end_date, page)
            print(f"Processing data for {start_date} to {end_date}, page {page}")
            Acquisition.process_leave_data(response_data['data'], Raw,aquisition_service)

            total_count = response_data['meta']['total']
            size = response_data['meta']['size']
            total_pages = (total_count + size - 1) // size

            while page < total_pages:
                page += 1
                # Adding a delay between requests to prevent server overload
                time.sleep(2)  # 2 seconds pause between requests
                response_data = Acquisition.fetch_leave_data(start_date, end_date, page)
                print(f"Processing data for {start_date} to {end_date}, page {page}")
                Acquisition.process_leave_data(response_data['data'], Raw,aquisition_service)
            

        except Exception as e:
            Acquisition.update_status(status_id,2)
            print(f"Error in task: {e}")

    @staticmethod
    def fetch_all_leave_data(start_date, end_date):
        try:
            last_task = status_service.find_last_added()[0]["status_type"]
        except:
            last_task = "Designation"
        if last_task != "Designation":
            print('task cannot be initiated now')
        else:
            try:
                status_id = Acquisition.insert_status('Raw',start_date, end_date)
                date_ranges = Acquisition.create_date_ranges(start_date, end_date)

                threads = []

                # Launch a new thread for each date range
                for start, end in date_ranges:
                    t = threading.Thread(target=Acquisition.fetch_and_process_data, args=(start, end, 1,status_id))
                    threads.append(t)
                    t.start()

                    # Adding a delay between starting threads to prevent server overload
                    time.sleep(5)  # Pause 5 seconds before launching the next thread

                # Wait for all threads to finish
                for t in threads:
                    t.join()
                Acquisition.update_status(status_id,1)
            except Exception as e:
                print(f"Error in task: {e}")
                


    @staticmethod
    def fetch_and_process_etl(table_name,inserted_date,position,status_id):
        try:
            if table_name == 'user':
                data = aquisition_service.get_user_data(inserted_date,position)
                Acquisition.process_leave_data(data,User,user_service)
                status_service.update_previous_status('Raw',status_id)
            elif table_name == 'leave':
                data = aquisition_service.get_leave_data(inserted_date,position)
                Acquisition.process_leave_data(data,Leave,leave_service)
                status_service.update_previous_status('User',status_id)
            elif table_name == 'leave_txn':
                data = aquisition_service.get_transaction_data(inserted_date,position)
                Acquisition.process_leave_data(data,LeaveTransaction,leave_txn_service)
                status_service.update_previous_status('Leave',status_id)
            elif table_name == 'designation':
                data = aquisition_service.get_designation_data(inserted_date,position)
                Acquisition.process_leave_data(data,Designation,designation_service)
                status_service.update_previous_status('LeaveTxn',status_id)
                status_service.update_previous_status('Designation',status_id+1)
            else:
                pass
        except Exception as e:
            Acquisition.update_status(status_id,2)
            print(f"Error in task: {e}")

    @staticmethod
    def initiate_etl(table_name, inserted_date):
        threads = []
        total_count = aquisition_service.get_data_count(inserted_date,table_name)[0]["total_count"]
        status_id = Acquisition.insert_status(Acquisition.convert_to_camel_case(table_name),inserted_date)
        for i in range(0,total_count,10000):
            t = threading.Thread(target=Acquisition.fetch_and_process_etl, args=(table_name, inserted_date,i,status_id))
            threads.append(t)
            t.start()

            # Adding a delay between starting threads to prevent server overload
            time.sleep(5)  # Pause 5 seconds before launching the next thread

        # Wait for all threads to finish
        for t in threads:
            t.join()
        Acquisition.update_status(status_id,1)

