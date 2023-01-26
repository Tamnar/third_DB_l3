#!/usr/bin/env python3

# import psycopg2
# import psycopg2.sql
# import psycopg2.extensions
import Lab.utils
import peewee


from . import DynamicSearch
from .AutoSchema import *


database_proxy = peewee.DatabaseProxy()


class Library_table(peewee.Model):  # (SchemaTable):
	class Meta:
		database = database_proxy
		schema = f"Library"


class Authors(Library_table):
	Name = peewee.CharField(max_length=127, null=False)


class BooksData(Library_table):
	AuthorID = peewee.ForeignKeyField(Authors, backref="publications")
	Name = peewee.CharField(max_length=127, null=False)
	PubYear = peewee.DateTimeField(null=False)
	Price = peewee.DecimalField(null=False)


class Books(Library_table):
	DataID = peewee.ForeignKeyField(BooksData, backref="books")


class Users(Library_table):
	Name = peewee.CharField(max_length=63, null=False)
	Surname = peewee.CharField(max_length=63, null=False)
	Patronymic = peewee.CharField(max_length=63, null=False)
	Address = peewee.CharField(max_length=255, null=False)


class Loan(Library_table):
	UserID = peewee.ForeignKeyField(Users, backref="loans")
	BookID = peewee.ForeignKeyField(Books, backref="loaned")
	LoanDate = peewee.DateTimeField()
	ReturnDate = peewee.DateTimeField()
	DesiredReturnDate = peewee.DateTimeField()


