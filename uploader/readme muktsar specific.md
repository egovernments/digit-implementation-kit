------------------------------
SURVEY DATA MIGRATION ONLY
-----------------------------

	   
List of OwnerTypes (No information available for muktsar)
				NA
				Not Applicable
				Widow
				Defense Person
				Handicapped 

As muktsar records received contains manual enteries also for session 2018-19 or below, 
	
		1. Check '/' in owner name in owner column
		   
updated unit map from building_categories and unit usages
	BD_UNIT_MAP = {
		"Residential Houses": (None, None, None),
		"Residential House": (None, None, None),
		

	# "Government buildings, including buildings of Government Undertakings, Board or Corporation": "",
	# Institutional Building,Community Hall,Social Clubs,Sports stadiums,Bus Stand, and Such like Building
	    "Industrial (any manufacturing unit), educational institutions, and godowns": (
		"INDUSTRIAL", "OTHERINDUSTRIALSUBMINOR", "OTHERINDUSTRIAL"),
		"Commercial buildings including Restaurants (except multiplexes, malls, marriage palaces)": (
		"COMMERCIAL", "OTHERCOMMERCIALSUBMINOR", "OTHERCOMMERCIAL"),
    	"Commercial Buildings except Multiplexes, Malls, Marriage Palaces": ("COMMERCIAL", "OTHERCOMMERCIALSUBMINOR", "OTHERCOMMERCIAL"),
	    "Commercial Buildings except Multiplexes, Malls, Marriage Palaces,Godown":("COMMERCIAL", "OTHERCOMMERCIALSUBMINOR", "OTHERCOMMERCIAL"),
		"Flats": (""),
		"Commercial Buildings except Multiplexes, Malls, Marriage Palaces,Parking space (only in respect of multi-storey flats or buildings).":(""),
		"Hotels - Having beyond 50 rooms": ("COMMERCIAL", "HOTELS", None),
		"Hotel": ("COMMERCIAL", "HOTELS", None),
		"Others": ("COMMERCIAL", "OTHERCOMMERCIALSUBMINOR", "OTHERCOMMERCIAL"),
		# "Mix-Use Building used for multiple purposes (like Residential+Commercial+Industrial)": "",
		"Institutional buildings (other than educational institutions), including community halls/centres, sports stadiums, social clubs, bus stands, gold clubs, and such like buildings used for public purpose": (
			"INSTITUTIONAL", "OTHERINSTITUTIONALSUBMINOR", "OTHERINSTITUTIONAL"),
		"Hotels - Having 50 rooms or below": ("COMMERCIAL", "HOTELS", None),
		"Multiplex, Malls, Shopping Complex/Center etc.": ("COMMERCIAL", "RETAIL", "MALLS"),
		"Vacant Plot": (None, None, None),
		"Vacant Plot(Commercial)": (None, None, None),
		"Vacant Plot(Residential)": (None, None, None),
		"Marriage Palaces": ("COMMERCIAL", "EVENTSPACE", "MARRIAGEPALACE"),
		"Petrol Pump":("COMMERCIAL", "OTHERCOMMERCIALSUBMINOR", "OTHERCOMMERCIAL"),
		"Multiplex": ("COMMERCIAL","ENTERTAINMENT","MULTIPLEX"),
		"Mall": ("COMMERCIAL","RETAIL","ESTABLISHMENTSINMALLS"),
		"Gas Godown": ("COMMERCIAL", "OTHERCOMMERCIALSUBMINOR", "OTHERCOMMERCIAL"),
		"Commercial Buildings except Multiplexes, Malls, Marriage Palaces,Residential House":("COMMERCIAL", "OTHERCOMMERCIALSUBMINOR", "OTHERCOMMERCIAL")
		
	}

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


------------------------------------------------
Preparing Legacy DB Data
------------------------------------------------
CREATE TABLE muktsar_pt_survey_data (
		srno text,
		returnid text,
		acknowledgementno text,
		entrydate text,
		zone text,
		sector text,
		colony text,
		houseno text,
		owner text,
		leasedetail text,
		address text,
		floor text,
		unbuiltarea text,
		exemptioncategory text,
		landusedtype text,
		usage text,
		plotarea text,
		totalcoveredarea text,
		propertytype text,
		buildingcategory text,
		remarks text,
		businessname text,
		waterconnectionno text,
		electrictyconnectionno text,
		photoid text,
		client_data_id text,
		name_of_surveyer,
		mobile_detail,
		other_detail,
		
			
		----------------
		uuid text default uuid_generate_v4(),
		previous_returnid text,
		status text default 'stage1'::text,
		tenantid text,
		batchname text,
		new_propertyid text,
		upload_status text,
		upload_response text,
		new_assessmentnumber text,
		new_tax text,
		new_total text,
		req_json text,
		time_taken float8,
		new_locality_code text,
		receipt_status text,
		receipt_request text,
		receipt_response text,
		receipt_number text,
		time_taken_receipt float8,
		parent_uuid text,
		colony_processed text,
		upload_response_workflow text,
		upload_response_assessment text
	);

CREATE INDEX IF NOT EXISTS idx_muktsar_survey_data_uuid on muktsar_survey_data(uuid);
CREATE INDEX IF NOT EXISTS idx_muktsar_survey_data_puuid on muktsar_survey_data(parent_uuid);
CREATE INDEX IF NOT EXISTS idx_muktsar_survey_data_ustatus on muktsar_survey_data(upload_status);
CREATE INDEX IF NOT EXISTS idx_muktsar_survey_data_rid on muktsar_survey_data(returnid);
CREATE INDEX IF NOT EXISTS idx_muktsar_survey_data_csector on muktsar_survey_data(colony, sector);
CREATE INDEX IF NOT EXISTS idx_muktsar_survey_data_locality on muktsar_survey_data(new_locality_code);
CREATE INDEX IF NOT EXISTS idx_muktsar_survey_data_colony_processed on muktsar_survey_data(colony_processed);

