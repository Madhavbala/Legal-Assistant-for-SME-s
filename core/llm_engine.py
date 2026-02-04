from core.ip_rules import infer_ip_meaning

def analyze_clause_with_llm(clause, lang):

    client = get_groq_client()

    rule_result = infer_ip_meaning(clause)

    if client is None:
        return rule_result

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": build_prompt(clause, lang)}],
            temperature=0
        )

        llm_result = parse(response.choices[0].message.content)

        # Fill missing fields using rules
        for key in ["ownership", "exclusivity", "risk_reason", "suggested_fix"]:
            if llm_result.get(key) in ["Unclear", "", None]:
                llm_result[key] = rule_result[key]

        return llm_result

    except Exception:
        return rule_result
