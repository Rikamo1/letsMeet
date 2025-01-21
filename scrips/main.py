from mongodb import get_data_frame_from_db
from xml_to_Dataframe import get_dataframe_from_xml
from xlsx_to_df import get_data_frame_from_xlsx

print(get_data_frame_from_db())
print(get_dataframe_from_xml())
print(get_data_frame_from_xlsx())
