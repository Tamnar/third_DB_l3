
DROP TABLE IF EXISTS "Library"."Authors";

CREATE TABLE IF NOT EXISTS "Library"."Authors"
(
    id bigserial,
    "Name" character varying(127) NOT NULL UNIQUE,
    CONSTRAINT "Authors_pkey" PRIMARY KEY (id)
)


DROP TABLE IF EXISTS "Library"."BooksData";

CREATE TABLE IF NOT EXISTS "Library"."BooksData"
(
    id bigserial,
    "AuthorID" bigint NOT NULL,
    "Name" character varying(127) NOT NULL,
    "PubYear" timestamp with time zone NOT NULL,
    "Price" money,
    CONSTRAINT "BooksData_pkey" PRIMARY KEY (id),
    CONSTRAINT "BooksData_AuthorID_fkey" FOREIGN KEY ("AuthorID")
        REFERENCES "Library"."Authors" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)


DROP TABLE IF EXISTS "Library"."Books";

CREATE TABLE IF NOT EXISTS "Library"."Books"
(
    id bigserial,
    "DataID" bigint NOT NULL,
    CONSTRAINT "Books_pkey" PRIMARY KEY (id),
    CONSTRAINT "Books_DataID_fkey" FOREIGN KEY ("DataID")
        REFERENCES "Library"."BooksData" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)


DROP TABLE IF EXISTS "Library"."Users";

CREATE TABLE IF NOT EXISTS "Library"."Users"
(
    id bigserial,
    "Name" character varying(63) NOT NULL,
    "Surname" character varying(63) NOT NULL,
    "Patronymic" character varying(63) NOT NULL,
    "Address" character varying(255) NOT NULL,
    CONSTRAINT "Users_pkey" PRIMARY KEY (id)
)


DROP TABLE IF EXISTS "Library"."Loan";

CREATE TABLE IF NOT EXISTS "Library"."Loan"
(
    id bigserial,
    "UserID" bigint NOT NULL,
    "BookID" bigint NOT NULL,
    "LoanDate" timestamp with time zone,
    "ReturnDate" timestamp with time zone,
    "DesiredReturnDate" timestamp with time zone,
    CONSTRAINT "Loan_pkey" PRIMARY KEY (id),
    CONSTRAINT "Loan_BookID_fkey" FOREIGN KEY ("BookID")
        REFERENCES "Library"."Books" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "Loan_UserID_fkey" FOREIGN KEY ("UserID")
        REFERENCES "Library"."Users" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)


