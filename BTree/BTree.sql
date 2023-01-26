
\timing on

DROP TABLE IF EXISTS "test_btree";
CREATE TABLE "test_btree"(
	"id" bigserial PRIMARY KEY,
	"test_text" varchar(255)
);

INSERT INTO "test_btree"("test_text")
SELECT
	substr(characters, (random() * length(characters) + 1)::integer, 10)
FROM
	(VALUES('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) as symbols(characters), generate_series(1, 1000000) as q;

SELECT COUNT(*) FROM "test_btree" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "test_btree" WHERE "id" % 2 = 0 OR "test_text" LIKE 'b%';
SELECT COUNT(*), SUM("id") FROM "test_btree" WHERE "test_text" LIKE 'b%' GROUP BY "id" % 2;

DROP INDEX IF EXISTS "test_btree_test_text_index";
CREATE INDEX "test_btree_test_text_index" ON "test_btree" USING btree ("test_text");

SELECT COUNT(*) FROM "test_btree" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "test_btree" WHERE "id" % 2 = 0 OR "test_text" LIKE 'b%';
SELECT COUNT(*), SUM("id") FROM "test_btree" WHERE "test_text" LIKE 'b%' GROUP BY "id" % 2; 

--------------------------------------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS "test_brin";
CREATE TABLE "test_brin"(
	"id" bigserial PRIMARY KEY,
	"test_time" timestamp
);

INSERT INTO "test_brin"("test_time")
SELECT
	(timestamp '2021-01-01' + random() * (timestamp '2020-01-01' - timestamp '2022-01-01'))
FROM
	(VALUES('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) as symbols(characters), generate_series(1, 1000000) as q;


SELECT COUNT(*) FROM "test_brin" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "test_brin" WHERE "test_time" >= '20200505' AND "test_time" <= '20210505';
SELECT COUNT(*), SUM("id") FROM "test_brin" WHERE "test_time" >= '20200505' AND "test_time" <= '20210505' GROUP BY "id" % 2;

DROP INDEX IF EXISTS "test_brin_test_time_index";
CREATE INDEX "test_brin_test_time_index" ON "test_brin" USING brin ("test_time");

SELECT COUNT(*) FROM "test_brin" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "test_brin" WHERE "test_time" >= '20200505' AND "test_time" <= '20210505';
SELECT COUNT(*), SUM("id") FROM "test_brin" WHERE "test_time" >= '20200505' AND "test_time" <= '20210505' GROUP BY "id" % 2;

--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS "reader";
CREATE TABLE "reader"(
	"readerID" bigserial PRIMARY KEY,
	"readerName" varchar(255)
);


DROP TABLE IF EXISTS "readerLog";
CREATE TABLE "readerLog"(
	"id" bigserial PRIMARY KEY,
	"readerLogID" bigint,
	"readerLogName" varchar(255)
);

--------------------------------------------------------------------------------------------------------------------------------

-- https://stackoverflow.com/questions/56544430/trigger-before-delete-doesnt-delete-data-in-table

CREATE OR REPLACE FUNCTION update_delete_func() RETURNS TRIGGER as $$

DECLARE
	CURSOR_LOG CURSOR FOR SELECT * FROM "readerLog";
	row_Log "readerLog"%ROWTYPE;

begin
	IF old."readerID" % 2 = 0 THEN
		INSERT INTO "readerLog"("readerLogID", "readerLogName") VALUES (old."readerID", old."readerName");
		UPDATE "readerLog" SET "readerLogName" = trim(BOTH 'x' FROM "readerLogName");
		RETURN NEW;
	ELSE 
		RAISE NOTICE 'readerID is odd';
		FOR row_log IN cursor_log LOOP
			UPDATE "readerLog" SET "readerLogName" = 'x' || row_Log."readerLogName" || 'x' WHERE "id" = row_log."id";
		END LOOP;
		RETURN NEW;
	END IF; 
END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER "test_trigger"
BEFORE UPDATE OR DELETE ON "reader"
FOR EACH ROW
EXECUTE procedure update_delete_func();

--------------------------------------------------------------------------------------------------------------------------------

INSERT INTO "reader"("readerName")
VALUES ('reader1'), ('reader2'), ('reader3'), ('reader4'), ('reader5');

SELECT * FROM "reader";
SELECT * FROM "readerLog";

UPDATE "reader" SET "readerName" = "readerName" || 'Lx' WHERE "readerID" = 5;
DELETE FROM "reader" WHERE "readerID" = 3;

--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS "task4";
CREATE TABLE "task4"(
	"id" bigserial PRIMARY KEY,
	"num" bigint,
	"char" varchar(255)
);

INSERT INTO "task4"("num", "char") VALUES (300, 'AAA'), (400, 'BBB'), (800, 'CCC');

SELECT * FROM "task4";

--------------------------------------------------------------------------------------------------------------------------------
-- -- READ UNCOMMITTED UNSUPPORTED
-- -- T1
-- START TRANSACTION;
-- SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED READ WRITE;
	
-- UPDATE "task4" SET "num" = "num" + 1;

-- COMMIT;
-- ROLLBACK;
-- -- /T1

-- -- T2
-- START TRANSACTION;
-- SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED READ WRITE;

-- SELECT * FROM "task4";

-- COMMIT;
-- -- /T2

--------------------------------------------------------------------------------------------------------------------------------
-- READ COMMITTED
-- T1
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED READ WRITE;
	
UPDATE "task4" SET "num" = "num" + 1;

COMMIT;
-- /T1

-- T2
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED READ WRITE;

SELECT * FROM "task4";

UPDATE "task4" SET "num" = "num" + 4;

COMMIT;
-- /T2

--------------------------------------------------------------------------------------------------------------------------------
-- REPEATABLE READ
-- T1
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ WRITE;
	
UPDATE "task4" SET "num" = "num" + 1;

COMMIT;
-- /T1

-- T2
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ WRITE;

SELECT * FROM "task4";

UPDATE "task4" SET "num" = "num" + 4;

COMMIT;
-- /T2

--------------------------------------------------------------------------------------------------------------------------------
-- SERIALIZABLE
-- T1
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE;
	
UPDATE "task4" SET "num" = "num" + 1;

COMMIT;
-- /T1

-- T2
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE;

SELECT * FROM "task4";

UPDATE "task4" SET "num" = "num" + 4;

COMMIT;
-- /T2


