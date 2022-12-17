DROP TABLE IF EXISTS list_cluster;

CREATE TABLE list_cluster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tgl TEXT NOT NULL,
    ot TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    depth INTEGER NOT NULL,
    mag TEXT NOT NULL,
    remark TEXT NOT NULL,
    cluster TEXT NOT NULL
);
