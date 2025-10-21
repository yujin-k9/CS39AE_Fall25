import streamlit as st

st.title("👋 Hello World!")

# ---------- TODO: Replace with your own info ----------
NAME = "Yujin Kim"
PROGRAM = "Bachelor of Science in Computer Science"
INTRO = (
    "I am a senior student taking a Data Visualization class."
    "I like building interactive visualizations and learning new data tools."
)
FUN_FACTS = [
    "I drink five cups of decaf Americano every day.",
    "My hamster is four months old.",
    "I always open my fridge just to stare and close it again.",
]
PHOTO_PATH = "your_photo.png"  # Put a file in repo root or set a URL

# ---------- Layout ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    try:
        st.image(PHOTO_PATH, caption=NAME, use_container_width=True)
    except Exception:
        st.info("Add a photo named `your_photo.jpg` to the repo root, or change PHOTO_PATH.")
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.markdown("### Fun facts")
for i, f in enumerate(FUN_FACTS, start=1):
    st.write(f"- {f}")

st.divider()
st.caption("Edit `pages/1_Bio.py` to customize this page.")
