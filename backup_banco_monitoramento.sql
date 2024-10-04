create database senai;
use senai;

GRANT ALL PRIVILEGES ON senai.* TO 'coletor'@'%' IDENTIFIED BY 'coletor';

show tables;

CREATE TABLE monitoramento(
id INT auto_increment primary KEY,
timestamp datetime,
hostname varchar(20),
ipv4 varchar(20),
logged_user varchar(20),
cpu_usage FLOAT,
memory_usage FLOAT,
disk_total FLOAT,
disk_usage FLOAT,
disk_free FLOAT,
disk_percent FLOAT,
kb_sent_per_sec FLOAT,
kb_recv_per_sec FLOAT
);

select * from monitoramento;