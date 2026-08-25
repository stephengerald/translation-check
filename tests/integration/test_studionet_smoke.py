import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt)
    return receipt


@pytest.mark.integration
def test_studionet_translation_review(default_account, secondary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "translation_check.py")
    standard = "Preserve meaning, numbers, negation, and named entities. Use every required target-language term in its intended sense."
    deployed = _ok(factory.deploy_contract_tx(args=[secondary_account.address, "English", "Spanish", standard], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    client = factory.build_contract(address, account=default_account)
    translator = factory.build_contract(address, account=secondary_account)
    _ok(client.add_segment(args=["s1", "The community library opens at nine and closes at six on weekdays.", "biblioteca comunitaria,días laborables", 2]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(client.lock_document(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(translator.submit_segment(args=["s1", "La biblioteca comunitaria abre a las nueve y cierra a las seis los días laborables."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = _ok(translator.review_segment(args=["s1"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    segment = client.get_segment(args=["s1"]).call()
    assert segment["quality"] in ("FAITHFUL", "MINOR_ISSUE", "MAJOR_ISSUE")
    assert len(segment["term_mask"]) == 2
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": segment["quality"] + "/" + segment["term_mask"]}, sort_keys=True, ensure_ascii=False))
