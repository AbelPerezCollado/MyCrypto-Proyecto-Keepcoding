CREATE TABLE "movimientos" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"moneda_from"	TEXT NOT NULL,
	"cantidad_from"	REAL NOT NULL,
	"moneda_to"	TEXT NOT NULL,
	"cantidad_to"	REAL NOT NULL
);