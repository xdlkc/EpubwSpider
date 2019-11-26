-- auto-generated definition
use epubw;
create table book
(
    id           bigint auto_increment
        primary key,
    name         varchar(256)                       not null comment '书名',
    author       varchar(256)                       null comment '作者',
    publish_date date                               null comment '出版日期',
    publisher    varchar(64)                        null comment '出版社',
    first_url    varchar(256)                       null comment '一级地址',
    second_url   varchar(256)                       null comment '二级地址',
    third_url    varchar(256)                       null comment '三级地址',
    pan_url      varchar(256)                       null comment '网盘地址',
    img          varchar(256)                       null comment '图书图片',
    isbn         varchar(64)                        null comment '图书编号',
    create_time  datetime default CURRENT_TIMESTAMP null,
    update_time  datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    version      bigint   default 1                 not null,
    secret       varchar(16)                        null,
    constraint first_url_i
        unique (first_url)
);

create index name_i
    on book (name);

