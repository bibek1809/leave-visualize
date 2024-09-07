data ={
    "FileController":{
        "upload":{"first":['file_separator','category','column_mapping'],
                  "second":['link','file_separator','category','column_mapping','filename']},
        "column_mapping":['column_mappings','transformation'],
        "transform":['transformations'],
        "download_file_s3":['path']
    },
    "SchemaController":{
        "upload":['0']
    },
    "SpaceController":{
        "save_space":['is_deleted','s3_file_path','space_name','space_schema','vds_path','account_id','bi_data_source_id','status'],
        "update_space":['created_date','id','is_deleted','s3_file_path','space_name','space_schema','updated_date','vds_path','status'],
        "create_vds":['vds_name'],
        "add_file_to_space":['space_schema','file_id'],
        "get_all_spaces_by_account_id":['account_id','bi_data_source_id'],
        "get_all_gsheet_spaces":['offset','limit']

    },
    "MongoController":{
        "get_schema":['vds_path'],
        "mapping_operation":['report_key','report_date_field','vds_path','collection_name','display_name','bi_data_source_id','field_name_json','calculated_field','segment_field_format'],
        "view_mapping":['query','collection_name'],
        "delete_mapping":['query','collection_name'],
        "register_map":['bi_data_source_id','display_name','source_path'],
        "get_sources_tables":['source_path'],
        "update_mapping":['query','collection_name','update_fields']
    }
}   

data_types= {
    "file_separator": str,
    "category": str,
    "column_mapping": dict,
    "column_mappings":dict,
    "link": str,
    "filename": str,
    "transformation": list,
    "transformations":list,
    "is_deleted": int,
    "status": int,
    "s3_file_path": str,
    "space_name": str,
    "space_schema": list,
    "vds_path": str,
    "vds_name":str,
    "account_id": str,
    "bi_data_source_id":int,
    "created_date":str,
    "updated_date":str,
    "file_id":int,
    "space_id":int,
    "id":int,
    "path":str,
    "offset":int,
    "limit":int,
    "calculated_field":list,
    "collection_name":str,
    "field_name_json":dict,
    "query":str,
    "update_fields":dict,
    "display_name":str,
    "source_path":str,
    "segment_field_format":dict,
    "report_date_field":str,
    "report_key":str
}

allowed_null_value = ['column_mapping','vds_path','s3_file_path','column_mappings','transformation','transformations','query']

data_type_names = {
    "int": "integer",
    "float": "float",
    "str": "string",
    "dict":"Dictionary",
    "list":"list"
}