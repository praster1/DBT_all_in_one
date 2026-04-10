-- 서버/버전/모드 사전 점검
select version();

show databases;
show variables like 'sql_mode';
show variables like 'explicit_defaults_for_timestamp';

-- 개발용 schema 생성 가능 여부 점검
create database if not exists analytics;
