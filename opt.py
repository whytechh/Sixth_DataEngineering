import pandas as pd
import json
import os


file_path = 'Variant V.csv'
opt_file_path = 'VariantV_opt.csv'
new_file_path = 'VariantV_p2.csv'

def read_file(file_name):
    return pd.read_csv(file_name)


def file_size_on_disk(file_path):
    file_size = os.path.getsize(file_path)
    print(f"Размер файла на диске: {file_size / 1024 / 1024:.2f} MB")


def get_memory_stat_by_column(df):
    memory_usage_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()

    column_stat = list()
    for key in df.dtypes.keys():
        column_stat.append({
            "column_name": key,
            "memory_abs": int(memory_usage_stat[key] // 1024),
            "memory_per": round(float(memory_usage_stat[key]) / total_memory_usage * 100, 4),
            "dtype": str(df.dtypes[key])
        })

    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)
    for column in column_stat:
        print(
            f"{column['column_name']:30}: {column['memory_abs']:10} КБ: {column['memory_per']:10}% : {column['dtype']}")
    return column_stat


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:  
        usage_b = pandas_obj.memory_usage(deep=True)

    usage_mb = usage_b / 1024 ** 2 
    return "{:03.2f} MB".format(usage_mb)


def opt_obj(df):
     converted_obj = pd.DataFrame()
     dataset_obj = df.select_dtypes(include=['object']).copy()

     for col in dataset_obj.columns:
         num_unique_values = len(dataset_obj[col].unique())
         num_total_values = len(dataset_obj[col])
         if num_unique_values / num_total_values < 0.5:
             converted_obj.loc[:, col] = dataset_obj[col].astype('category')
         else:
             converted_obj.loc[:, col] = dataset_obj[col]

     #print(mem_usage(dataset_obj))
     #print(mem_usage(converted_obj))
     return converted_obj


def opt_int(df):
   dataset_int = df.select_dtypes(include=['int'])

   converted_int = dataset_int.apply(pd.to_numeric, downcast='unsigned')
   #print(mem_usage(dataset_int))
   #print(mem_usage(converted_int))
   
   compare_ints = pd.concat([dataset_int.dtypes, converted_int.dtypes], axis=1)
   compare_ints.columns = ['before', 'after']
   compare_ints.apply(pd.Series.value_counts)
   #print(compare_ints)
   
   return converted_int


def opt_float(df):

    dataset_float = df.select_dtypes(include=['float'])
    converted_float = dataset_float.apply(pd.to_numeric, downcast='float')

    #print(mem_usage(dataset_float))
    #print(mem_usage(converted_float))

    compare_floats = pd.concat([dataset_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ['before', 'after']
    compare_floats.apply(pd.Series.value_counts)
    #print(compare_floats)
    return converted_float


data = read_file(file_name=file_path)
file_size_on_disk(file_path=file_path)
print(f'Размер DataFrame в памяти {mem_usage(pandas_obj=data)}')
stat_no_opt = get_memory_stat_by_column(df=data)

with open('./results/stat_no_opt.json', 'w', encoding='utf-8') as file:
    json.dump(stat_no_opt, file, ensure_ascii=False, indent=1)

opt_data = data.copy()

converted_obj = opt_obj(data)
converted_int = opt_int(data)
converted_float = opt_float(data)

opt_data[converted_obj.columns] = converted_obj
opt_data[converted_int.columns] = converted_int
opt_data[converted_float.columns] = converted_float
opt_data.to_csv(opt_file_path, index=False, encoding='utf-8')

file_size_on_disk(file_path=opt_file_path)
print(f'Размер DataFrame в памяти {mem_usage(pandas_obj=opt_data)}')
stat_opt = get_memory_stat_by_column(df=opt_data)

with open('./results/stat_opt.json', 'w', encoding='utf-8') as file:
    json.dump(stat_opt, file, ensure_ascii=False, indent=1)

need_column = dict()
column_names = ['income', 
                'customer_age', 
                'payment_type',
                'name_email_similarity', 
                'date_of_birth_distinct_emails_4w',
                'employment_status', 
                'credit_risk_score', 
                'housing_status',
                'has_other_cards', 
                'session_length_in_minutes']

opt_dtypes = opt_data.dtypes
for key in data.columns:
    need_column[key] = opt_dtypes[key]
    print(f"{key}:{opt_dtypes[key]}")

with open('./results/new_file_types.json', 'w', encoding='utf-8') as file:
    dtype_json = need_column.copy()
    for key in dtype_json.keys():
        dtype_json[key] = str(dtype_json[key])
    json.dump(dtype_json, file)

read_and_optimized = pd.read_csv(file_path, usecols=lambda x: x in column_names, dtype=need_column)
read_and_optimized.to_csv(new_file_path, index=False, encoding='utf-8')