CREATE TABLE muktsar_boundary (
		code text,
		colony text,
		sector text,
		area text,
		colony_processed text
	);

CREATE INDEX IF NOT EXISTS idx_muktsar_boundary_code on muktsar_boundary(code);
CREATE INDEX IF NOT EXISTS idx_muktsar_boundary_colony on muktsar_boundary(colony);
CREATE INDEX IF NOT EXISTS idx_muktsar_boundary_sector on muktsar_boundary(sector);
CREATE INDEX IF NOT EXISTS idx_muktsar_boundary_colony_processed on muktsar_boundary(colony_processed);

-- Set the FILLFACTOR to 50% so large updates don't take time
	ALTER TABLE muktsar_survey_data SET (FILLFACTOR = 50);
	VACUUM FULL muktsar_survey_data;
	REINDEX TABLE muktsar_survey_data;
```


```csv(returnid,colony,houseno,owner,guardianname,mobileno,address,floor,landusedtype,usage,plotarea,totalcoveredarea,occupancy,propertytype,buildingcategory,new_locality_code,businessname)

```


```pgsql
	COPY muktsar_pt_survey_data(returnid,colony,houseno,owner,guardianname,mobileno,address,floor,landusedtype,usage,plotarea,totalcoveredarea,occupancy,propertytype,buildingcategory,new_locality_code,businessname)		
	FROM 'F:\legacy data\Muktsar Sahib\muktsar_survey_data_under_processing_utf8.csv'
	WITH (format csv, QUOTE '"', header);
	```



select * from  muktsar_survey_data

update muktsar_pt_survey_data set owner=split_part(owner,'/',1)   where owner like '%/%'

update muktsar_pt_survey_data set guardianname=split_part(guardianname,'/',1)   where guardianname like '%/%'

Some of Government Building received as ownertype(land_used_type) "Citizen Propery", it should be updated to Government property as under
			select * from muktsar_survey_data 
			--update muktsar_survey_data set landusedtype='State Government Property' 
			where buildingcategory='Government building' and landusedtype='Citizen Property'
		   


	Now that the data is imported, we want to be able to identify each record using a unique identifier, so we assign a `uuid` to each record


	```pgsql
	update muktsar_survey_data set uuid = uuid_generate_v4();

	update muktsar_survey_data set 
	new_propertyid = NULL, upload_status = NULL, receipt_status = NULL, receipt_number = NUll, receipt_request = null, receipt_response = null, req_json = Null, parent_uuid = Null, upload_response = null;
	```










	In the DB assign the batch id to each record (assumed 10 in this case)

	```PGSQL
	update muktsar_survey_data set batchname =('{1,2,3,4,5,6,7,8,9,10}'::text[])[ceil(random()*10)] where upload_status is null;
	```

	After installing all the requirements, update the `run_pt_upload.sh`, use first with `DRY_RUN=True`, once the upload starts working use `DRY_RUN=False`  and use `BATCH_PARALLEL` to increase the number of parallel jobs 

	----------------------------------------------------------------
	AFTER MIGRATION
	-----------------------------------------------------------------

	To Settle the demands as all migrated assessments are to be set as paid
	-------------------------------------------------------------

	--update egbs_demanddetail_v1 set collectionamount=taxamount 
	--select count(*) from egbs_demanddetail_v1
	where demandid in (select d.id
	from egbs_demanddetail_v1 dd, egbs_demand_v1 d
	where dd.demandid=d.id
	--and d.status!='CANCELLED'
	and d.consumercode in (select propertyid from eg_pt_property where tenantId='pb.muktsar' and source='LEGACY_RECORD' and channel='LEGACY_MIGRATION' and status='ACTIVE' and createdtime>1633709138000)
	and consumercode not in (select distinct consumercode from egbs_bill_v1 bill, egbs_billdetail_v1 bd where status='ACTIVE' and bd.billid=bill.id and consumercode in (select propertyid from eg_pt_property where tenantId='pb.muktsar' and source='LEGACY_RECORD' and channel='LEGACY_MIGRATION' and status='ACTIVE' ))
	group by d.id)



	All Properties with RENTED units are made under status INWORKFLOW so that needed to be APPROVED before assessments
	---------------------------------------------------------------------------------------------------------------------- 
	--update eg_pt_property set status='INWORKFLOW' 
	--select count(*) from eg_pt_property
	where id in (select propertyid from eg_pt_unit where occupancytype='RENTED' and active='true') and status='ACTIVE' and tenantid='pb.muktsar' and source='LEGACY_RECORD' and channel='LEGACY_MIGRATION' and createdtime>1633709138000  


	----------------------------------------
	To set height above 36ft for all Flats
	----------------------------------------
	update eg_pt_property set additionaldetails=cast(concat('{ "heightAbove36Feet": true,',substring(additionaldetails::text,2)) as json)
	where additionaldetails->'legacyInfo'->>'buildingcategory'='Flat' and tenantid='pb.muktsar' and channel='LEGACY_MIGRATION' and source='LEGACY_RECORD' and status='ACTIVE' 
	and createdtime>1633709138000  