-- CREATE DATABASE forum;

-- unvid 1 = Columbia
-- did 1 = secondhand

USE forum;

DROP TABLE categories;
DROP TABLE users;
DROP TABLE secondhand;

CREATE TABLE categories(
    `did` INT(5) unvidSIGNED NOT NULL, 
    `unvid` INT(3) UNSINGED NOT NULL, 
    `name` VARCHAR(20),
    PRIMARY KEY (`did`, `unvid`));

CREATE TABLE users(
    `uid` INT(7) UNSIGNED NOT NULL PRIMARY KEY,
    `unvid` INT(3) UNSINGED NOT NULL, 
    `name` VARCHAR(15),
    FOREIGN KEY(unvid) REFERENCE categories(unvid));

CREATE TABLE secondhand(
    tid INT(7) UNSIGNED NOT NULL, 
    did INT(5) UNSIGNED NOT NULL, 
    uid INT(7) UNSIGNED NOT NULL, 
    postdate DATETIME, 
    content TEXT,
    PRIMARY KEY (tid, uid),
    FOREIGH KEY (uid) REFERENCE users(uid),
    FOREIGH KEY (did) REFERENCE categories(did));

