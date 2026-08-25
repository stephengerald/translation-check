from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "translation_check.py"
SDK = "v0.2.16"
PROMPT = "Independently review one translation segment"
STANDARD = "Preserve the source meaning, numbers, negation, and named entities. Use every required target-language term exactly in its intended sense. Stylistic variation is allowed when meaning remains faithful."


def deploy(vm, direct_deploy, alice, bob):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), "0x" + bob.hex(), "English", "Spanish", STANDARD, sdk_version=SDK)


def add_segment(contract):
    contract.add_segment("s1", "The community library opens at nine and closes at six on weekdays.", "biblioteca comunitaria,días laborables", 2)
    contract.lock_document()


def test_faithful_segment_and_terms_complete_document(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_bob)
    add_segment(contract)
    direct_vm.sender = direct_bob
    contract.submit_segment("s1", "La biblioteca comunitaria abre a las nueve y cierra a las seis los días laborables.")
    direct_vm.mock_llm(PROMPT, json.dumps({"quality": "FAITHFUL", "term_mask": "11"}))
    contract.review_segment("s1")
    assert contract.get_document()["phase"] == "COMPLETE"
    assert contract.get_segment("s1")["state"] == "ACCEPTED"
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_one_revision_repairs_meaning_and_terminology(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_bob)
    add_segment(contract)
    direct_vm.sender = direct_bob
    contract.submit_segment("s1", "La biblioteca abre a las nueve y cierra a las seis durante la semana.")
    direct_vm.mock_llm(PROMPT, json.dumps({"quality": "MINOR_ISSUES", "term_mask": "10"}))
    contract.review_segment("s1")
    assert contract.get_segment("s1")["state"] == "REVISION_REQUIRED"
    contract.submit_segment("s1", "La biblioteca comunitaria abre a las nueve y cierra a las seis los días laborables.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"quality": "FAITHFUL", "term_mask": "11"}))
    contract.review_segment("s1")
    assert contract.get_segment("s1")["revision_count"] == 1
    assert contract.get_document()["phase"] == "COMPLETE"


def test_translator_identity_and_mask_length_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_bob)
    add_segment(contract)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_translator"):
        contract.submit_segment("s1", "Una cuenta no relacionada no debe poder reemplazar el trabajo del traductor registrado.")
    direct_vm.sender = direct_bob
    contract.submit_segment("s1", "La biblioteca comunitaria abre a las nueve y cierra a las seis los días laborables.")
    direct_vm.mock_llm(PROMPT, json.dumps({"quality": "FAITHFUL", "term_mask": "1"}))
    with direct_vm.expect_revert("invalid_term_mask"):
        contract.review_segment("s1")
    assert contract.get_segment("s1")["state"] == "READY_FOR_REVIEW"

