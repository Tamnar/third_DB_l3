#!/usr/bin/env python
import itertools
import pprint

from .dynamicsearch import *

__all__ = [
	f"BookDynamicSearch",
	f"UserLoanDynamicSearch", ]


class BookDynamicSearch(DynamicSearchBaseORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name: str = f"Books"
		BooksData = self.schema.tables.BooksData.ORM
		Authors = self.schema.tables.Authors.ORM
		self.search: dict[self.SearchCriteriasORM[CompareConstantORM]] = {
			f"Author": SearchCriteriasORM(Authors.Name),
			f"Name": SearchCriteriasORM(BooksData.Name),
			f"PubYear": SearchCriteriasORM(BooksData.PubYear),
			f"Price": SearchCriteriasORM(BooksData.Price),
		}

	@property
	def ORM_join(self):
		Books = self.schema.tables.Books.ORM
		BooksData = self.schema.tables.BooksData.ORM
		Authors = self.schema.tables.Authors.ORM
		q = \
			Books.select(Authors.Name, BooksData.Name, BooksData.PubYear, BooksData.Price) \
			.join(BooksData, on=(BooksData.id == Books.DataID)) \
			.join(Authors, on=(BooksData.AuthorID == Authors.id))
		return q


class UserLoanDynamicSearch(DynamicSearchBaseORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name: str = "UsersLoan"
		BooksData = self.schema.tables.BooksData.ORM
		Users = self.schema.tables.Users.ORM
		Loan = self.schema.tables.Loan.ORM
		self.search: dict[self.SearchCriteriasORM[CompareConstantORM]] = {
			f"Name": SearchCriteriasORM(Users.Name),
			f"Surname": SearchCriteriasORM(Users.Surname),
			f"Patronymic": SearchCriteriasORM(Users.Patronymic),
			f"Address": SearchCriteriasORM(Users.Address),
			f"LoanDate": SearchCriteriasORM(Loan.LoanDate),
			f"ReturnDate": SearchCriteriasORM(Loan.ReturnDate),
			f"DesiredReturnDate": SearchCriteriasORM(Loan.DesiredReturnDate),
			f"BookName": SearchCriteriasORM(BooksData.Name),
		}

	@property
	def ORM_join(self):
		BooksData = self.schema.tables.BooksData.ORM
		Books = self.schema.tables.Books.ORM
		Users = self.schema.tables.Users.ORM
		Loan = self.schema.tables.Loan.ORM
		q = \
			Users.select(
				Users.Name,
				Users.Surname,
				Users.Patronymic,
				Users.Address,
				Loan.LoanDate,
				Loan.ReturnDate,
				Loan.DesiredReturnDate,
				BooksData.Name,
			) \
			.join(Loan, on=(Users.id == Loan.UserID)) \
			.join(Books, on=(Loan.BookID == Books.id)) \
			.join(BooksData, on=(Books.DataID == BooksData.id))
		return q


def _test():
	pass


if __name__ == "__main__":
	_test()
