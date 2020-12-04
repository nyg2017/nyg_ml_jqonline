from data_interface import jq_data
from data_interface.jq_data_mongodb import JqMdb

data_api_dict = {
    "jq":jq_data,
    "jq_mdb":JqMdb
}

UserDataApi = data_api_dict['jq_mdb']