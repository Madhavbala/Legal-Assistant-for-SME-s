def infer_ip_meaning(clause: str):

    text = clause.lower()

    ownership = "Unclear"
    exclusivity = "Unclear"
    reason = ""
    fix = ""

    if "shall vest" in text or "vest exclusively" in text:
        ownership = "Company"
        exclusivity = "Yes"
        reason = (
            "The clause assigns all intellectual property ownership "
            "exclusively to the company, leaving the SME with no rights "
            "over work created during the engagement."
        )
        fix = (
            "Limit IP assignment to only deliverables created specifically "
            "for the company, or convert full ownership to a non-exclusive "
            "license for business use."
        )

    elif "exclusive" in text and "license" in text:
        ownership = "Company"
        exclusivity = "Yes"
        reason = (
            "An exclusive license prevents the SME from reusing its own work "
            "or licensing it to other clients."
        )
        fix = (
            "Change the exclusive license to a non-exclusive, royalty-free "
            "license limited to the contract purpose."
        )

    elif "intellectual property" in text:
        ownership = "Unclear"
        exclusivity = "Unclear"
        reason = (
            "The clause mentions intellectual property but does not clearly "
            "define ownership or usage rights."
        )
        fix = (
            "Explicitly define IP ownership and clarify whether usage rights "
            "are exclusive or non-exclusive."
        )

    return {
        "ownership": ownership,
        "exclusivity": exclusivity,
        "risk_reason": reason,
        "suggested_fix": fix
    }
