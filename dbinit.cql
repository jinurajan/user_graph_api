CREATE  KEYSPACE userdb WITH REPLICATION = {     'class' : 'SimpleStrategy',     'replication_factor' : 1    };
USE userdb;
CREATE TABLE user(email text PRIMARY KEY, name text, phone text, created_at int, updated_at int);
CREATE TABLE following_user_map(email text, following_user_email text, created_at int, PRIMARY KEY (email,following_user_email));