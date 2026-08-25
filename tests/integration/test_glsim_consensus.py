from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Independently review one translation segment"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"quality": "FAITHFUL", "term_mask": "11"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_segment_acceptance():
    client, translator = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "translation_check.py")
    standard = "Preserve meaning, numbers, negation, and named entities. Use every required target-language term in its intended sense."
    deployed = factory.deploy_contract_tx(args=[translator.address, "English", "Spanish", standard], account=client, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    owner = factory.build_contract(address, account=client)
    worker = factory.build_contract(address, account=translator)
    ok(owner.add_segment(args=["s1", "The community library opens at nine and closes at six on weekdays.", "biblioteca comunitaria,días laborables", 2]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.lock_document(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(worker.submit_segment(args=["s1", "La biblioteca comunitaria abre a las nueve y cierra a las seis los días laborables."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(worker.review_segment(args=["s1"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    assert owner.get_document(args=[]).call()["phase"] == "COMPLETE"

