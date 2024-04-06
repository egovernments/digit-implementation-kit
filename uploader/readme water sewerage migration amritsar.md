Amritsar Migration of Water and Sewerage Connections to mSeva: Documentation
----------------------------------------------------------------------------
Amritsar Property tax is already running on mSeva, Water & Sewerage module is to be used in mSeva for Amritsar which was earlier being handled by IKON

As in mSeva existance of property id is mandatory for WS connection, Received an excel from Amritsar with details of water & sewerage connections with columns as under

consumercode,block,propertyno,ownername,Mobile,guardian,guardianname,uidno,email,remarks,propertyusagetype,Service ,disconn_status,Nooftaps,area_in_sqy,ismetered,Localityname,DIGIT Localityname,DIGIT Locality code,streetname,Active,Arrear,Advance,LastBillDate

additional columns are added for support migration script in the excel and excel columns becomes
consumercode,block,propertyno,ownername,Mobile,guardian,guardianname,uidno,email,remarks,propertyusagetype,Service ,disconn_status,Nooftaps,area_in_sqy,ismetered,Localityname,DIGIT Localityname,DIGIT Locality code,streetname,Active,Arrear,Advance,LastBillDate,new_propertyid text,  batchname text,  upload_status text,  upload_req text,  upload_res text,  water_query_activate text,  uuid text,  sewerage_query_activate text,  new_water_application_number text,  new_sewerage_application_number text,  isdemandmigrated text,  property_creation_status text,  property_req text,  property_res text,  upload_batch text

create local database and table as below and import records from received excel to that table. this table is to be used by WS connection migration scripts

create database amritsar_ws_data

CREATE TABLE public.amritsar_ws_records
(
  consumercode text,
  block text,
  propertyno text,
  ownername text,
  mobile text,
  guardian text,
  guardianname text,
  uidno text,
  email text,
  remarks text,
  propertyusagetype text,
  service text,
  disconn_status text,
  nooftaps text,
  area_in_sqy text,
  ismetered text,
  localityname text,
  digit_localityname text,
  digit_locality_code text,
  streetname text,
  active text,
  meterno,
  arrear text,
  advance text,
  lastbilldate text,
  new_propertyid text,
  batchname text,
  upload_status text,
  upload_req text,
  upload_res text,
  water_query_activate text,
  uuid text,
  sewerage_query_activate text,
  new_water_application_number text,
  new_sewerage_application_number text,
  isdemandmigrated text,
  property_creation_status text,
  property_req text,
  property_res text,
  upload_batch text
)

against each water connection where propertyid (new_propertyid) is not present, then property should be created with status PENDINGWS,

set guradianname as 'NA' where null
brush the ownename, guradianname etc columns to remove special characters like /.-'` etc
plotsize in received excel may be 0 or below 2sqy which is not supported in mSeva property module, it should be set to min 2.0sqy

update amritsar_ws_records set upload_batch =('{1,2,3,4,5,6,7,8,9,10}'::text[])[ceil(random()*10)] where upload_status is null;

for property creation PropertyTaxDBProcess.py script is to be executed, it will create new property and will store back propertyid in new_propertyid column

after properties are created new_propertyid is stored against each WS connnection, then we have to set the status of newly created Properties to PENDINGWS through db query for UAT enviornment

update amritsar_ws_legacy_data set conn_type='B' where conn_type='Integrated Water & Sewerage'
update amritsar_ws_legacy_data set conn_type='W' where conn_type='Water'
update amritsar_ws_legacy_data set conn_type='S' where conn_type='Sewerage'

Step 2:
 Water and Sewerage Connections creation
 
Step 3:
 Demand and Arrear updations for water and sewerage connection

