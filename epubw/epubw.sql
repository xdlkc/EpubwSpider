create database if not exists epubw;
use epubw;
create table book
(
    id           bigint primary key auto_increment,
    name         varchar(256) not null comment '书名',
    author       varchar(256) comment '作者',
    publish_date date comment '出版日期',
    publisher    varchar(64) comment '出版社',
    url          varchar(256) comment '网盘地址',
    first_url    varchar(256) comment '一级地址',
    isbn         varchar(64) comment '图书编号',
    create_time  datetime default current_timestamp,
    update_time  datetime default current_timestamp on update current_timestamp,
    version      bigint   default 1   not null,
    key name_i (name),
    unique index first_url_i (first_url)
);
insert into epubw.book (name, author, publish_date, first_url, isbn, publisher)
values ('%s', '正月初三', '2019-08-02', '%s', '%s', '%s');
select *
from book
where name like '%马原藏区小说精品%';