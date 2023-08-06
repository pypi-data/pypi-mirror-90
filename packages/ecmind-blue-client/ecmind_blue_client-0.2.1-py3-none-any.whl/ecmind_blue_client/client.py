from abc import ABC, abstractmethod
from typing import Optional, Any, List, Dict, Union
from XmlElement import XmlElement as X
from .job import Job
from .result import Result
from .result_file import ResultFile
from .const import SystemFields, ImportActions

class Client(ABC):

    @abstractmethod
    def execute(self, job:Job) -> Result:
        """Send a job to the blue server, execute it and return the response.

        Keyword arguments:
        job -- A previously created Job() object.
        """
        raise NotImplemented
    
    def get_object_type_by_id(self, object_id:int) -> int:
        """Helper function: Execute the dms.GetObjectTypeByID job for a given object id and return the objects type id.

        Keyword arguments:
        object_id -- A folder, register or document id.
        """
        job = Job('dms.GetObjectTypeByID', Flags=0, ObjectID=object_id)
        return self.execute(job).values['ObjectType']

    def store_in_cache(self, object_id:int, object_type_id:Optional[int]=None, checkout:Optional[bool]=False) -> List[ResultFile]:
        """Helper function: Execute the std.StoreInCache job for a given object to retrieve its files.

        Keyword arguments:
        object_id -- A document id.
        object_type_id -- (Optional) The documents type id. When not provided, it is retrieve via get_object_type_by_id() first.
        checkout -- (Optional) When True, change the documents state to checked out on the server.
        """
        if object_type_id == None:
            object_type_id = self.get_object_type_by_id(object_id)

        job = Job('std.StoreInCache',
            Flags=1,
            dwObjectID=object_id,
            dwObjectType=object_type_id,
            DocState=(0 if checkout else 1),
            FileCount=0
        )
        result = self.execute(job)
        if result.return_code != 0:
            raise(RuntimeError(f'Received return code {result.return_code}: {result.error_message}'))

        return result.files

    def xml_import(self,
                  object_name:str,
                  search_fields:Dict[str, str],
                  import_fields:Dict[str, str],
                  table_fields:Dict[str, List[Dict[str, Any]]]=None,
                  folder_id:Optional[int]=None,
                  register_id:Optional[int]=None,
                  object_id:Optional[int]=None,
                  options:str='',
                  action0:ImportActions=ImportActions.INSERT,
                  action1:ImportActions=ImportActions.UPDATE,
                  actionM:ImportActions=ImportActions.ERROR,
                  files:List[str]=[]
        ):
        """Helper function: Execute the dms.XMLImport job.

        Keyword arguments:
        object_name -- The internal name of the object type to import.
        search_fields -- Dict of internal field names and values. If one or more objects match all search_fields, the action1 or actionM will be used, action0 otherwise. 
        import_fields -- Dict of internal field names and (new) values.
        table_fields -- Dict of internal table field names and list of new rows as dicts of internal column name and values.
        folder_id -- (Optional) Folder id to import registers or documents into.
        register_id -- (Optional) Register id to import sub-registers or documents into.
        object_id -- (Optional) Objekt id to force an update of this element. 
        options -- (Optional) Semicolon separated string of import options.
        action0 -- (Optional) ImportActions Enum element defining how to handle imports when the search_fields do not match any pre-existing objects.
        action1 -- (Optional) ImportActions Enum element defining how to handle imports when the search_fields do match exactly one pre-existing object.
        actionM -- (Optional) ImportActions Enum element defining how to handle imports when the search_fields do match more then one pre-existing object.
        files -- (Optional) List of strings containing file path to import into a document object.
        """


        object_element = X('Object', s=[ X(
            'Search', s=[ search_fields_element := X('Fields') ]), 
            import_fields_element := X('Fields') 
        ])

        xml = X('DMSData', s=[
                X('Archive', s=[
                    X('ObjectType', {'internal_name': object_name}, [object_element])
                ])
        ])
        
        folder_id and object_element.set('folder_id', str(folder_id))
        register_id and object_element.set('register_id', str(register_id))
        object_id and object_element.set('object_id', str(object_id))

        for field_internal_name, field_value in search_fields.items():
            field = X('Field', a={'internal_name': field_internal_name}, t=field_value)
            if field_internal_name in SystemFields._member_names_:
                field.set('system', '1')
            search_fields_element.append(field)

        for field_internal_name, field_value in import_fields.items():
            field = X('Field', a={'internal_name': field_internal_name}, t=field_value)
            if field_internal_name in SystemFields._member_names_:
                field.set('system', '1')
            import_fields_element.append(field)

        if table_fields != None and len(table_fields):
            object_element.append(table_fields_element := X('TableFields'))
            for table_field_internal_name, table_field_rows in table_fields.items():
                table_field = X('TableField', {'internal_name': table_field_internal_name})
                table_fields_element.append(table_field)
                for table_field_row in table_field_rows:
                    table_field.append(X('Row', s=[ X(
                        'Field', {'internal_name': table_row_field_internal_name}, t=table_row_field_value) \
                            for table_row_field_internal_name, table_row_field_value in table_field_row.items()
                    ]))

        job = Job('dms.XMLImport', Flags=0, Options=options, 
            Action0=action0.value, Action1=action1.value, ActionM=actionM.value, 
            files=files, Encoding='UTF-8', XML=xml
        )

        return self.execute(job)

    def get_object_details(self, object_name:str, object_id:int, system_fields:Optional[List[SystemFields]]=[]) -> dict:
            query_fields = []
            for system_field in system_fields:
                query_field = X('Field', {'internal_name': system_field.name, 'system': '1'})
                query_fields.append(query_field)

            query_xml = X('DMSQuery', {}, [
                X('Archive', {} , [
                    X('ObjectType', {'internal_name': object_name}, [
                        X('Fields', {'field_schema': 'ALL'}, query_fields),
                        X('Conditions', {}, [
                            X('ConditionObject', {'internal_name': object_name}, [
                                X('FieldCondition', {'internal_name': SystemFields.OBJECT_ID.name, 'operator': '=', 'system': '1'}, [
                                    X('Value', t=str(object_id))
                                ])
                            ])
                        ])
                    ])
                ])
            ])

            job = Job('dms.GetResultList', Flags=0, Encoding='UTF-8', RequestType='HOL', XML=query_xml)
            result = self.execute(job)
            if result.return_code != 0:
                raise(Exception(f'Failed with error code: {result.return_code}'))

            if result.values['Count'] == 0:
                return {}

            result_xml = X.from_string(result.values['XML'])
            obj_xml = result_xml.Archive[0].ObjectType[0].ObjectList[0].Object[0]

            result = {}
            for field in obj_xml.Fields[0].Field:
                result[field.attributes['internal_name']] = field.text

            return result

    def execute_sql(self, sql_command:str) -> Union[List[Dict[str, str]], None]:
        """Helper function: Execute a sql command via ADO.

        Keyword arguments:
        
        - sql_command -- The sql command.

        Returns:
        
        - For SELECT statements: `List[Dict]` -- The list of records with each row as dictionary of column name and string-value
        - For other statements: `None`
        """
        
        job = Job('ado.ExecuteSQL', Flags=0, Command=sql_command.strip())
        result = self.execute(job)
        if result.return_code != 0:
            raise Exception(f'Failed with error code: {result.return_code}')

        if result.files:
            xml_result = X.from_string(result.files[0].bytes().decode('UTF-8'))
            data = [ row.attributes for row in xml_result['{urn:schemas-microsoft-com:rowset}data'][0]['{#RowsetSchema}row'] ]
            return data
        else:
            return None