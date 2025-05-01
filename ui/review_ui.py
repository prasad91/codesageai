import json
import streamlit as st
from pathlib import Path

SUGGESTIONS_FILE = Path("../output/suggestions.json")

st.title("CodeSageAPI – Human-in-the-Loop Review")

if not SUGGESTIONS_FILE.exists():
    st.warning("No suggestions available. Trigger a PR webhook first.")
    st.stop()

data = json.loads(SUGGESTIONS_FILE.read_text())

for idx, item in enumerate(data):
    st.subheader(f"🔹 File: {item['file']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.code(item["original"], language="java")
    with col2:
        st.code(item["suggested"], language="java")

    decision = st.radio(
        f"Approve suggestion #{idx+1}?",
        options=["Approve", "Reject", "Edit"],
        key=f"decision_{idx}"
    )

    if decision == "Edit":
        edited = st.text_area("Edit the suggested code:", item["suggested"], key=f"edit_{idx}")
        item["edited"] = edited
    else:
        item["edited"] = None

    st.markdown("---")

if st.button("✅ Submit Feedback"):
    feedback_path = SUGGESTIONS_FILE.with_name("reviewed.json")
    feedback_path.write_text(json.dumps(data, indent=2))
    st.success(f"Feedback saved to {feedback_path}")

