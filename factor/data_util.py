import pandas as pd

def fetch_data_from_jqloc(database,table_name,stock_list,fields = None):
    table = database[table_name]

    cursor = table.find(
        {
            'code': {
                '$in': list(stock_list)
            },
            "date_stamp":
                {
                    "$eq": QA_util_date_stamp(date),
                }   
        },
        {"_id": 0},
        batch_size=10000
    )
    res = pd.DataFrame([item for item in cursor])
    return res