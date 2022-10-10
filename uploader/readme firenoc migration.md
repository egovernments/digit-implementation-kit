create table for firenoc_legacy_data with following field
-------------------------------------

CREATE TABLE firenoc_zira_legacy_data
(
  uuid text,
  no_of_buildings text,
  noc_type text,
  building_address text,
  areatype text,
  city text,
  subdistrict text,
  localitycode text,
  firestationid text,
  name_of_building text,
  usagetype text,
  usagesubtype text,
  height_of_building text,
  number_of_actual_floors text,
  number_of_basements text,
  builtup_area text,
  land_area text,
  covered_area_total text,
  parking_area text,
  left_surrounding text,
  right_surrounding text,
  back_surrounding text,
  front_surrounding text,
  date_of_approval text,
  application_id text,
  date_of_submission text,
  old_noc_no text,
  new_noc_no text,
  noc_valid_upto text,
  unique_application_id text,
  owner_name text,
  owner_address text,
  applicant_contact_no text,
  upload_status text,
  upload_request text,
  upload_response text,
  additionaldetails text,
)


csv file template format
--------------------------
noc_type,building_address,urban,city,subdistrict,localitycode,firestationid,name,usageType,usageSubType,height_of_building,number_of_actual_floors,number_of_basements,builtup_area,land_area,covered_area_total,parking_Area,leftSurrounding,rightsurrunding,back,front,date_of_approval,application_id,date_of_submission,old_noc_no,new_noc_no,noc_valid_upto,unique_application_id,owner_name,owner_address,applicant_contact_no

query to fetch data
---------------------
select applications.noc_type,building_address,'urban',fireStation_name as city,area_tehsil_name as subdistrict,'UNKNOWN' as localitycode,'zira' as firestationid,
 name_of_building as name,substring_index(building_category,".",1) as usageType,substring_index(building_category,".",-1) as usageSubType,
 height_in_mtr as height_of_building,
 number_of_actual_floors,number_of_basements,covered_area_total as builtup_area,land_area,covered_area_total,parking_Area as parking_Area,surrounding_left as leftSurrounding,surrounding_right as rightsurrunding,surrounding_back as back,surrounding_front as front,
 date_of_approval,application_id,payment_date as date_of_submission,old_noc_no,concat(applications.unique_application_number,'/',noc_no) as  new_noc_no,expiry_date as noc_valid_upto,unique_application_number as unique_application_id,
 Owner_name as Owner_name,concat(owner_address,',',owner_city,"','",owner_state) as owenr_address,Applicant_contact_no as contact_no
from applications
inner join noc_issued on applications.application_id=noc_issued.application_no
where applications.current_status='Approved'

assigining uuids
-------------------

update firenoc_zira_legacy_data set uuid = uuid_generate_v4();