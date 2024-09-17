from typing import Sequence
from unittest.mock import patch
from click import Abort
from pandas import DataFrame
from pytest import fixture
import pytest
import typer
from typer.testing import CliRunner
from sqlalchemy.orm import Session

from fam.command.adding.action import add_new_statement
from fam.database.users.models import ClassificationTable, SubCategoryTable
from fam.enums import BankEnum, FinancialProductEnum
from fam.main import app

COMMAND_WITH_BMO_CREDIT_CARD = ["add", "statement", "-b", "bmo", "-p", "credit card"]
COMMAND_WITH_TANGERINE = [""]

classification: Sequence[ClassificationTable] = [ClassificationTable()]
subcategory: Sequence[SubCategoryTable] = [SubCategoryTable()]


@fixture
def mock_local_build_choice():
    with patch(
        "fam.command.adding.action.build_choice",
        autospec=True,
    ) as mock:
        yield mock


def test_add_new_statement_raises_abort_if_no_subcategories(
    runner: CliRunner,
    mock_get_subcategory_and_classification,
):

    with pytest.raises(typer.Abort):

        mock_get_subcategory_and_classification.return_value = None, classification
        db: Session = Session()
        df: DataFrame = DataFrame()

        add_new_statement(
            bank=BankEnum.BMO,
            db=db,
            df=df,
            nickname_id=1,
            product=FinancialProductEnum.CREDIT_CARD,
        )

    mock_get_subcategory_and_classification.assert_called_once()


def test_add_new_statement_raises_abort_if_no_classification(
    mock_get_subcategory_and_classification,
):

    with pytest.raises(typer.Abort):

        mock_get_subcategory_and_classification.return_value = subcategory, None
        db: Session = Session()
        df: DataFrame = DataFrame()

        add_new_statement(
            bank=BankEnum.BMO,
            db=db,
            df=df,
            nickname_id=1,
            product=FinancialProductEnum.CREDIT_CARD,
        )

    mock_get_subcategory_and_classification.assert_called_once()


def test_add_new_statement_raise_abort_if_transaction_list_is_empty(
    mock_get_subcategory_and_classification,
    mock_categorize_transaction,
    mock_local_build_choice,
):

    with pytest.raises(typer.Abort):

        mock_get_subcategory_and_classification.return_value = (
            subcategory,
            classification,
        )
        mock_categorize_transaction.return_value = []
        mock_local_build_choice.return_value = {}, []
        db: Session = Session()
        df: DataFrame = DataFrame()

        add_new_statement(
            bank=BankEnum.BMO,
            db=db,
            df=df,
            nickname_id=1,
            product=FinancialProductEnum.CREDIT_CARD,
        )

    mock_get_subcategory_and_classification.assert_called_once()


def test_add_new_statement_with_bmo_credit_card_when_categorize_transaction_return_empty_list():
    pass
