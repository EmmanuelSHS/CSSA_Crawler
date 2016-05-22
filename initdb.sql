USE forum;

DROP TABLE secondhand;

CREATE TABLE secondhand(
    tid INT(7) UNSIGNED NOT NULL,
    uid INT(7) UNSIGNED NOT NULL,
    postdate DATETIME,
    content TEXT,
    PRIMARY KEY (tid, uid));
