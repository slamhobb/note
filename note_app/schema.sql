drop table if exists user;
create table user(
    id integer primary key autoincrement,
    login text not null,
    viber_id text not null
);

create index pk_user_id on user(id);
create unique index uq_user_viber_id on user(viber_id);


drop table if exists auth_token;
create table auth_token(
    id integer primary key autoincrement,
    user_id integer not null,
    token text not null
);

create index pk_auth_token_id on auth_token(id);
create index ix_auth_token_token_user_id on auth_token(token, user_id);


drop table if exists note_type;
create table note_type(
    id integer primary key autoincrement,
    user_id integer not null,
    name text not null
);

create index pk_note_type_id on note_type(id);
create index ix_note_type_user_id on note_type(user_id);

insert into note_type(user_id, name) values (0, 'Общие');


drop table if exists note;
create table note(
    id integer primary key autoincrement,
    user_id integer not null,
    text text not null,
    note_type_id integer not null,
    create_date text not null,
    modify_date text not null,
    hidden integer not null
);

create index pk_note_id on note(id);
create index ix_note_user_id_note_type_id_hidden
    on note(user_id, note_type_id, hidden);


drop table if exists birthday;
create table birthday(
    id integer primary key autoincrement,
    user_id integer not null,
    birth_date text not null,
    name text not null
);

create index pk_birthday_id on birthday(id);
create index ix_birthday_user_id on birthday(user_id);
