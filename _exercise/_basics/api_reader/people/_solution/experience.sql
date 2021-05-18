#############################################
## step 1. raw experience data by person
create or replace table people.experience_data_bytes
as
    select 1 as pid, to_base64(cast('hello' as bytes)) bytes_data
        limit 0;

### optional: hold experience data by person in temporary table
create or replace table people.experience_data_tmp_01
as
    select to_base64(cast('hello' as bytes)) bytes_data
        limit 0;

## step 2. decoded json data
create or replace table people.experience_data
as
    select pid, cast(from_base64(bytes_data) as string) as json_data
        from people.experience_data_bytes;

## step 3. build people / company data
create or replace table people.experiences
as
    select  pid,
            trim(json_extract(json_data, '$.company.name'), '"') as company,
            trim(json_extract(json_data, '$.company.id'), '"') as company_id,
            date(concat(trim(json_extract(json_data, '$.start_date'), '"'), '-01')) as start_date,
            date(concat(trim(json_extract(json_data, '$.end_date'), '"'), '-15')) as end_date,
            json_extract(json_data, '$.is_primary') as is_primary
        from people.experience_data;

## step 4. analytics
### check duration
select *, generate_date_array(start_date, ifnull(end_date, current_date()), interval 1 day) as duration
    from people.experiences

with dt as (
    select pid, company_id, work_day, date_trunc(work_day, MONTH) as work_month
        from people.experiences
            cross join unnest(generate_date_array(start_date, ifnull(end_date, current_date()), interval 1 day)) as work_day
)
select *
    from dt
        order by pid, work_day;

create or replace table people.employee_count
as
    with dt as (
        select distinct pid, company_id, date_trunc(work_day, MONTH) as work_month
            from people.experiences
                cross join unnest(generate_date_array(start_date, ifnull(end_date, current_date()), interval 1 day)) as work_day
    )
    select company_id, work_month, count(1) as employee_counts
        from dt
            group by company_id, work_month
        order by company_id, work_month;


#############################################
## step 5. cache db / postgres
* no operation data
* refreshed regularly by importing from bigquery
drop table employee_count;
create table employee_count (
   company_id varchar(128) not null,
   work_month date not null,
   employee_counts int not null
);

-- ## step 6: query table
select * from employee_count where company_id = 'Banana' and work_month = to_date('2020-03-01', 'YYYY-MM-DD');
 company_id | work_month | employee_counts
------------+------------+-----------------
 Banana     | 2020-03-01 |               4
(1 row)

## rest service consideration:
* Framework: restplus ...
* redis cache