class AuthorsTable(SchemaTableORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ORM = Authors

	# def describe(self):
	# 	print(f"Authors")


class BooksDataTable(SchemaTableORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ORM = BooksData


class BooksTable(SchemaTableORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ORM = Books


class UsersTable(SchemaTableORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ORM = Users


class LoanTable(SchemaTableORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ORM = Loan

	def randomFill(self, instances=None, *args, **kwargs):
		if instances is None:
			instances = 100

		sql = f"""
			INSERT INTO "{self.schema}"."loan"("UserID_id", "BookID_id", "LoanDate", "ReturnDate", "DesiredReturnDate")
			SELECT
			(SELECT "id" FROM "{self.schema}"."users" ORDER BY random()*q LIMIT 1),
			(SELECT "id" FROM "{self.schema}"."books" ORDER BY random()*q LIMIT 1),

			timestamp '2020-01-01' + random() * (timestamp '2020-11-11' - timestamp '2020-01-01'),
			timestamp '2021-01-01' + random() * (timestamp '2021-11-11' - timestamp '2021-01-01'),
			timestamp '2021-01-01' + random() * (timestamp '2021-11-11' - timestamp '2021-01-01')
			FROM
			(VALUES('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) as symbols(characters),
			generate_series(1, {instances}) as q;
		"""
		super().randomFill(*args, **kwargs, sql_replace=sql)


class Library(Schema):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._dynamicsearch = {a.name: a for a in [DynamicSearch.BookDynamicSearch(self), DynamicSearch.UserLoanDynamicSearch(self)]}
		database_proxy.initialize(self.dbconn)
		# self.reoverride()

	def reoverride(self):
		# print(f"reoverride")
		# Table override

		self.tables.Authors = AuthorsTable(self, f"authors")
		self.tables.BooksData = BooksDataTable(self, f"booksdata")
		self.tables.Books = BooksTable(self, f"books")
		self.tables.Users = UsersTable(self, f"users")
		self.tables.Loan = LoanTable(self, f"loan")

	def reinit(self):
		# sql = f"""
		# 	SELECT table_name FROM information_schema.tables
		# 	WHERE table_schema = '{self}';
		# """
		with self.dbconn.cursor() as dbcursor:
			# dbcursor.execute(sql)
			for a in self.refresh_tables():  # tuple(dbcursor.fetchall()):
				q = f"""DROP TABLE IF EXISTS {a} CASCADE;"""
				# print(q)
				dbcursor.execute(q)

		self.dbconn.create_tables([Authors, BooksData, Books, Users, Loan])

		# tables = [
		# 	f"""CREATE SCHEMA IF NOT EXISTS "{self}";""",
		# 	f"""CREATE TABLE IF NOT EXISTS "{self}"."Authors" (
		# 		id bigserial,
		# 		"Name" character varying(127) NOT NULL,
		# 		CONSTRAINT "Authors_pkey" PRIMARY KEY (id)
		# 		-- UNIQUE("Name")
		# 	);
		# 	""",
		# 	f"""CREATE TABLE IF NOT EXISTS "{self}"."BooksData" (
		# 		id bigserial,
		# 		"AuthorID" bigint NOT NULL,
		# 		"Name" character varying(127) NOT NULL,
		# 		"PubYear" timestamp with time zone NOT NULL,
		# 		"Price" money,
		# 		CONSTRAINT "BooksData_pkey" PRIMARY KEY (id),
		# 		CONSTRAINT "BooksData_AuthorID_fkey" FOREIGN KEY ("AuthorID")
		# 			REFERENCES "{self}"."Authors" (id) MATCH SIMPLE
		# 			ON UPDATE NO ACTION
		# 			ON DELETE CASCADE
		# 			NOT VALID
		# 	);
		# 	""",
		# 	f"""CREATE TABLE IF NOT EXISTS "{self}"."Books" (
		# 		id bigserial,
		# 		"DataID" bigint NOT NULL,
		# 		CONSTRAINT "Books_pkey" PRIMARY KEY (id),
		# 		CONSTRAINT "Books_DataID_fkey" FOREIGN KEY ("DataID")
		# 			REFERENCES "{self}"."BooksData" (id) MATCH SIMPLE
		# 			ON UPDATE NO ACTION
		# 			ON DELETE CASCADE
		# 			NOT VALID
		# 	);
		# 	""",
		# 	f"""CREATE TABLE IF NOT EXISTS "{self}"."Users" (
		# 			id bigserial,
		# 			"Name" character varying(63) NOT NULL,
		# 			"Surname" character varying(63) NOT NULL,
		# 			"Patronymic" character varying(63) NOT NULL,
		# 			"Address" character varying(255) NOT NULL,
		# 			CONSTRAINT "Users_pkey" PRIMARY KEY (id)
		# 	);
		# 	""",
		# 	f"""CREATE TABLE IF NOT EXISTS "{self}"."Loan" (
		# 		id bigserial,
		# 		"UserID" bigint NOT NULL,
		# 		"BookID" bigint NOT NULL,
		# 		"LoanDate" timestamp with time zone,
		# 		"ReturnDate" timestamp with time zone,
		# 		"DesiredReturnDate" timestamp with time zone,
		# 		CONSTRAINT "Loan_pkey" PRIMARY KEY (id),
		# 		CONSTRAINT "Loan_BookID_fkey" FOREIGN KEY ("BookID")
		# 			REFERENCES "{self}"."Books" (id) MATCH SIMPLE
		# 			ON UPDATE NO ACTION
		# 			ON DELETE CASCADE
		# 			NOT VALID,
		# 		CONSTRAINT "Loan_UserID_fkey" FOREIGN KEY ("UserID")
		# 			REFERENCES "{self}"."Users" (id) MATCH SIMPLE
		# 			ON UPDATE NO ACTION
		# 			ON DELETE CASCADE
		# 			NOT VALID
		# 	);
		# 	""",
		# ]

		# with self.dbconn.cursor() as dbcursor:
		# 	for a in tables:
		# 		dbcursor.execute(a)

		self.dbconn.commit()

		self.refresh_tables()
		# self.reoverride()

	def randomFill(self):
		# self.tables.Authors.randomFill(5_000)
		# self.tables.Users.randomFill(10_000)
		# self.tables.BooksData.randomFill(1_000)
		# self.tables.Books.randomFill(50_000)
		# self.tables.Loan.randomFill(10_000)

		self.tables.Authors.randomFill(100)
		self.tables.Users.randomFill(200)
		self.tables.BooksData.randomFill(20)
		self.tables.Books.randomFill(300)
		self.tables.Loan.randomFill(600)

	# def dynamicsearch(self):
	# 	result = Lab.utils.LabConsoleInterface({
	# 		"Books": lambda: DynamicSearch.BookDynamicSearch(self),
	# 		# "UsersLoan": lambda: DynamicSearch.UserLoanDynamicSearch(self),
	# 		"return": lambda: Lab.utils.menuReturn(f"User menu return"),
	# 	}, promt=f"""Schema "{self}" dynamic search interface""")
	# 	return result


def _test():
	pass


if __name__ == "__main__":
	_test()
