def parse_ai_mcqs(raw_text):
    parsed = []
    blocks = raw_text.split("## MCQ")

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        try:
            if "Question:" not in block:
                continue

            # Split lines cleanly
            lines = [line.strip() for line in block.split("\n") if line.strip()]

            # Extract question
            question_line = next(line for line in lines if line.startswith("Question:"))
            question = question_line.replace("Question:", "").strip()

            # Extract options (next 4 meaningful lines)
            option_lines = []
            for line in lines:
                if line.startswith(("A)", "B)", "C)", "D)")):
                    option_lines.append(line)

            # Fallback if labels are missing
            if len(option_lines) < 4:
                raw_options = [
                    line for line in lines
                    if not line.startswith("Question:")
                    and not line.lower().startswith("correct answer")
                ][:4]

                option_lines = [
                    f"A) {raw_options[0]}",
                    f"B) {raw_options[1]}",
                    f"C) {raw_options[2]}",
                    f"D) {raw_options[3]}",
                ]

            # Extract correct answer
            correct = "Not provided"
            for line in lines:
                if line.lower().startswith("correct answer"):
                    correct = line.split(":", 1)[1].strip()

            parsed.append({
                "question": question,
                "options": option_lines,
                "correct": correct
            })

        except Exception:
            # Never crash UI
            continue

    return parsed
