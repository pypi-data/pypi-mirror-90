import copy
import datetime
import hashlib
import os
import shutil
import time

import googleads
import pandas as pd
import yaml
from dbstream import DBStream

# Timeout between retries in seconds.
from pyrror.Error import Error

BACKOFF_FACTOR = 5

# Maximum number of retries for 500 errors.
MAX_RETRIES = 5

# Maximum number of items to be sent in a single API response.
PAGE_SIZE = 100


def set_report_definition(report_type, start, end, fields):
    return {
        'reportName': "%s between %s and %s" % (report_type, start, end),
        'dateRangeType': "CUSTOM_DATE",
        'reportType': report_type,
        'downloadFormat': 'CSV',
        'selector': {
            'fields': fields,
            'dateRange': {
                "min": start,
                "max": end
            },
        }
    }


def treat_columns(columns_name):
    for i in range(len(columns_name)):
        columns_name[i] = columns_name[i].lower() \
            .replace(" ", "_") \
            .replace(".", "_") \
            .replace("-", "_")
    return columns_name


def set_batch_id(customer_id, month):
    a = str(customer_id) + str(month)
    id_batch = hashlib.sha224(a.encode()).hexdigest()
    return id_batch


class GoogleAds:
    def __init__(self,
                 dbstream: DBStream,
                 developer_token,
                 client_customer_id,
                 path_to_private_key_file,
                 delegated_account,
                 data_directory_path,
                 reports_config_path,
                 schema_name="adwords"):
        self.dbstream = dbstream
        self.developer_token = developer_token
        self.client_customer_id = client_customer_id
        self.path_to_private_key_file = path_to_private_key_file
        self.delegated_account = delegated_account
        self.data_directory_path = data_directory_path if (data_directory_path[-1] == "/") else (
                data_directory_path + "/")
        self.reports_config = yaml.load(open(reports_config_path), Loader=yaml.FullLoader)
        self.schema_name = schema_name
        self.error = Error(
            client_id=self.dbstream.client_id,
            monitoring_error_url="http://dev-datacockpit.herokuapp.com/api/monitoring/error_to_slack"
        )

    def get_client(self):
        return googleads.adwords.AdWordsClient.LoadFromString(
            yaml.dump(
                {
                    "adwords": {
                        "developer_token": self.developer_token,
                        "client_customer_id": self.client_customer_id,
                        "path_to_private_key_file": self.path_to_private_key_file,
                        "delegated_account": self.delegated_account
                    }
                }
            ))

    def get_customer_ids(self):
        client = self.get_client()
        managed_customer_service = client.GetService(
            service_name='ManagedCustomerService',
            version='v201809')
        offset = 0
        # Get the account hierarchy for this account.
        selector = {
            "fields": ["CustomerId", "Name"],
            "predicates": [{
                "field": "CanManageClients",
                "operator": "EQUALS",
                "values": [False]
            }],
            "paging": {
                "startIndex": str(offset),
                "numberResults": str(PAGE_SIZE)
            }
        }

        more_pages = True
        result = []

        while more_pages:
            page = managed_customer_service.get(selector)

            if page and 'entries' in page and page['entries']:
                for entry in page['entries']:
                    result.append(entry['customerId'])
                    print(entry["name"])
            else:
                raise Exception('Can\'t retrieve any customer ID.')
            offset += PAGE_SIZE
            selector['paging']['startIndex'] = str(offset)
            more_pages = offset < int(page['totalNumEntries'])

        return result

    def download_report(self, report_definition, customer_id, folder_path):
        client = self.get_client()
        report_downloader = client.GetReportDownloader()
        file_path = folder_path + str(customer_id) + ".csv"

        retry_count = 0

        while True:
            print('Loading report for customer ID "%s" into "%s"...'
                  % (customer_id, file_path))
            try:
                with open(file_path, 'wb') as handler:
                    report_downloader.DownloadReport(
                        report_definition,
                        output=handler,
                        client_customer_id=customer_id)
                return True, {'customerId': customer_id}
            except googleads.errors.AdWordsReportError as e:
                if e.code == 500 and retry_count < MAX_RETRIES:
                    time.sleep(retry_count * BACKOFF_FACTOR)
                else:
                    if "CUSTOMER_NOT_ACTIVE" in str(e):
                        print("CUSTOMER_NOT_ACTIVE")
                    else:
                        self.error.log("adwords_loading_code_%s_retry_count_%s_customer_%s"
                                   % (e.code, retry_count + 1, customer_id)
                                   )
                    return False, {"customerId": customer_id, "code": e.code, "message": str(e)}

    def treat_reports(self, folder_path, table_name, time_increment, time_increment_field_mapping):
        row_data = []
        rows = []
        for f in os.listdir(folder_path):
            customer_id = f.split(".")[0]
            print(folder_path + f)
            len_file = len(open(folder_path + f).readlines())
            if len_file == 0:
                continue
            list_dict = pd.read_csv(open(folder_path + f), skiprows=1).to_dict(orient="records")[:-1]
            for l in list_dict:
                l["batch_id"] = set_batch_id(customer_id, l[
                    time_increment_field_mapping if time_increment_field_mapping else time_increment])
                row_data.append(l)

        columns_name = list(row_data[0].keys())
        for r in row_data:
            row = []
            for c in columns_name:
                if " --" in str(r[c]):
                    row.append(None)
                else:
                    row.append(str(r[c]))
            rows.append(row)
        data = {
            "table_name": "%s.%s_temp" % (self.schema_name, table_name),
            "columns_name": treat_columns(columns_name),
            "rows": rows
        }
        self.dbstream.send_data(
            data,
            other_table_to_update="%s.%s" % (self.schema_name, table_name)
        )
        self.dbstream.clean("batch_id", schema_prefix=self.schema_name, table=table_name)

    def manage_reports(self, report_key, customer_id=None, start=None, end=None, time_increment=None):
        report_config = self.reports_config["reports"][report_key]
        if time_increment:
            time_increment_dict = {time_increment: report_config["time_increments"][time_increment]}
        else:
            time_increment_dict = report_config["time_increments"]

        if customer_id:
            customer_ids = [customer_id]
        else:
            customer_ids = self.get_customer_ids()
        shutil.rmtree(self.data_directory_path, ignore_errors=True)
        for time_increment in time_increment_dict.keys():
            table_name = report_key + "_" + time_increment.lower()

            fields = copy.deepcopy(report_config.get("fields"))
            fields.append(time_increment)

            folder_path = self.data_directory_path + table_name + "/"
            time_increment_field_mapping = time_increment_dict[time_increment].get("field_mapping")
            for customer_id in customer_ids:
                if start is None:
                    start = self.dbstream.get_max(
                        schema=self.schema_name,
                        table=table_name,
                        field=time_increment_field_mapping if time_increment_field_mapping else time_increment,
                        filter_clause="where customer_id='%s'" % customer_id
                    )
                    if isinstance(start, datetime.datetime):
                        start = start.strftime("%Y%m%d")
                if start is None:
                    start = time_increment_dict[time_increment]["since"]

                if end is None:
                    end = datetime.date.today().strftime("%Y%m%d")
                report_definition = set_report_definition(
                    report_type=report_config.get("report_type"),
                    fields=fields,
                    start=start,
                    end=end
                )

                os.makedirs(folder_path, exist_ok=True)
                self.download_report(
                    report_definition=report_definition,
                    customer_id=customer_id,
                    folder_path=folder_path
                )

            self.treat_reports(folder_path=folder_path,
                               table_name=table_name,
                               time_increment=time_increment,
                               time_increment_field_mapping=time_increment_dict[time_increment].get("field_mapping")
                               )
        shutil.rmtree(self.data_directory_path, ignore_errors=True)
