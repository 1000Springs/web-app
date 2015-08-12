create or replace view public_location as (
    select * from  location
    where access <> 'SECRET'
);

create or replace view public_sample as (
    select s.* from sample s
    join public_location pl on s.location_id = pl.id
);

create or replace view public_chemical_data as (
    select cd.* from chemical_data cd
    join public_sample ps on cd.id = ps.chem_id
);

create or replace view public_image as (
    select i.* from image i
    join public_sample ps on i.sample_id = ps.id
);

create or replace view public_physical_data as (
    select pd.* from physical_data pd
    join public_sample ps on pd.id = ps.phys_id
);

create or replace view public_sample_taxonomy as (
    select st.* from sample_taxonomy st
    join public_sample ps on st.sample_id = ps.id
);

create or replace view public_taxonomy as (
    select t.* from taxonomy t
    join public_sample_taxonomy pst on pst.taxonomy_id = t.id
);

create or replace view public_confident_taxonomy as (
    select ct.* from confident_taxonomy ct
    join public_sample ps on ct.sample_id = ps.id
);