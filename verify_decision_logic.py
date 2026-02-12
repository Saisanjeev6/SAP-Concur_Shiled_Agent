from concur_shield.agents.audit_escalation.tools import make_audit_decision

def test_decision_logic():
    print("Testing decision logic...")

    # Test APPROVED case
    result_approved = make_audit_decision(
        employee_id="EMP001",
        total_amount=100.0,
        total_expenses=2,
        policy_rejected=0,
        policy_needs_review=0,
        fraud_risk_score=10,
        fraud_risk_level="LOW",
        total_violations=0,
        total_fraud_signals=0
    )
    print(f"Case 1 (Low Risk): {result_approved['decision']}")
    assert result_approved['decision'] == "APPROVED", f"Expected APPROVED, got {result_approved['decision']}"

    # Test REJECTED case (High Risk Score)
    result_high_risk = make_audit_decision(
        employee_id="EMP002",
        total_amount=1000.0,
        total_expenses=5,
        policy_rejected=0,
        policy_needs_review=0,
        fraud_risk_score=60, # > 50
        fraud_risk_level="HIGH",
        total_violations=0,
        total_fraud_signals=0
    )
    print(f"Case 2 (Risk Score 60): {result_high_risk['decision']}")
    assert result_high_risk['decision'] == "REJECTED", f"Expected REJECTED, got {result_high_risk['decision']}"

    # Test REJECTED case (Policy Rejections)
    result_policy_rejected = make_audit_decision(
        employee_id="EMP003",
        total_amount=500.0,
        total_expenses=3,
        policy_rejected=1, # >= 1
        policy_needs_review=0,
        fraud_risk_score=10,
        fraud_risk_level="LOW",
        total_violations=1,
        total_fraud_signals=0
    )
    print(f"Case 3 (Policy Rejected): {result_policy_rejected['decision']}")
    assert result_policy_rejected['decision'] == "REJECTED", f"Expected REJECTED, got {result_policy_rejected['decision']}"

    # Test REJECTED case (Fraud Signals)
    result_fraud_signals = make_audit_decision(
        employee_id="EMP004",
        total_amount=500.0,
        total_expenses=3,
        policy_rejected=0,
        policy_needs_review=0,
        fraud_risk_score=10,
        fraud_risk_level="LOW",
        total_violations=0,
        total_fraud_signals=2 # >= 2
    )
    print(f"Case 4 (Fraud Signals): {result_fraud_signals['decision']}")
    assert result_fraud_signals['decision'] == "REJECTED", f"Expected REJECTED, got {result_fraud_signals['decision']}"

    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_decision_logic()
