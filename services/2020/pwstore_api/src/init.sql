begin transaction;

create table if not exists user (
    user_id             integer not null primary key autoincrement,
    name                text,
    pwhash              text,
    isadmin             integer 
);

create table if not exists pwentry (
    pw_id               integer not null primary key,
    user_id             integer not null,
    pw                  text,
    creation_timestamp  text,
    description         text,
    constraint user foreign key ('user_id') references pwentry('user_id') on delete cascade
);

commit;